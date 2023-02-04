import os
import random
import time
from datetime import date
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from simplelist import listfromtxt
import openai
import pyttsx3
import speech_recognition as rec
from API_Hidden_Key import api_key
from Control import *
from AppOpener import open, close
from spotify import song, songv

openai.api_key = api_key()

engine = pyttsx3.init()

r = rec.Recognizer()
mic = rec.Microphone()
conversation = ""
user_name = "Jefino"

# resource initialisation
t = time.localtime()
d = date.today()
dt = datetime.now().strftime('%A')
current_time = time.strftime("%H:%M:%S", t)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
greetings = ["Hello!", "What's up?!", "Howdy!", "Greetings!"]
goodbyes = ["Bye!", "Goodbye!", "See you later!", "See you soon!"]
special = ['day', 'time', 'weather', "/voice", "maths"]
res = [dt, current_time, ]
keywords = listfromtxt('keywords.txt')
response = listfromtxt('responses.txt')
current_time = time.strftime("%H:%M:%S", t)


# initial functions
def weather(place="Chennai"):
    place = place.replace(" ", "+")
    resource = requests.get(
        f'https://www.google.com/search?q={place}&oq={place}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourced=chrome&ie=UTF-8',
        headers=headers)
    print("Searching...")
    soup = BeautifulSoup(resource.text, 'html.parser')
    location = soup.select('#wob_loc')[0].getText().strip()
    place_time = soup.select('#wob_dts')[0].getText().strip()
    info = soup.select('#wob_dc')[0].getText().strip()
    temp = soup.select('#wob_tm')[0].getText().strip()
    print(location)
    print(place_time)
    print(info)
    print(temp + "°C")
    engine.say(f"the weather in {location} is {info} and the temperature is {temp} degrees celsius")


math_operations = {
    "addition": lambda n1, n2: n1 + n2,
    "subtraction": lambda n1, n2: n1 - n2,
    "multiplication": lambda n1, n2: n1 * n2,
    "division": lambda n1, n2: n1 / n2
}


def play_song():
    with mic as origin:
        print("say the name of the song")
        engine.say("say the name of the song")
        engine.runAndWait()
        r.adjust_for_ambient_noise(origin, duration=0.2)
        sound = r.listen(origin)
        print("Recognizing...")
        engine.say("Recognizing...")
        engine.runAndWait()
    try:
        users_text = r.recognize_google(sound)
        print("You said: " + users_text)
    except BaseException:
        print("cant recognize, please try again")
        engine.say("cant recognize, please try again")
        engine.runAndWait()
        return
    song(users_text)
    engine.say("playing music")
    engine.runAndWait()


def open_app(app_name, speech_text):
    open(app_name)
    engine.say(speech_text)
    engine.runAndWait()


def close_app(app_name, speech_text):
    close(app_name)
    engine.say(speech_text)
    engine.runAndWait()


# checking files
engine.say("Initialising Zapy, please wait")
engine.runAndWait()
time.sleep(1)

Keyword_file = os.path.exists('keywords.txt')
response_file = os.path.exists('responses.txt')
time.sleep(1)

if not Keyword_file:
    print("keyword file not found")
    time.sleep(2)
    print("creating (keywords.txt) file")
    open("keywords.txt", "x")
    print("done")
if not response_file:
    print("response file not found")
    time.sleep(2)
    print("creating (responses.txt) file")
    open("responses.txt", "x")
    print("done")

