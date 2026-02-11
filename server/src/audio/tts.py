import pyttsx3

engine = pyttsx3.init()

async def text_to_speech(text: str):
    engine.say(text)
    engine.runAndWait()