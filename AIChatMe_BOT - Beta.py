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
from Control import decrease, increase
from AppOpener import open

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
special = ['day', 'time', 'weather', 'add', 'addition', 'subtract', 'subtraction', 'multiply', 'multiplication',
           'division', 'divide', "/ai"]
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


def addition(n1, n2):
    addi = n1 + n2
    print("Result = ", addi)


def subtraction(n1, n2):
    sub = n1 - n2
    print("Result = ", sub)


def multiplication(n1, n2):
    mul = n1 * n2
    print("Result = ", mul)


def division(n1, n2):
    div = n1 / n2
    rem = n1 % n2
    print("Quotient = ", div)
    print("Remainder = ", rem)


# checking files
time.sleep(1)
print("checking files")
time.sleep(1)
Keyword_file = os.path.exists('keywords.txt')
response_file = os.path.exists('responses.txt')
print("keywords found status :", Keyword_file)
print("Response found status :", response_file)
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
time.sleep(1)
print("its", current_time, dt)
print("Bot:", random.choice(greetings))
user = input("You: ")
user = user.lower()
while user != "bye":
    keyword_found = False
    # analise
    for index in range(len(keywords)):
        if keywords[index] == user:
            print("Bot: " + response[index])
            keyword_found = True
            break
    # special
    if not keyword_found:
        for index in range(len(special)):
            if special[2] in user:
                try:
                    city = input("Bot: Enter the Name of City -> ")
                    city = city + " weather"
                    weather(city)
                    keyword_found = True
                except BaseException:
                    print("An error occurred")
                    print("[Check your Connection]")
                    keyword_found = True
                    pass
                break

            elif special[3] == user or special[2] == user:
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))
                addition(num1, num2)
                keyword_found = True
                break
            elif special[5] == user or special[6] == user:
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))
                subtraction(num1, num2)
                keyword_found = True
                break
            elif special[7] == user or special[8] == user:
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))
                multiplication(num1, num2)
                keyword_found = True
                break
            elif special[9] == user or special[10] == user:
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))
                division(num1, num2)
                keyword_found = True
                break
            elif special[11] == user:
                while True:
                    with mic as source:
                        print("Listening...")
                        r.adjust_for_ambient_noise(source, duration=0.2)
                        audio = r.listen(source)
                        print("no longer listening...")
                    try:
                        user_input = r.recognize_google(audio)
                        print("You said: " + user_input)

                    except BaseException:
                        print("Could not understand audio, please try again")
                        engine.say("Could not understand audio, please try again")
                        engine.runAndWait()
                        continue
                    if user_input == "open WhatsApp":
                        open("whatsapp")
                        engine.say("opening whatsapp")
                        engine.runAndWait()
                    if user_input == "open Google":
                        open("google chrome")
                        engine.say("opening google")
                        engine.runAndWait()
                    if user_input == "open YouTube":
                        open("youtube")
                        engine.say("opening youtube")
                        engine.runAndWait()
                    if user_input == "open Firefox":
                        open("firefox")
                        engine.say("opening firefox")
                        engine.runAndWait()
                    if user_input == "decrease volume" or user_input == "degrees volume" or user_input == "decrease the volume":
                        decrease()
                        engine.say("decreasing volume")
                        engine.runAndWait()
                    if user_input == "increase volume" or user_input == "increase the volume":
                        increase()
                        engine.say("increasing volume")
                        engine.runAndWait()
                    else:
                        prompt = user_name + ": " + user_input + "\nBot: "
                        conversation += prompt

                        response = openai.Completion.create(engine='text-davinci-003', prompt=conversation,
                                                            max_tokens=100)
                        response_string = response['choices'][0]['text'].replace("\n", " ")
                        response_string = response_string.split(user_name + ":", 1)[0].split("Bot:", 1)[0]

                        conversation += response_string + "\n"

                        print("Bot: " + response_string)
                        engine.say(response_string)
                        engine.runAndWait()

                        if user_input == "exit":
                            break
                keyword_found = True
                break

    if not keyword_found:
        user_input = user

        prompt = user_name + ": " + user_input + "\nBot: "
        conversation += prompt

        response = openai.Completion.create(engine='text-davinci-003', prompt=conversation, max_tokens=50)
        response_string = response['choices'][0]['text'].replace("\n", " ")
        response_string = response_string.split(user_name + ":", 1)[0].split("Bot:", 1)[0]

        conversation += response_string + "\n"

        print("Bot: " + response_string)
        engine.say(response_string)
        engine.runAndWait()
        keyword_found = True

    user = input("You: ")
    user = user.lower()

print("Bot:", random.choice(goodbyes))

