import math
import os
import random
import time
from datetime import date
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from simplelist import listfromtxt, txtfromlist
import openai
import pyttsx3
import speech_recognition as rec
from API_Hidden_Key import api_key
from Control import *
from AppOpener import open, close




try:
    from spotify import *
except:
    pass

engine = pyttsx3.init()
r = rec.Recognizer()
mic = rec.Microphone()


def close_app(app_name, speech_text):
    close(app_name)
    engine.say(speech_text)
    engine.runAndWait()


def open_app(app_name, speech_text):
    open(app_name)
    engine.say(speech_text)
    engine.runAndWait()


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


math_operations = {
    "addition": lambda n1, n2: n1 + n2,
    "subtraction": lambda n1, n2: n1 - n2,
    "multiplication": lambda n1, n2: n1 * n2,
    "division": lambda n1, n2: n1 / n2,
    "modulus": lambda n1, n2: n1 % n2,
    "exponential": lambda n1, n2: n1 ** n2,
    "square root": lambda n1: n1 ** 0.5,
    "cube root": lambda n1: n1 ** 0.333,
    "square": lambda n1: n1 ** 2,
    "cube": lambda n1: n1 ** 3,
    "log": lambda n1: math.log(n1),
    "log base 10": lambda n1, n2=None: math.log10(n1) if n2 is None else "Invalid Operation",
    "log base 2": lambda n1, n2=None: math.log2(n1) if n2 is None else "Invalid Operation",
    "factorial": lambda n1, n2=None: math.factorial(n1) if n2 is None else "Invalid Operation",
    "sin": lambda n1, n2=None: math.sin(n1) if n2 is None else "Invalid Operation",
    "cos": lambda n1, n2=None: math.cos(n1) if n2 is None else "Invalid Operation",
    "tan": lambda n1, n2=None: math.tan(n1) if n2 is None else "Invalid Operation",
    "sin inverse": lambda n1, n2=None: math.asin(n1) if n2 is None else "Invalid Operaotion",
    "cos inverse": lambda n1, n2=None: math.acos(n1) if n2 is None else "Invalid Operatin",
    "tan inverse": lambda n1, n2=None: math.atan(n1) if n2 is None else "Invalid Operation",
    "arcsin": lambda n1, n2=None: math.asin(n1) if n2 is None else "Invalid Operation",
    "arccos": lambda n1, n2=None: math.acos(n1) if n2 is None else "Invalid Operation",
    "arctan": lambda n1, n2=None: math.atan(n1) if n2 is None else "Invalid Operation",
    "sinh": lambda n1, n2=None: math.sinh(n1) if n2 is None else "Invalid Operation",
    "cosh": lambda n1, n2=None: math.cosh(n1) if n2 is None else "Invalid Operation",
    "tanh": lambda n1, n2=None: math.tanh(n1) if n2 is None else "Invalid Operation",
    "sinh inverse": lambda n1, n2=None: math.asinh(n1) if n2 is None else "Invalid Operation",
    "cosh inverse": lambda n1, n2=None: math.acosh(n1) if n2 is None else "Invalid Operation",
    "tanh inverse": lambda n1, n2=None: math.atanh(n1) if n2 is None else "Invalid Operation",
    "arcsinh": lambda n1, n2=None: math.asinh(n1) if n2 is None else "Invalid Operation",
    "arccosh": lambda n1, n2=None: math.acosh(n1) if n2 is None else "Invalid Operation",
    "arctanh": lambda n1, n2=None: math.atanh(n1) if n2 is None else "Invalid Operation",
    "degrees": lambda n1, n2=None: math.degrees(n1) if n2 is None else "Invalid Operation",
    "radians": lambda n1, n2=None: math.radians(n1) if n2 is None else "Invalid Operation",
    "pi": lambda: math.pi,
    "e": lambda: math.e,
    "tau": lambda: math.tau,
    "gamma": lambda: math.gamma,
}


def user_input():
    user = input("{}: ".format(user_name))
    user.lower()


print("""\033[34m
             ███████╗░█████╗░██████╗░██╗░░░██╗  ░█████╗░██╗
             ╚════██║██╔══██╗██╔══██╗╚██╗░██╔╝  ██╔══██╗██║
             ░░███╔═╝███████║██████╔╝░╚████╔╝░  ███████║██║
             ██╔══╝░░██╔══██║██╔═══╝░░░╚██╔╝░░  ██╔══██║██║
             ███████╗██║░░██║██║░░░░░░░░██║░░░  ██║░░██║██║
             ╚══════╝╚═╝░░╚═╝╚═╝░░░░░░░░╚═╝░░░  ╚═╝░░╚═╝╚═╝\033[0m""")
openai.api_key = api_key()

conversation = ""
bot_name = "Zapy"
version = "1.0"
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

# initial functions

keywords = listfromtxt('keywords.txt')

response = listfromtxt('responses.txt')

current_time = time.strftime("%H:%M:%S", t)

# checking files

intial = """
█ █▄░█ █ ▀█▀ █ ▄▀█ █░░ █ ▀█ █ █▄░█ █▀▀   ▀█ ▄▀█ █▀█ █▄█
█ █░▀█ █ ░█░ █ █▀█ █▄▄ █ █▄ █ █░▀█ █▄█   █▄ █▀█ █▀▀ ░█░"""
dot = "   ▄ ▄ ▄"
engine.say("Initialising {}".format(bot_name))
engine.runAndWait()
print(intial, end='')
for char in dot:
    print(char, end='', flush=True)
    time.sleep(0.3)
