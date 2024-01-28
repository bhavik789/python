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
    
    # sets up a reminder and reminds you some task
    # elif 'reminder' in query:
    #   # print()
    #   speak("What should i remind you sir")
    #   summary = takeCommand().lower()
      
    #   speak(f"At what time should i remind you about {summary}")
    #   strtime=takeCommand().lower()
    
    #   data = MIMEMultipart()
    #   data['kind']='calendar#calendarListEntry'
    #   data['id']=id
    #   extra+=1
    #   data['summary'] = summary
    #   data['accessRole']="owner"
    #   data['backgroundColor']='#0088aa'
    #   data['defaultReminders']='''[{"method": "popup","minutes": 15}]'''
    #   data['notificationSettings']='''{"notifications": [{"type": "eventCreation","method": "email"}]}'''
                                        
    #   if 'a.m.' in strtime:
    #     tim = strtime.split(" ")
    #     findtim = tim.index('a.m.')
    #     data['timezone'] = 'Asia/Kolkata'
      
      
    #   link = f'https://calendar.google.com/calendar/u/0/r/{data.as_string()}'
    #{data.as_string()}
    
    
    # new code
    
    
    # elif 'reminder' in query:
      
    #   event = MIMEMultipart()
      
    #   speak("What should i remind you sir")
    #   summary = takeCommand().lower()

    #   # while True:
    #   #   speak("")
      
    #   speak(f"At what time should i remind you about {summary} please answer me in am pm format or hours or minutes from now")
    #   strtime=takeCommand().lower()
      
    #   while True:
    #     speak(f"Do you want to change time of {summary} ,sir?")
    #     opt = takeCommand().lower()

    #     if 'yes' in opt:
    #       speak(f"At what time should i remind you about {summary} please answer me in am pm format or hours or minutes from now")
    #       strtime=takeCommand().lower()
        
    #     elif 'no' in opt:
    #       break

    #   d = date.today()
    #   arr = strtime.split(" ")

      
    #   if 'a.m.' in strtime:
    #     ind = arr.index("a.m.") - 1
    #     dt = datetime.datetime(d.year, d.month, d.day, int(strtime[ind]), 00, 00)

    #   elif 'p.m.' in strtime:
    #     ind = arr.index("p.m.") - 1
    #     dt = datetime.datetime(d.year, d.month, d.day, int(strtime[ind]), 00, 00)
      
    #   elif 'hour' in strtime:
        
    #     if 'hours' in strtime:
    #       hr = arr.index("hours") - 1
    #     else:
    #       hr = arr.index("hour") - 1
                   
    #     dt = datetime.datetime(d.year, d.month, d.day, int(strtime[hr]), 00, 00)
    #     if 'minute' in strtime:
    #       if 'minutes' in strtime:
    #         min = arr.index("minutes") - 1
    #       else:
    #         min = arr.index("minute") - 1
    #       dt = datetime.datetime(d.year, d.month, d.day, int(strtime[hr]), int(strtime[min]), 00)

      
    #   event['start']="{'dateTime': f'{dt}','timeZone':'Aisa/Kolkata'}"
    #   event['end']='''{
    #                     'dateTime': f'{dt}',
    #                     'timeZone':'Aisa/Kolkata'
    #                     }'''
    #   # event["etag"]= etag
    #   # event["updated"]= datetime
    #   event["kind"]= "calendar#event"
    #   event["id"]= id
    #   event["status"]= 'confirmed'
    #   event["created"]= datetime.datetime.now()
    #   event["summary"]= summary
    #   event["description"]= ''
    #   # event["location"]= ''
    #   event["colorId"]= 5
    #   event["creator"]= {
    #                     "id": id,
    #                     "email": 'bhavik4063@gmail.com',
    #                     "displayName": 'Bhavik',
    #                     "self": True
    #                     }
    #   # event["htmlLink"]= f'https://calendar.google.com/calendar/u/0/r/{event.as_string()}'
     
    #   link = f'https://calendar.google.com/calendar/u/0/r/{event.as_string()}'
    #   #https://www.googleapis.com/calendar/v3/calendars/[CALENDARID]/events?key=[YOUR_API_KEY] HTTP/1.1
    #   #  API KEY = AIzaSyDCAxKjaoRwEnzmb3NY4Md9VZUQDMW_6d8
    #   # POST https://www.googleapis.com/calendar/v3/calendars/abc/events?conferenceDataVersion=3&sendNotifications=true&key=[YOUR_API_KEY]

    #   # Authorization: Bearer [YOUR_ACCESS_TOKEN]
    #   # Accept: application/json
    #   # Content-Type: application/json

    #   # {
    #   #   "end": {
    #   #     "dateTime": "",
    #   #     "timeZone": ""
    #   #   },
    #   #   "start": {
    #   #     "dateTime": "",
    #   #     "timeZone": ""
    #   #   },
    #   #   "reminders": {
    #   #     "overrides": []
    #   #   },
    #   #   "summary": ""
    #   # }
      
      
    #   webbrowser.open(link)
      
    elif 'jarvis shut down' in query:
        speak("Call on me when needed sir")
        time.sleep(0.3)
        speak("I am always ready to help")
        break
    