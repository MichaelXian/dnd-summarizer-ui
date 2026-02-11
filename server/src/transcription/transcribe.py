from pathlib import Path
import whisper

from server.src.constants import TRANSCRIPT_FILE

model = whisper.load_model("turbo")

def transcribe(audio: bytes) -> None:
    transcript = model.transcribe(audio)
    save_transcription(transcript["text"])

def save_transcription(transcription: str) -> None:
    Path(TRANSCRIPT_FILE).write_text(transcription)