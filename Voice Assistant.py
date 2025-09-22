import edge_tts
import asyncio
import speech_recognition as sr
from playsound import playsound
import uuid
import os

# قاموس الأوامر المدعومة والكود اللي ينفذها
commands = {
    "يوتيوب": "start chrome https://www.youtube.com",
    "حاسبه": "start calc",
    "متصفح": "start chrome",
    "شات جي بي تي": "start chrome https://chat.openai.com",
    "اعد تشغيل الجهاز": "shutdown /r /t 5",
    "اغلق الجهاز": "shutdown /s /t 5",
    "الاعدادات": "start ms-settings:",
}

async def text_to_speech_arabic(text):
    filename = f"{uuid.uuid4()}.mp3"
    communicate = edge_tts.Communicate(text, voice="ar-AE-FatimaNeural")
    await communicate.save(filename)
    playsound(filename)
    os.remove(filename)

def listen_and_recognise():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("تفضل، تكلم الآن...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language="ar-SA")
        print(f"سمعت: {text}")
        return text
    except sr.UnknownValueError:
        print("لم أفهم ما قلت، حاول مرة ثانية.")
        return ""
    except sr.RequestError as e:
        print(f"هناك مشكلة في الاتصال: {e}")
        return ""

def execute_command(text):
    for key in commands:
        if key in text:
            os.system(commands[key])
            return f"تم تنفيذ أمر: {key}"
    return "عذرًا، لم أفهم الأمر."

def main():
    while True:
        text = listen_and_recognise()
        if text:
            response = execute_command(text)
            asyncio.run(text_to_speech_arabic(response))
        else:
            asyncio.run(text_to_speech_arabic("لم أسمع أمرًا واضحًا."))

if __name__ == "__main__":
    main()

