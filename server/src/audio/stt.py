import whisper
import tempfile

asr_model = whisper.load_model("turbo")

def transcribe_audio(audio_bytes):
    with tempfile.NamedTemporaryFile(suffix=".wav") as temp_audio:
        temp_audio.write(audio_bytes)
        temp_audio.flush()

        result = asr_model.transcribe(temp_audio.name)
        return result["text"]