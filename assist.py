# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 19:33:38 2019

@author: Sir_Lighton
"""



import speech_recognition as sr
import os
import sys
import re
import webbrowser
import smtplib
import requests
import subprocess
from pyowm import OWM
import youtube_dl
import vlc
import urllib
import urllib.request
import json
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import wikipedia
import random
from time import strftime




def sofiaResponse(audio):
    "speaks audio passed as argument"
    print(audio)
    for line in audio.splitlines():
        os.system("say" + audio)


def myCommand():
    "listen for commands"
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something....")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio).lower()
        print("You said: " + command + "\n")
        #loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print(".....")
        command = myCommand();
        return command

def assistant(command):
    "if statements for executing commands"

    #open reddit
    if "open reddit" in command:
        url = "https://www.reddit.com"
        webbrowser.open(url)
        sofiaResponse("Reddit has been opened for you Sir")

    elif "shutdown" in command:
        sofiaResponse("Bye bye. Have a nice day")
        sys.exit()

    #open a website
    elif "visit" in command:
        reg_ex = re.search("open (.+)", command)
        if reg_ex:
            domain = reg_ex.group(1)
            print(domain)
            url = "http://www." + domain
            webbrowser.open(url)
            sofiaResponse("The website you requested has been open for you Sir,")
        else:
            pass



    #Greetings
    elif "hello" in command:
        day_time = int(strftime("%H"))
        if day_time < 12:
            sofiaResponse("Hello Sir. Good morning")
        elif 12 <= day_time < 18:
            sofiaResponse("Hello Sir. Good afternoon")
        else:
            sofiaResponse("Hello Sir. Good evening")

    #help
    elif "help me" in command:
        sofiaResponse("""You can use these commands and I'll help you out:
        1. Open reddit subreddit : Opens the subreddit in default browser.
        2. Open xyz.com : replace xyz with any website name
        3. Current weather in {cityname} : Tells you the current condition and temperture
        4. Hello
        5. play me a video : Plays song in your VLC media player
        6. change wallpaper : Change desktop wallpaper
        7. news for today : reads top news of today
        8. time : Current system time
        9. top stories from google news (RSS feeds)
        10. tell me about xyz : tells you about xyz
        """)

    #tell a joke
    elif "joke" in command:
        res = requests.get(
            'https://icanhazdadjoke.com/',
            headers ={"Accept" : "application/json"})
        if res.status_code == requests.codes.ok:
            sofiaResponse(str(res.json()['joke']))
        else:
            sofiaResponse("Ooops, I ran out of jokes")

    #top stories from google
    elif "news for today" in command:
        try:
            news_url = "https://news.google.com/news/rss"
            Client = urlopen(news_url)
            xml_page=Client.read()
            Client.close()
            soup_page = soup(xml_page,"xml")
            news_list = soup_page.findAll("items")
            for news in news_list[:15]:
                sofiaResponse(news.title.text.encode('utf-8'))
        except Exception as e:
            print(e)

    #current weather
    elif "current weather" in command:
        reg_ex = re.search("current weather in (.+)", command)
        if reg_ex:
            city = reg_ex.group(1)
            owm = OWM(API_key='ab0d5e80e8dafb2cb81fa9e82431c1fa')
            obs = owm.weather_at_place(city)
            w = obs.get_weather()
            k = w.get_status()
            x = w.get_temperature(unit="celsius")
            sofiaResponse(
                'Current weather in %s is %s. The maximum temperature is %0.2f and '
                'the minimum temperature is %0.2f degree celcius' % (city, k, x['temp_max'], x['temp_min']))



    #tell time
    elif "time" in command:
        import datetime
        now = datetime.datetime.now()
        sofiaResponse("Current time is %d hours %d minutes" % (now.hour, now.minute))


    #send mail
    elif 'email' in command:
        sofiaResponse('Who is the recipient?')
        recipient = myCommand()
        if 'friend' in recipient:
            sofiaResponse('What should I say to him?')
            content = myCommand()
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail.ehlo()
            mail.starttls()
            mail.login('your_email_address', 'your_password')
            mail.sendmail('sender_email', 'receiver_email', content)
            mail.close()
            sofiaResponse('Email has been sent successfuly. You can check your inbox.')
        else:
            sofiaResponse('I don\'t know what you mean!')

    #launch any app
    elif "open" in command:
        reg_ex = re.search("launch (.+)",command)
        if reg_ex:
            appname = reg_ex.group(1)
            appname1 = appname +".exe"
            subprocess.Popen(["open","-n" ,"/Applications/" + appname1], stdout = subprocess.PIPE)
        sofiaResponse("I have launched the desired app")

    # play youtube song
    elif "play me a song" in command:
        path = '//Users/Sir_Lighton/video'
        folder = path
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)
    sofiaResponse('What song shall I play Sir?')
    mysong = myCommand()
    if mysong:
        flag = 0
        url = "https://www.youtube.com/results?search_query=" + mysong.replace(' ', '+')
        response = urllib.request.urlopen(url)
        html = response.read()
        soup1 = soup(html, "lxml")
        url_list = []
        for vid in soup1.findAll(attrs={'class': 'yt-uix-tile-link'}):
            if ('https://www.youtube.com' + vid['href']).startswith("https://www.youtube.com/watch?v="):
                flag = 1
                final_url = 'https://www.youtube.com' + vid['href']
                url_list.append(final_url)
        url = url_list[0]
        ydl_opts = {}
        os.chdir(path)
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            vlc.play(path)
            if flag == 0:
                sofiaResponse('I have not found anything in Youtube ')

#askme anything
    elif 'tell me about' in command:
        reg_ex = re.search('tell me about (.*)', command)
        try:
            if reg_ex:
                topic = reg_ex.group(1)
                ny = wikipedia.page(topic)
                sofiaResponse(ny.content[:500].encode('utf-8'))
        except Exception as e:
                print(e)
                sofiaResponse(e)


sofiaResponse("Hi User, I am sofia and I am your personal voice assistant, Please give me a command or say 'help me'"
              "and I will tell you what all I can do for you")

#loop to continue executing multiple commands
while True:
    assistant(myCommand())