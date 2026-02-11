from fastapi import APIRouter
from fastapi.openapi.models import Response
from pathlib import Path
from fastapi import BackgroundTasks

from server.src.constants import TRANSCRIPT_FILE, SUMMARY_FILE, CHUNKS_FILE
from server.src.rag.chunking import generate_chunks
from server.src.rag.inference import get_rag_model
from server.src.state import state, Status
from server.src.summarization.summarize import summarize_transcript
from server.src.transcription.transcribe import transcribe

router = APIRouter()

def cleanup():
    Path(TRANSCRIPT_FILE).unlink(missing_ok=True)
    Path(SUMMARY_FILE).unlink(missing_ok=True)
    Path(CHUNKS_FILE).unlink(missing_ok=True)

    state.status = Status.AWAITING_DATA
    state.rag_model = None

def session_audio_handler(audio: bytes):
    transcribe(audio)
    summarize_transcript()
    generate_chunks()
    state.rag_model = get_rag_model()
    state.status = Status.READY

@router.post("/session-audio", status_code=200)
def handle_session_audio(audio: bytes, response: Response, background_tasks: BackgroundTasks):
    if state.status == Status.PROCESSING:
        response.status_code = 202
        return {"error": "Processing already started"}

    cleanup()
    state.status = Status.PROCESSING
    session_audio_handler(audio)
    background_tasks.add_task(session_audio_handler, audio)

    return {"status": "ok"}

@router.get("/transcript", status_code=200)
def get_transcript(response: Response):
    if state.status != Status.READY:
        response.status_code = 503
        return {"error": "No transcript available yet"}
    return Path(TRANSCRIPT_FILE).read_text()

@router.get("/summary", status_code=200)
def get_summary(response: Response):
    if state.status != Status.READY:
        response.status_code = 503
        return {"error": "No summary available yet"}
    return Path(SUMMARY_FILE).read_text()