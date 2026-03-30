import datetime
import os
import win32com.client
import speech_recognition as sr
import webbrowser
from google import genai
from google.genai import types
from config import apikey

speaker = win32com.client.Dispatch('SAPI.SpVoice')

def say(text):
    speaker.Speak(text)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
            return query
        except Exception:
            return "Some Error Occurred. Sorry from Jarvis"

def chat_with_gemini(prompt):
    client = genai.Client(api_key=apikey)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0)
        )
    )
    return response.text

if __name__ == '__main__':
    print('PyCharm')
    say("Hello, I am Jarvis AI")
    while True:
        print("Listening...")
        query = takeCommand()

        if "exit" in query.lower():
            say("Goodbye sir")
            break

        # Dictionary for sites
        sites = {
            "youtube": "https://www.youtube.com",
            "wikipedia": "https://www.wikipedia.com",
            "google": "https://www.google.com"
        }

        # Dictionary for apps (process names)
        apps = {
            "chrome": "chrome.exe",
            "notepad": "notepad.exe",
            "camera": "WindowsCamera.exe"
        }

        # Open sites
        if query.lower().startswith("open "):
            site_name = query.lower().replace("open ", "").strip()
            if site_name in sites:
                say(f"Opening {site_name} sir...")
                webbrowser.open(sites[site_name])
                continue

        # Close apps
        elif query.lower().startswith("close "):
            app_name = query.lower().replace("close ", "").strip()
            if app_name in apps:
                say(f"Closing {app_name} sir...")
                os.system(f"taskkill /f /im {apps[app_name]}")
            else:
                say("Sorry sir, I don't know how to close that yet.")

        # Play music
        elif "play music" in query.lower():
            musicPath = r'C:\Users\vaibh\Downloads\SlavaFunk.mp3'
            say("Playing music sir")
            os.startfile(musicPath)

        # Tell time
        elif "the time" in query.lower():
            hour = datetime.datetime.now().strftime("%H")
            minute = datetime.datetime.now().strftime("%M")
            say(f"Sir, the time is {hour} bajke {minute} minutes")

        # Open camera
        elif "open camera" in query.lower():
            say("Opening camera sir")
            os.system("start microsoft.windows.camera:")

        # AI intelligence
        elif "intelligence" in query.lower():
            reply = chat_with_gemini(query)
            print("Gemini:", reply)
            say(reply)

        # Default AI response
        else:
            reply = chat_with_gemini(query)
            print("Gemini:", reply)
            say(reply)