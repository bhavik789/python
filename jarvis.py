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
import sys

# useful for sending auto email
mail_list = { "tushar": "gajjartushar4@gmail.com" ,"dharmesh":"sandershpatel1975@gmail.com","bhavik":"bhavik4063@gmail.com"}

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
    r.energy_threshold = 2000
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
    
    #constant check for reminder
    if os.listdir("reminder/"):
      files = os.listdir("reminder/")
      for i in files:
        # read file get title time data set by user
        k = open(f'reminder/{i}','r')
        line = k.read()
        data = line.split(" ")
        time_data = data[1].split(":")
        title = data[0]
        
        # get current time to compare with user given time
        current_time = datetime.datetime.now().strftime("%H %M %S")
        arr_time = current_time.split(" ") # stores time in string array format
        arr_int_time = [0,0,0] # will store time in int format
        for index,i in enumerate(arr_time):
          arr_int_time[index] = int(i)
        
        print(time_data,arr_int_time)
        if int(time_data[0]) == arr_int_time[0] and int(time_data[1]) == arr_int_time[1]:
          for i in range(5):
            speak(f"Reminder for {title}")
            time.sleep(0.2)
          os.remove(f"reminder/{title}.txt")
        

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
    elif 'search' in query or 'convert' in query:
      if 'convert' in query:
        query=query.replace("convert","formula for")
        query=query.replace("$","dollar ")
      else:
        query=query.replace("search","")

      links = googlesearch.search(query,tld='com', lang='en', tbs='0', safe='off', num=10, start=1,
           stop=1, pause=2.0, country='', extra_params=None,
           user_agent=None, verify_ssl=True)
      for i in links:
        webbrowser.open(i)
        speak("Opening site")      
        break
    
    # use notepad to store event in a file with time to remind it
    # continuousy read it using schedule module if time matches then remind it 
    # can keep reminder before 15 minutes
    
    elif 'reminder' in query:
      
      if(not os.path.exists("reminder")):
        os.mkdir("reminder")
        
      speak("what would you like me to remind you sir?")
      title = takeCommand().lower()
      print(f"Title for reminder {title}")
      
      while True:
        speak("Do you want to change name of your reminder sir?")
        consent = takeCommand().lower()
        
        if 'yes' in consent:
          speak("what should be the new name of the reminder sir?")
          title = takeCommand().lower()
          print(f"Title for reminder {title}")
          
        else:
          break
        
      
      f = open(f"reminder/{title}.txt","w")
      speak(f"after what time would you like me to remind about {title}?")
      time_of_reminder = takeCommand().lower()
      
      # Will be written in file for reminder
      store_time=datetime.datetime.now().strftime("%H %M %S")
      arr_time = store_time.split(" ") # stores time in string array format
      arr_int_time = [0,0,0] # will store time in int format
      for index,i in enumerate(arr_time):
        arr_int_time[index] = int(i)
        
      #used for getting hour minutes from user input
      store = time_of_reminder.split(" ")
      hours=''
      minutes=''
      
      ################### Hour Minutes Logic ###################
      
      #if time in hours and miuntes
      if 'hour' in time_of_reminder or'hours' in time_of_reminder:
        
        # get hours
        if 'hour' in time_of_reminder:
          hours = int(store[store.index("hour")-1])
        else:
          hours = int(store[store.index("hours")-1])
          
        arr_int_time[0] += hours
        
        #get minutes if any
        if 'minutes' in time_of_reminder or 'minute' in time_of_reminder:
          
          if 'minutes' in time_of_reminder:
            minutes = int(store[store.index("minutes")-1])
          else:
            minutes = int(store[store.index("minute")-1])
            
          arr_int_time[1] += minutes
          
        # both hours and minutes condition checked
        f.write(f"{title} {arr_int_time[0]}:{arr_int_time[1]}")
        f.close()
        speak(f"Reminder for {title} is successfully set at {arr_int_time[0]}:{arr_int_time[1]}")            
            
      #if time in only minutes
      if 'minutes' in time_of_reminder or 'minute' in time_of_reminder:
        
        if 'minutes' in time_of_reminder:
          minutes = int(store[store.index("minutes")-1])
        else:
          minutes = int(store[store.index("minute")-1])
          
        arr_int_time[1] += minutes
        
        f.write(f"{title} {arr_int_time[0]}:{arr_int_time[1]}")
        f.close()
        speak(f"Reminder for {title} is successfully set at {arr_int_time[0]}:{arr_int_time[1]}")
        
      ################### A.M. P.M. logic ###################
      
      if 'a.m.' in time_of_reminder:
        store_time = int(store[store.index("a.m.")-1])
        f.write(f"{title} {store_time}")
        f.close()
        speak(f"Reminder for {title} is successfully set at {store_time}")
      elif 'p.m.' in time_of_reminder:
        store_time = int(store[store.index("p.m.")-1])
        f.write(f"{title} {store_time}")
        f.close()
        speak(f"Reminder for {title} is successfully set at {store_time}")
        
    elif 'write' in query:  
      if(not os.path.exists("writer")):
        os.mkdir("writer")
        
      speak("what should be the name of the file sir?")
      title = takeCommand().lower()
      print(f"Title for your file {title}")
      
      while True:
        if (not os.path.exists(f"writer/{title}")):
          speak("Do you want to change name of your file sir?")
          consent = takeCommand().lower()
          
          if 'yes' in consent:
            speak("what should be the new name of the file sir?")
            title = takeCommand().lower()
            print(f"Title for file {title}")
          
          else:
            break
        else:
          speak("Name Already Exists Please Select Different Name sir!")
          title = takeCommand().lower()
          print(f"Title for your file {title}")
        
      f = open(f"write/{title}.txt","w")
      
      while True:
        text = takeCommand().lower()
        if 'quit' in text:
          break
        else:
          if 'fullstop' in text:
            text.replace("fullstop",'.')
          elif 'full stop' in text:
            text.replace("fullstop",'.')
            
          if 'comma' in text:
            text.replace("comma",',')
          
          if 'colon' in text:
            text.replace("colon",':')
            
          if 'semicolon' in text:
            text.replace("semicolon",';')
          
          if 'slash' in text:
            text.replace("slash",'/')
          
          if 'backslash' in text:
            text.replace("backslash",'\\')
          
          f.write(text)
  
    elif 'jarvis shut down' in query or 'jarvis shutdown' in query:
        speak("Call on me when needed sir")
        time.sleep(0.3)
        speak("I am always ready to help")
        break
    