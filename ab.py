import os
import pyttsx3
import speech_recognition as sr
import random
import webbrowser
import datetime
from plyer import notification
import pyautogui
"""import wikipedia
import pywhatkit as pwk
import user_config
import smtplib, ssl
import openai_request as ai
import image_generation"""
import mtranslate
 
engine = pyttsx3.init() 
voices = engine.getProperty('voices')
engine.setProperty('voice', voices [2].id)
engine.setProperty("rate", 170)
def speak(audio):
  engine.say(audio)
  engine.runAndWait()



def command():
  content = ""
  while content == "":
   # obtain audio from the microphone
     r = sr. Recognizer()
     with sr. Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
     try:
        content = r.recognize_google (audio, language='en-in')
        content = mtranslate.translate (content, to_language="en-in")
        print("You Said.." + content)
     except Exception as e:
        print("Please try again...")
  return content
def main_process():
   jarvis_chat = []
   while True:
     request = command().lower()
     if "hello" in request :
        speak("welcome, how can i help you.")
     elif "play music" in request:
         speak("playing music")
         song = random.randint(1,3)
         if song ==1:
            webbrowser.open("")
         elif song == 2:
            webbrowser.open("")
         elif song == 3:
            webbrowser.open("")
     elif "say time" in request:
        now_time = datetime.datetime.now().strftime("%H:%M")
        speak("Current time is " + str(now_time))
     elif "say dob" in request:
      now_date = datetime.datetime.now().strftime("%d:%m")
      speak("Current date is " + str(now_date))
     elif "new task" in request:
        task = request.replace("new task", "")
        task = task.strip()
        if task != "":
           speak("Adding task: "+ task)
           with open ("todo.txt", "a") as file:
               file.write(task + "\n")
     elif "speak task" in request:
        with open ("todo.txt", "r") as file:
           speak("Work we have to do today is"  + file.read())
     elif "show work" in request:
        with open ("todo.txt", "r") as file: 
           task = file.read()
        notification.notify(
           title = "today's work",
           message = task
           ) 
     elif "open" in request:
        query = request.replace("open", "")
        pyautogui.press("super")
        pyautogui.typewrite(query)
        pyautogui.sleep(2)
        pyautogui.press("enter")
     elif "close" in request:
        if request.strip() == "close":
           try:
               active_window = gw.getActiveWindow()
               if active_window:
                  app_title = active_window.title
                  active_window.close()
                  speak(f"Closed active window: {app_title}")
               else:
                 speak("No active window found.")
           except Exception as e:
              print("Error:", e)
              speak("Unable to close the current window.")
        else:
           app_name = request.replace("close", "").strip()
           if app_name != "":
              speak(f"Closing {app_name}")
              os.system(f"taskkill /f /im {app_name}.exe")
           else:
             speak("Please tell me which application to close.")     
main_process()

                     
