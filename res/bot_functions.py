from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import requests
from bs4 import BeautifulSoup
import pyttsx3
from selenium.common.exceptions import WebDriverException
import speech_recognition as rec


class BotFunctions:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) '
                          'Chrome/58.0.3029.110 Safari/537.3'
        }

    def search_youtube(self, text):
        try:
            browser = webdriver.Chrome()
            browser.get('https://www.youtube.com/')
            search_box = browser.find_element(By.NAME, 'search_query')
            search_box.send_keys(text)
            search_box.send_keys(Keys.RETURN)
            time.sleep(10)
            results = browser.find_elements(By.ID, 'video-title')
            results[0].click()
            time.sleep(10)
            browser.quit()
        except WebDriverException:
            print("An exception occurred while using WebDriver.")
        except rec.UnknownValueError:
            print("Speech Recognition could not understand audio.")
        except rec.RequestError as e:
            print(f"Could not request results from Speech Recognition service; {e}.")
        except Exception as e:
            print(f"An unexpected error occurred; {e}.")

    def say(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def close_app(self, app_name, speech_text):
        # Add your close app logic here
        self.say(speech_text)
        self.engine.runAndWait()

    def open_app(self, app_name, speech_text):
        # Add your open app logic here
        self.say(speech_text)
        self.engine.runAndWait()

    def weather(self, place="Chennai"):
        place = place.replace(" ", "+")
        resource = requests.get(
            f'https://www.google.com/search?q={place}&oq={place}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourced'
            f'=chrome&ie=UTF-8',
            headers=self.headers)
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
        self.say(f"the weather in {location} is {info} and the temperature is {temp} degrees celsius")
