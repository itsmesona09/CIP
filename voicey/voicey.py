import speech_recognition as sr
from gtts import gTTS
import random
import json
import os
import pyautogui
import webbrowser
import datetime

# Load intents from a JSON file
with open("intents.json", "r") as file:
    intents = json.load(file)

def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for commands...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        print("Could not understand audio. Please try again.")
        return None
    except sr.RequestError:
        print("Unable to access the Google Speech Recognition API.")
        return None

def respond(text):
    print(text)
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")
    os.system("afplay response.mp3")  # macOS specific

def get_intent(command):
    for intent in intents["intents"]:
        for pattern in intent["pattern"]:
            if pattern.lower() in command:
                return intent
    return None

todos = []

def handle_intent(intent, command):
    tag = intent["tag"]
    response = random.choice(intent["responses"])
    action = intent.get("action_url")

    if action == "time":
        time_now = datetime.datetime.now().strftime("%I:%M %p")
        respond(f"The current time is {time_now}.")
    elif action == "date":
        today = datetime.datetime.now().strftime("%A, %B %d, %Y")
        respond(f"Today is {today}.")
    elif action and action.startswith("http"):
        webbrowser.open(action)
        respond(response)
    elif tag == "screenshot":
        pyautogui.screenshot("screenshot.png")
        respond("Screenshot taken and saved.")
    elif tag == "exit":
        respond(response)
        exit()
    else:
        respond(response)

def main():
    respond("Heyyy!!! We go party party now!")
    while True:
        command = listen_for_command()
        if command:
            intent = get_intent(command)
            if intent:
                handle_intent(intent, command)
            else:
                respond("uff")

if __name__ == "__main__":
    main()
