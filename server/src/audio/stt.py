from pathlib import Path

import whisper
import tempfile

asr_model = whisper.load_model("turbo")

def transcribe_audio(audio_bytes):
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir) / "audio.wav"

        with open(temp_path, "wb") as f:
            f.write(audio_bytes)

        result = asr_model.transcribe(str(temp_path))
        lines = [segment["text"].strip() for segment in result["segments"]]
        return "\n".join(lines)