print()
print("""𝕡𝕝𝕖𝕒𝕤𝕖 𝕨𝕒𝕚𝕥...""")
engine.say(" please wait")
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
engine.say("AI Chat Me BOT {}, version {}, Initiated".format(bot_name, version))
print("\033[32m{}: AI Chat Me BOT {}, version {}, Initiated\033[0m".format(bot_name, bot_name, version))
time.sleep(1)
engine.runAndWait()
user = input("\033[36mselect mode: \n 1. user mode\033[0m \n \033[31m2. dev mode\033[0m \n You: ") or "1"
save_response = "n"
if user == "1":
    print("{}: user mode selected".format(bot_name))
    engine.say("user mode selected")
    engine.runAndWait()
    print("{}: Text to speech enabled, use /voice to enable voice mode".format(bot_name))
    engine.say("Text to speech enabled, use /voice to enable voice mode")
    engine.runAndWait()
elif user == "2":
    print("\033[31m2{}: dev mode selected".format(bot_name))
    engine.say("dev mode selected")
    engine.runAndWait()
    engine.say("Do you want to save new response?")
    engine.runAndWait()
    save_response = input(
        "Do you want to save this response? (y/n) \n [tip: save when you are training the bot] \n You: ")
    print("{}: Text to speech enabled, use /voice to enable voice mode".format(bot_name))
    engine.say("Text to speech enabled, use /voice to enable voice mode")
    engine.runAndWait()

engine.say("Let me know your name, before we start")
engine.runAndWait()
print("{}: Let me know your name, before we start".format(bot_name))
user1name = input("please enter your name:") or "user"
print("{}: ""Hello! {} I am {}, a virtual assistant."
        " I'm here to answer your questions. How can I assist you today?".format(bot_name, user1name, bot_name))
engine.say(
    "Hello! {} I am {}, a virtual assistant. I am here to answer your questions. How can I assist you today?".format(
        user1name, bot_name))
engine.runAndWait()
user_name = "{}".format(user1name)
user = input("You: ")
user = user.lower()

while user != "bye":
    keyword_found = False
    # analise
    for index in range(len(keywords)):
        if keywords[index] == user:
            print("{}: ".format(bot_name) + response[index])
            engine.say(response[index])
            engine.runAndWait()
            keyword_found = True
            break
    # special
    if not keyword_found:
        for index in range(len(special)):
            if special[2] in user:
                try:
                    city = input("{}: Enter the Name of City ->  ".format(bot_name))
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
                operation = input("Enter operation (addition, subtraction, etc, exit): ")
                if operation == "exit":
                    keyword_found = True
                    break

                else:

                    n1 = float(input("Enter first number: "))

                    if operation in ["square root", "cube root", "square", "cube", "log", "log base 10",
                                     "log base 2",
                                     "factorial", "sin", "cos", "tan", "sin inverse", "cos inverse", "tan inverse",
                                     "arcsin", "arccos", "arctan", "sinh", "cosh", "tanh", "sinh inverse",
                                     "cosh inverse", "tanh inverse", "arcsinh", "arccosh", "arctanh", "degrees",
                                     "radians"]:

                        # If operation requires only one input, set n2 to a default value of 0

                        n2 = None

                    else:

                        n2 = float(input("Enter second number: "))

                    result = math_operations.get(operation, lambda x, y: "Invalid Operation")(n1, n2)

                    if isinstance(result, float):
                        print("Result: ", result)
                    else:
                        print(result)
                    keyword_found = True

            elif user == "hi" or user == "hello" or user == "hey":
                print("{}: ".format(bot_name) + random.choice(greetings))
                keyword_found = True

                break

            elif user == "change your name":
                bot_name = input("Enter new name: ")
                keyword_found = True
                break

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
                        print("Could not recognize,please try again")
                        engine.say("Could not recognize,please try again")
                        engine.runAndWait()
                        continue

                    if user_input in commands:
                        commands[user_input]()
                    else:
                        try:
                            prompt = user_name + ": " + user_input + "\n{}: ".format(bot_name)
                            conversation += prompt

                            response_ = openai.Completion.create(engine='text-davinci-003', prompt=conversation,
                                                                     max_tokens=50)
                            response_string = response_['choices'][0]['text'].replace("\n", " ")
                            response_string = \
                                response_string.split(user_name + ":", 1)[0].split("{}:".format(bot_name), 1)[0]

                            conversation += response_string + "\n"

                            print("{}: ".format(bot_name) + response_string)
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

        try:
            prompt = user_name + ": " + user_input + "\n{}:".format(bot_name)
            conversation += prompt

            _response = openai.Completion.create(engine='text-davinci-003', prompt=conversation, max_tokens=50)
            response_string = _response['choices'][0]['text'].replace("\n", " ")
            response_string = response_string.split(user_name + ":", 1)[0].split("{}:".format(bot_name), 1)[0]

            conversation += response_string + "\n"

            print("Zapy: " + response_string)
            engine.say(response_string)
            engine.runAndWait()
        except:
                print("Check your connection")
                new_keyword = user
                keywords.append(new_keyword)
                print("{}: SORRY!! I'm not sure how to respond".format(bot_name))
                print("{}: How should I respond to [ {} ] ?".format(bot_name, new_keyword))
                new_response = input("BotResponse: ")
                response.append(new_response)
                txtfromlist('keywords.txt', keywords)
                txtfromlist('responses.txt', response)
                print("{}: New response has been updated".format(bot_name))
                keyword_found = True
        if save_response == "y":
            keywords.append(user)
            response.append(response_string)
            txtfromlist('keywords.txt', keywords)
            txtfromlist('responses.txt', response)
            print("Response saved")
            engine.say("Response saved")
            engine.runAndWait()

    user = input("{}: ".format(user_name))
    user = user.lower()

print("{}:".format(bot_name), random.choice(goodbyes))


