from tkinter import *
import numpy as np
import cv2
import PIL.Image
import PIL.ImageTk
import pyttsx3
import datetime
import time
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import random
import smtplib
import pyowm
from PIL import Image
import requests
import handTrackingModule as htm
from tkinter.messagebox import showinfo


def speak(text: str):
    engine = pyttsx3.init()

    engine.setProperty('rate', 10)
    engine.setProperty('volume', 100)

    engine.say(text)
    engine.runAndWait()


def record():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.pause_threshold = 2
        audio = r.listen(source)

        try:
            query = r.recognize_google(audio, language="en-IN")
        except Exception as e:
            showinfo(title='Error!', message=e)
            speak("I am sorry, I did not get that, but could you please repeat that")

            return "Nothing"
        return query


# ------------------------------------------------------------------------------------
def SignLangauge():
    stt_wn = Toplevel(root)
    stt_wn.title('Number Sign Detection')
    stt_wn.geometry("350x200")
    stt_wn.configure(bg='IndianRed')

    Label(stt_wn, text='Signlangauge Converter', font=(
        "Comic Sans MS", 15), bg='IndianRed').place(x=50)

    def getNumber(ar):
        s = ""
        for i in ar:
            s += str(ar[i])

        if(s == "00000"):
            return (0)
        elif(s == "01000"):
            return(1)
        elif(s == "01100"):
            return(2)
        elif(s == "01110"):
            return(3)
        elif(s == "01111"):
            return(4)
        elif(s == "11111"):
            return(5)
        elif(s == "01001"):
            return(6)
        elif(s == "01011"):
            return(7)
        elif(s == "01101"):
            return(8)
        elif(s == "11001"):
            return(9)

    wcam, hcam = 640, 480
    cap = cv2.VideoCapture(0)
    cap.set(3, wcam)
    cap.set(4, hcam)
    pTime = 0
    detector = htm.handDetector(detectionCon=0.75)
    while True:
        success, img = cap.read()
        img = detector.findHands(img, draw=True)
        lmList = detector.findPosition(img, draw=False)
        # print(lmList)
        tipId = [4, 8, 12, 16, 20]
        if(len(lmList) != 0):
            fingers = []
            # thumb
            if(lmList[tipId[0]][1] > lmList[tipId[0]-1][1]):
                fingers.append(1)
            else:
                fingers.append(0)
            # 4 fingers
            for id in range(1, len(tipId)):

                if(lmList[tipId[id]][2] < lmList[tipId[id]-2][2]):
                    fingers.append(1)

                else:
                    fingers.append(0)

            cv2.rectangle(img, (20, 255), (170, 425), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, str(getNumber(fingers)), (45, 375), cv2.FONT_HERSHEY_PLAIN,
                        10, (255, 0, 0), 20)
        
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (400, 70),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), 3)
        cv2.imshow("image", img)
        if(cv2.waitKey(1) & 0xFF == ord('q')):
        
            break
    
    pass


# Creating the main TTS and STT functions and the instruction functions
def TTS():
    tts_wn = Toplevel(root)
    tts_wn.title('Text-to-Speech Converter')
    tts_wn.geometry("350x250")
    tts_wn.configure(bg='Brown')

    Label(tts_wn, text='Text-to-Speech Converter',
          font=("Comic Sans MS", 15), bg='Brown').place(x=50)

    text = Text(tts_wn, height=5, width=30, font=12)
    text.place(x=7, y=60)

    speak_btn = Button(tts_wn, text='Record', bg='LightCoral',
                       command=lambda: speak(str(text.get(1.0, END))))
    speak_btn.place(x=140, y=200)


def STT():
    stt_wn = Toplevel(root)
    stt_wn.title('Speech-to-Text Converter')
    stt_wn.geometry("350x200")
    stt_wn.configure(bg='IndianRed')

    Label(stt_wn, text='Speech-to-Text Converter',
          font=("Comic Sans MS", 15), bg='IndianRed').place(x=50)

    text = Text(stt_wn, font=12, height=3, width=30)
    text.place(x=7, y=100)

    record_btn = Button(stt_wn, text='Record', bg='Sienna',
                        command=lambda: text.insert(END, record()))
    record_btn.place(x=140, y=50)


def get_location():
    # """ Function To Print GeoIP Latitude & Longitude """
    ip_request = requests.get('https://get.geojs.io/v1/ip.json')
    my_ip = ip_request.json()['ip']
    geo_request = requests.get(
        'https://get.geojs.io/v1/ip/geo/' + my_ip + '.json')
    geo_data = geo_request.json()
    geo = geo_data['city']
    return geo


a = {'Vikram Jha BE Project Group 15': 'vikramjha718@gmail.com'}
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

window = Tk()

global var
global var1

var = StringVar()
var1 = StringVar()


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def sendemail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    # replace with master/sender email id and app-password generated from email provider
    server.login('vikramjha718@gmail.com', 'vikram419@#')
    server.sendmail('vikramjha718@gmail.com',
                    'vikramjha719@gmail.com', 'hello sir')
    server.close()


