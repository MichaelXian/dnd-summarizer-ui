from server.src.transcription.constants import TRANSCRIPT_FILE
import whisper

model = whisper.load_model("turbo")

async def transcribe(audio: bytes) -> None:
    transcript = model.transcribe(audio)
    save_transcription(transcript["text"])

def save_transcription(transcription: str) -> None:
    with open(TRANSCRIPT_FILE, "w") as f:
        f.write(transcription)