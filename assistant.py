import os
import webbrowser
import datetime
import urllib.parse
import speech_recognition as sr
import pyttsx3
from openai import OpenAI

# OpenAI API — set the OPENAI_API_KEY environment variable before running
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Ses motoru
engine = pyttsx3.init()

def speak(text):
    print("Asistan:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Dinleniyor...")
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio, language="tr-TR")
        print("Sen:", command)
        return command.lower()
    except sr.UnknownValueError:
        speak("Sizi anlayamadım, lütfen tekrar söyleyin.")
        return ""
    except sr.RequestError as e:
        speak("Ses tanıma servisine ulaşılamıyor.")
        print(f"Ses tanıma hatası: {e}")
        return ""

def ai_response(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI API hatası: {e}")
        return "Şu anda yanıt veremiyorum, lütfen daha sonra tekrar deneyin."

def run_assistant():
    speak("Hazırım, seni dinliyorum.")

    while True:
        command = listen()

        if "saat kaç" in command:
            now = datetime.datetime.now().strftime("%H:%M")
            speak(f"Saat {now}")

        elif "google'da ara" in command:
            query = command.replace("google'da ara", "").strip()
            webbrowser.open(f"https://www.google.com/search?q={urllib.parse.quote_plus(query)}")
            speak("Google'da arıyorum")

        elif "youtube aç" in command:
            webbrowser.open("https://youtube.com")
            speak("YouTube açılıyor")

        elif "çık" in command:
            speak("Görüşürüz!")
            break

        elif command != "":
            cevap = ai_response(command)
            speak(cevap)

if __name__ == "__main__":
    run_assistant()
