import pyttsx3
import speech_recognition
import datetime
import requests
from bs4 import BeautifulSoup
import pywhatkit

def say():
    recog = speech_recognition.Recognizer()
    try:
        with speech_recognition.Microphone() as mic:
            recog.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recog.listen(mic, timeout=1.0)
            text = recog.recognize_google(audio)
            text = text.lower()
    except:
        text = ''
        # speech_recognition.UnknownValueError()
        # recog = speech_recognition.Recognizer()
    return text

def speak(text, gender):
    try:
        audio = pyttsx3.init()
        if gender=="female":
            voices = audio.getProperty('voices')
            audio.setProperty('voice', voices[1].id)
        audio.setProperty("rate", 140)
        audio.say(text)
        audio.runAndWait()
    except KeyboardInterrupt:
        audio.terminate()
    # audio.stop()

def wishMe(name, gender):
    speak("Hi "+ name, gender)
    speak("How can i help you?", gender)
    # hour = int(datetime.datetime.now().hour)
    # if hour>= 0 and hour<12:
    #     speak("Good Morning "+name, gender)
  
    # elif hour>= 12 and hour<18:
    #     speak("Good Afternoon "+name, gender)  
  
    # else:
    #     speak("Good Evening "+name, gender)
  

def time_now():
    time = datetime.datetime.now().strftime('%I:%M')
    return time

def breaking_news():
    record = ""
    url = "https://observerbd.com/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    titles = soup.find_all('span', class_="title_inner")
    for title in titles:
        news_title = title.find('a').text.strip()
        news = title.find('a')
        link = news['href']
        final = '<li><a class="text-dark" href="https://observerbd.com/'+ link +'">'+news_title+'. '+'</a></li>'
        record+=final
    return record

def sports_news():
    record = ""
    url = "https://observerbd.com/cat.php?cd=185"
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    titles = soup.find_all('div', class_="title_inner")
    for title in titles:
        news_title = title.find('a').text.strip()
        news = title.find('a')
        link = news['href']
        final = '<li><a class="text-dark" href="https://observerbd.com/'+ link +'">'+news_title+'. '+'</a></li>'
        record+=final
    return record

def play_yt(video):
    pywhatkit.playonyt(video)
