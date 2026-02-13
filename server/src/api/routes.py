from pathlib import Path
from fastapi import BackgroundTasks, APIRouter, UploadFile, File, Response

from server.src.audio.stt import transcribe_audio
from server.src.audio.tts import text_to_speech
from server.src.constants import TRANSCRIPT_FILE, SUMMARY_FILE, CHUNKS_FILE
from server.src.rag.chunking import generate_chunks
from server.src.rag.inference import get_rag_model
from server.src.state import state, Status
from server.src.summarization.summarize import summarize_transcript
from server.src.transcription.refine import refine
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
    refine()
    generate_chunks()
    state.rag_model = get_rag_model()
    state.status = Status.READY

@router.post("/session-audio", status_code=200)
async def handle_session_audio(
        response: Response,
        background_tasks: BackgroundTasks,
        file: UploadFile = File(...),
):
    if state.status == Status.PROCESSING:
        response.status_code = 202
        return {"error": "Processing already started"}

    cleanup()
    audio: bytes = await file.read()
    state.status = Status.PROCESSING
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

@router.post("/chat", status_code=200)
async def chat(file: UploadFile, res`ponse: Response, background_tasks: BackgroundTasks):
    if state.status != Status.READY:
        response.status_code = 503
        return {"error": "Chat available yet"}

    audio = await file.read()
    query = transcribe_audio(audio)
    model_response = state.rag_model.chat(query)

    background_tasks.add_task(text_to_speech, model_response)

    return {
        "query": query,
        "response": model_response
    }
