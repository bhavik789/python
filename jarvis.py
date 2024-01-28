from datetime import date, datetime
from email.mime import multipart
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import datetime
import googlesearch
from numpy import take
import pyttsx3
import speech_recognition as sr
import wikipedia
import webbrowser
import smtplib
from email.mime.base import MIMEBase
import googleapiclient as gac
import time

# id for calender event
extra=1
id = str(extra)+"_"+datetime.datetime.now().strftime("%D")
# print(id)

# useful for sending auto email
mail_list = { "tushar gajjar": "gajjartushar4@gmail.com" ,"dharmesh":"sandershpatel1975@gmail.com","bhavik":"bhavik4063@gmail.com"}

# creates and selects voices from your device
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# voices in your computer / device
# print(voices)
# print(voices[0].id)
# print(voices[1].id)

engine.setProperty('voice', voices[0].id)

# Jarvis Speaks using this function
def speak(audio):
  engine.say(audio)
  engine.runAndWait()

# Jarvis Wishes or greets using this function
def wishme():
  hour = int(datetime.datetime.now().hour)

  if hour >= 0 and hour < 12:
    speak("Good Morning!")

  elif hour >= 12 and hour < 18:
    speak("Good Afternoon!")

  else:
    speak("Good Evening!")
  speak("I am Jarvis sir, Please tell me how may I help you!")

# Jarvis takes voice input using this function
def takeCommand():
  '''
    it takes microphone input from user and returns string output 
    '''

  r = sr.Recognizer()
  with sr.Microphone() as source:
    print("Listening...")
    r.pause_threshold = 1
    r.energy_threshold = 1000
    # r.operation_timeout = 5
    audio = r.listen(source)

  try:
    print("Recognizing")
    query = r.recognize_google(audio, language='en-in') # type: ignore
    print(f"User said: {query}\n")

  except Exception as e:
    # print(e)
    print("Say that again please...")
    return "None"

  return query

# Jarvis auto sends email using this function
def sendemail(to,content):
  server = smtplib.SMTP('smtp.gmail.com',587)
  server.ehlo()
  server.starttls()
  server.login("bhavik4063@gmail.com","pglvuijlnvtvewhg")
  server.sendmail("bhavik4063@gmail.com",to,content)
  server.close()
  
  
# main code start
if __name__ == "__main__":
  wishme()

  while True:
      
    query = takeCommand().lower()
  
    #logic for executing tasks based on query
    
    #opens wikipedia and searchs for a specific question
    if 'wikipedia' in query:
        speak('Searching Wikipedia...')
        quert = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences = 2)
        speak("According to wikipedia")
        print(results)
        speak(results)

    # opens youtube
    elif 'open youtube' in query:
        speak("opening Youtube")
        webbrowser.open("youtube.com")
        
    #opens google
    elif 'open google' in query:
        speak("opening google")
        webbrowser.open("google.com")
    
    #opens stackoverflow
    elif 'open stackoverflow' in query:
        speak("opening stackoverflow")
        webbrowser.open("stackoverflow.com")
        
    #plays music from pc
    elif 'play music' in query:
        music_dir = 'H:\\1New folder'
        songs = os.listdir(music_dir)
        print(songs)    # can use radom module and play differet songs each time
        os.startfile(os.path.join(music_dir,songs[0]))
        
    #tells the current time
    elif 'the time' in query:
        strTime=datetime.datetime.now().strftime("%H:%M:%S")
        print(strTime)
        speak(f"sir, the time is {strTime}")
        
    #opens vscode
    elif 'open code' in query:
        codepath = "C:\\Users\\Admin\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
        os.start(codepath) # type: ignore
    
    # sends email using voice command
    elif 'send email' in query:
        try:
          
          msg = MIMEMultipart()
          
          speak("What is the subject sir?")
          print("What is the subject sir?")
          msg['Subject'] = takeCommand().lower()
          
          speak("What is the message sir")
          content = takeCommand().lower()
          msg.attach(MIMEText(content,'plain')) # type: ignore
          print(msg)
          findname = query.split(" ") # split and get the string and name after to like "send email to bhavik" get bhavik after splitting
          ind = findname.index("to")
          name = findname[ind+1]
          to = mail_list[name] # email id
          sendemail(to,msg.as_string())
          speak("email has been sent")
          
        except Exception as e:
          print(e)
          speak("Sorry sir, i was not able to sent the email")
      
    # uses google search to search using voice command    
    elif 'search' in query:
      query=query.replace("search","")

      links = googlesearch.search(query,tld='com', lang='en', tbs='0', safe='off', num=10, start=0,
           stop=None, pause=2.0, country='', extra_params=None,
           user_agent=None, verify_ssl=True)
      for i in links:
        webbrowser.open(i)
        speak("Opening site")      
        break
      
    elif 'jarvis shut down' in query:
        speak("Call on me when needed sir")
        time.sleep(0.3)
        speak("I am always ready to help")
        break
    