# bot starts
print("Zapy:", random.choice(greetings))
engine.say("AI Chat Me BOT ZAPY, version 1.0, Initiated")
time.sleep(1)
engine.runAndWait()
print("Zapy: Text to speech enabled, use /voice to enable voice mode")
engine.say("Text to speech enabled, use /voice to enable voice mode")
engine.runAndWait()
user = input("You: ")
user = user.lower()
while user != "bye":
    keyword_found = False
    # analise
    for index in range(len(keywords)):
        if keywords[index] == user:
            print("Zapy: " + response[index])
            engine.say(response[index])
            engine.runAndWait()
            keyword_found = True
            break
    # special
    if not keyword_found:
        for index in range(len(special)):
            if special[2] in user:
                try:
                    city = input("Bot: Enter the Name of City -> ")
                    engine.say("Enter the Name of City")
                    city = city + " weather"
                    weather(city)
                    keyword_found = True
                except:
                    print("An error occurred")
                    engine.say("An error occurred")
                    print("[Check your Connection]")
                    engine.say("Check your Connection")
                    keyword_found = True
                    pass
                break
            elif user == "play a song" or user == "play song" or user == "play a song for me" or user == "play song for me":
                engine.say("playing a song")
                engine.runAndWait()
                songv()
                keyword_found = True
                break
            elif special[4] == user:
                operation = input("Enter operation (addition, subtraction, multiplication, division, exit): ")
                if operation == "exit":
                    keyword_found = True
                    break

                else:
                    n1 = float(input("Enter first number: "))
                    n2 = float(input("Enter second number: "))
                    result = math_operations.get(operation, "Invalid Operation")(n1, n2)

                    if isinstance(result, float):
                        print("Result: ", result)
                    else:
                        print(result)

            elif special[3] == user:
                print("voice mode enabled")
                engine.say("voice mode enabled")
                engine.runAndWait()
                commands = {
                    "open Google": lambda: open_app("google chrome", "opening google"),
                    "open chrome": lambda: open_app("google chrome", "opening google"),
                    "open YouTube": lambda: open_app("youtube", "opening youtube"),
                    "open WhatsApp": lambda: open_app("whatsapp", "opening whatsapp"),
                    "open Firefox": lambda: open_app("firefox", "opening firefox"),
                    "play a song": play_song,
                    "increase brightness": increase_,
                    "increase the brightness": increase_,
                    "decrease volume": decrease,
                    "decrease the volume": decrease,
                    "increase volume": increase,
                    "increase the volume": increase,
                    "decrease brightness": decrease_,
                    "decrease the brightness": decrease_,
                    "open camera": lambda: open_app("camera", "opening camera"),
                    "open calculator": lambda: open_app("calculator", "opening calculator"),
                    "open Notepad": lambda: open_app("notepad", "opening notepad"),
                }
                while True:
                    with mic as source:
                        print("listening...")
                        engine.say("listening...")
                        engine.runAndWait()
                        r.adjust_for_ambient_noise(source, duration=0.2)
                        audio = r.listen(source)
                        print("recognising...")
                        engine.say("recognising...")
                        engine.runAndWait()
                    try:
                        user_input = r.recognize_google(audio)
                        print("You said: " + user_input)
                    except:
                        print("Could not understand audio")
                        engine.say("Could not understand audio")
                        engine.runAndWait()
                        continue

                    if user_input in commands:
                        commands[user_input]()
                    else:
                        try:
                            prompt = user_name + ": " + user_input + "\nZapy: "
                            conversation += prompt

                            response_ = openai.Completion.create(engine='text-davinci-003', prompt=conversation,
                                                                 max_tokens=100)
                            response_string = response_['choices'][0]['text'].replace("\n", " ")
                            response_string = response_string.split(user_name + ":", 1)[0].split("Zapy:", 1)[0]

                            conversation += response_string + "\n"

                            print("Zapy: " + response_string)
                            engine.say(response_string)
                            engine.runAndWait()
                        except:
                            print("check your internet connection")
                            engine.say("check your internet connection")
                            engine.runAndWait()
                            continue

                    if user_input == "exit":
                        break
                keyword_found = True
                break
    if not keyword_found:
        user_input = user

        prompt = user_name + ": " + user_input + "\nZapy: "
        conversation += prompt

        _response = openai.Completion.create(engine='text-davinci-003', prompt=conversation, max_tokens=50)
        response_string = _response['choices'][0]['text'].replace("\n", " ")
        response_string = response_string.split(user_name + ":", 1)[0].split("Zapy:", 1)[0]

        conversation += response_string + "\n"

        print("Zapy: " + response_string)
        engine.say(response_string)
        engine.runAndWait()
        keyword_found = True

    user = input("You: ")
    user = user.lower()

print("Zapy:", random.choice(goodbyes))