def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour <= 12:
        var.set("Good Morning Sir")
        window.update()
        speak("Good Morning Sir!")
    elif hour >= 12 and hour <= 18:
        var.set("Good Afternoon Sir!")
        window.update()
        speak("Good Afternoon Sir!")
    else:
        var.set("Good Evening Sir")
        window.update()
        speak("Good Evening Sir!")
    speak("Myself NATASHA! How may I help you")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        var.set("Listening...")
        window.update()
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 400
        audio = r.listen(source)
    try:
        var.set("Recognizing...")
        window.update()
        print("Recognizing")
        query = r.recognize_google(audio, language='en-in')
    except Exception as e:
        return "None"
    var1.set(query)
    window.update()
    return query


def play():
    btn2['state'] = 'disabled'
    btn0['state'] = 'disabled'
    btn1.configure(bg='orange')
    wishme()
    while True:
        btn1.configure(bg='orange')
        city = get_location()

        query = takeCommand().lower()
        if 'exit' in query:
            var.set("Bye sir")
            btn1.configure(bg='#5C85FB')
            btn2['state'] = 'normal'
            btn0['state'] = 'normal'
            window.update()
            speak("Bye sir have a nice day ")
            break

        elif 'wikipedia' in query:
            if 'wikipedia' in query:
                try:
                    speak("searching")
                    query = query.replace("according to internet", "")
                    results = wikipedia.summary(query, sentences=2)
                    speak("According to internet")
                    var.set(query)
                    window.update()
                    speak(results)
                except Exception as e:
                    var.set('sorry sir could not find any results')
                    window.update()
                    speak('sorry sir could not find any results')
            else:
                try:
                    speak("searching in internet")
                    query = query.replace("according to internet", "")
                    results = wikipedia.summary(query, sentences=2)
                    speak("According to internet")
                    var.set(query)
                    window.update()
                    speak(results)
                except Exception as e:
                    var.set('sorry sir could not find any results')
                    window.update()
                    speak('sorry sir could not find any results')

        elif 'open youtube' in query:
            var.set('opening Youtube')
            window.update()
            speak('opening Youtube')
            webbrowser.open("youtube.com")

        elif 'open coursera' in query:
            var.set('opening coursera')
            window.update()
            speak('opening coursera')
            webbrowser.open("coursera.com")

        elif 'open google' in query:
            var.set('opening google')
            window.update()
            speak('opening google')
            webbrowser.open("google.com")

        elif 'mylocation' in query:
            ip_request = requests.get('https://get.geojs.io/v1/ip.json')
            my_ip = ip_request.json()['ip']
            geo_request = requests.get(
            'https://get.geojs.io/v1/ip/geo/' + my_ip + '.json')
            geo_data = geo_request.json()
            geo = geo_data['city']
            return geo

            pass

        elif 'say hello' in query:
            var.set('Hello Everyone! My self Natasha')
            window.update()
            speak('Hello Everyone! My self Natasha')

        elif 'hello' in query:
            var.set('Hello')
            window.update()
            speak("Hello")

        elif 'ok' in query:
            var.set('ok')
            window.update()
            speak("ok sir ")

        elif 'open stack overflow' in query:
            var.set('opening stackoverflow')
            window.update()
            speak('opening stackoverflow')
            webbrowser.open('stackoverflow.com')

        elif ('play music' in query) or ('change music' in query):
            # elif ('play music' in query):
            var.set('Here are your favorites')
            window.update()
            speak('Here are your favorites')
            music_dir = 'E:\\HP\\music'
            songs = os.listdir(music_dir)
            n = random.randint(0, 2)
            os.startfile(os.path.join(music_dir, songs[n]))

        elif 'no content available' in query:
            strtime = datetime.datetime.now().strftime("%H:%M:%S")
            var.set("Sir the time is %s" % strtime)
            window.update()
            speak("Sir the time is %s" % strtime)

        elif 'the date' in query:
            strdate = datetime.datetime.today().strftime("%d %m %y")
            var.set("Sir today's date is %s" % strdate)
            window.update()
            speak("Sir today's date is %s" % strdate)

        elif 'thank you' in query:
            var.set("Welcome")
            window.update()
            speak("Welcome")

        elif 'can you do for me' in query:
            var.set(
                'I can do multiple tasks for you sir.\n tell me whatever you want to perform sir')
            window.update()
            speak(
                'I can do multiple tasks for you sir. tell me whatever you want to perform sir')

        elif 'old are you' in query:
            var.set("I am a little baby")
            window.update()
            speak("I am a little baby")

        elif 'your name' in query:
            var.set("Myself Natasha Sir")
            window.update()
            speak('myself Natasha sir')

        # elif 'weather' in query:
        #     owm = pyowm.OWM('api-key')  # open weather map API key
        #     # current weather forecast
        #     loc = owm.weather_at_place(city)
        #     weather = loc.get_weather()
        #     # status
        #     status = weather.get_detailed_status()
        #     var.set(f'{status} in {city}')
        #     window.update()
        #     speak(f'{status} in {city}')
        #     # temperature
        #     temp = weather.get_temperature(unit='celsius')
        #     for key, val in temp.items():
        #         if key == 'temp':
        #             var.set(f'{val} degree celcius')
        #             window.update()
        #             speak(f"current temperature is {val} degree celcius")
        #     # humidity, wind, rain, snow
        #     humidity = weather.get_humidity()
        #     wind = weather.get_wind()
        #     var.set(f'{humidity} grams per cubic meter')
        #     window.update()
        #     speak(f'humidity is {humidity} grams per cubic meter')
        #     var.set(f'wind {wind}')
        #     window.update()
        #     speak(f'wind {wind}')
        #     # sun rise and sun set
        #     sr = weather.get_sunrise_time(timeformat='iso')
        #     ss = weather.get_sunset_time(timeformat='iso')
        #     var.set(sr)
        #     window.update()
        #     speak(f'SunRise time is {sr}')
        #     var.set(ss)
        #     window.update()
        #     speak(f'SunSet time is {ss}')
        #     # clouds and rain
        #     loc = owm.three_hours_forecast(city)
        #     clouds = str(loc.will_have_clouds())
        #     rain = str(loc.will_have_rain())
        #     if clouds == 'True':
        #         var.set("It may have clouds in next 5 days")
        #         window.update()
        #         speak("It may have clouds in next 5 days")
        #     else:
        #         var.set("It may not have clouds in next 5 days")
        #         window.update()
        #         speak("It may not have clouds in next 5 days")
        #     if rain == 'True':
        #         var.set("It may rain in next 5 days")
        #         window.update()
        #         speak("It may rain in next 5 days")
        #     else:
        #         var.set("It may not rain in next 5 days")
        #         window.update()
        #         speak("It may not rain in next 5 days")

        elif 'email to' in query:
            try:
                query = query.replace("email to", "")
                query = query.replace(" ", "")
                print(query)
                var.set("What should I say")
                window.update()
                speak('what should I say')
                content = takeCommand()
                to = a[query]
                sendemail('vikramjha719@gmail.com', 'hello sir good evening')
                var.set('Email has been sent!')
                window.update()
                speak('Email has been sent!')

            except Exception as e:
                print(e)
                var.set("Sorry Sir! I was not able to send this email")
                window.update()
                speak('Sorry Sir! I was not able to send this email')

        elif 'click photo' in query:
            stream = cv2.VideoCapture(0)
            grabbed, frame = stream.read()
            if grabbed:
                cv2.imshow('pic', frame)
                cv2.imwrite('pic.jpg', frame)
            stream.release()

        elif 'record video' in query:
            cap = cv2.VideoCapture(0)
            out = cv2.VideoWriter(
                'output.avi', cv2.VideoWriter_fourcc(*"MJPG"), 30, (640, 480))
            while(cap.isOpened()):
                ret, frame = cap.read()
                if ret:

                    out.write(frame)

                    cv2.imshow('frame', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                else:
                    break
            cap.release()
            out.release()
            cv2.destroyAllWindows()


def update(ind):
    frame = frames[(ind) % 100]
    ind += 1
    label.configure(image=frame)
    window.after(100, update, ind)


label2 = Label(window, textvariable=var1, bg='#FAB60C')
label2.config(font=("Courier", 20))
var1.set('User Said:')
label2.pack()

label1 = Label(window, textvariable=var, bg='#ADD8E6')
label1.config(font=("Courier", 20))
var.set('Welcome')
label1.pack()

frames = [PhotoImage(file='assist.gif', format='gif -index %i' % (i))
          for i in range(100)]
window.title('NATASHA')

label = Label(window, width=1500, height=500)
label.pack()
Label(text='BE-Project  Group  15  AI Desktop Virtual Assistant',
      font=('Comic Sans MS', 16), bg='Salmon', wrap=True, wraplength=300).place(x=0, y=0)
window.after(0, update, 0)


btn0 = Button(text='WISH ME', width=20, command=wishme, bg='#5C85FB')
btn0.config(font=("Courier", 12))
btn0.pack()
btn1 = Button(text='START', width=20, command=play, bg='#5C85FB')
btn1.config(font=("Courier", 12))
btn1.pack()
btn2 = Button(text='EXIT', width=20, command=window.destroy, bg='#5C85FB')
btn2.config(font=("Courier", 12))
btn2.pack()
btn3 = Button(text='TTS Conversion', width=20, command=TTS, bg='#5C85FB')
btn3.config(font=("Courier", 12))
btn3.pack()
btn4 = Button(text='STT Conversion', width=20, font=(
    'Helvetica', 16), bg='MediumPurple', command=STT)
btn4.config(font=("Courier", 12))
btn4.pack()

btn5 = Button(text='Sign Language', width=20, font=(
    'Helvetica', 16), bg='MediumPurple', command=SignLangauge)
btn5.config(font=("Courier", 12))
btn5.pack()




root = Tk()
root.title('BEProject python text to speech and speech to text Converter')
root.geometry('300x300')
root.resizable(0, 0)
root.configure(bg='Salmon')

root.update()
root.mainloop()

window.mainloop()
