from pathlib import Path

from server.src.audio.stt import transcribe_audio
from server.src.constants import TRANSCRIPT_FILE

def transcribe(audio: bytes) -> None:
    text = transcribe_audio(audio)
    save_transcription(text)

def save_transcription(transcription: str) -> None:
    Path(TRANSCRIPT_FILE).write_text(transcription)