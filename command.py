import os
import pyttsx3
import speech_recognition as sr
import pywhatkit
import random
import webbrowser
import wikipedia
import datetime
from plyer import notification
import pyautogui
import pytesseract
import cv2
import time
from PIL import ImageGrab, Image
import re
import eel
from google import genai
from google.genai import types
from io import BytesIO
import sys
import threading
# -------------------- CONFIG -------------------- #
INPUT_MODE = "voice"
last_search_query = ""

# -------------------- GEMINI API -------------------- #
GEMINI_API_KEY = "AIzaSyAT6vGCAb8L05zzogH9QdSwK2_u409g5Gs"  # apna key daalna
client_gemini = genai.Client(api_key=GEMINI_API_KEY)

# -------------------- INIT EEL -------------------- #
eel.init("web")  # zara.html folder

# -------------------- SPEAK FUNCTION -------------------- #
# -------------------- SPEAK FUNCTION -------------------- #
class FrontendLogger:
    def write(self, message):
        if message.strip():  # खाली लाइन नहीं भेजेगा
            try:
                eel.show_terminal_output(message)
            except:
                pass
        sys.__stdout__.write(message)  # टर्मिनल पर भी दिखाएगा

    def flush(self):
        sys.__stdout__.flush()

sys.stdout = FrontendLogger()

# -------------------- SPEAK FUNCTION -------------------- #
engine = pyttsx3.init()  # सिर्फ एक बार init
voices = engine.getProperty('voices')

# Female Hindi first preference
female_voice_set = False
for v in voices:
    if ("female" in v.name.lower() or "female" in v.id.lower()) and \
       ("hindi" in v.name.lower() or "hindi" in v.id.lower()):
        engine.setProperty('voice', v.id)
        female_voice_set = True
        break

# अगर Hindi female ना मिले तो English female (e.g., Zira)
if not female_voice_set:
    for v in voices:
        if "female" in v.name.lower() or "zira" in v.name.lower():
            engine.setProperty('voice', v.id)
            break

engine.setProperty("rate", 170)        
def speak(audio: str):
    try:
        eel.show_terminal_output(audio)
    except:
        pass
    engine.say(audio)
    engine.runAndWait()        
# -------------------- GEMINI TEXT -------------------- 

def ask_gemini(question: str) -> str:
    """Gemini clean short answer"""
    try:
        response = client_gemini.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Answer in min 100 words without ** or markdown formatting:\n{question}",
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=0)
            ),
        )
        answer = response.text or ""
        return answer
    except Exception as e:
        return f"Gemini error: {e}" 
def ask_gemini_image(prompt: str):
    """Generate image from Gemini"""
    try:
        response = client_gemini.models.generate_content(
            model="gemini-2.0-flash-preview-image-generation",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE']
            )
        )

        for part in response.candidates[0].content.parts:
            # if getattr(part, "text", None):
                # अगर Gemini कोई text भी भेजता है तो सुनाओ
                #speak(part.text)
            if getattr(part, "inline_data", None):
                try:
                    # Base64 decode करो
                    image = Image.open(BytesIO((part.inline_data.data)))
                    filename = "zara_image.png"
                    image.save(filename)
                    image.show()
                    speak(f"Image saved as {filename}")
                except Exception as e:
                    speak(f"Image decode error: {e}")
        return True
    except Exception as e:
        speak(f"Gemini image error: {e}")
        return False

# -------------------- OCR CLICK -------------------- #
def click_on_text(target_text: str) -> bool:
    time.sleep(1)
    screenshot = ImageGrab.grab()
    screenshot.save("screen.png")
    image = cv2.imread("screen.png")

    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    for i, word in enumerate(data["text"]):
        if word.lower() == target_text.lower():
            x = data["left"][i]
            y = data["top"][i]
            w = data["width"][i]
            h = data["height"][i]
            pyautogui.moveTo(x + w // 2, y + h // 2)
            pyautogui.click()
            return True
    speak(f"Text '{target_text}' not found on screen.")
    return False

# -------------------- CLOSE APPS -------------------- #
def close_application(app_name: str):
    exe_name_map = {
        "chrome": "chrome.exe",
        "firefox": "firefox.exe",
        "edge": "msedge.exe",
        "notepad": "notepad.exe",
        "vlc": "vlc.exe",
        "spotify": "Spotify.exe",
        "whatsapp": "WhatsApp.exe",
        "telegram": "Telegram.exe",
        "discord": "Discord.exe",
        "calculator": "CalculatorApp.exe",
        "word": "WINWORD.EXE",
        "excel": "EXCEL.EXE",
        "vs code": "Code.exe",
        "paint": "mspaint.exe",
        "cmd": "cmd.exe",
        "powershell": "powershell.exe",
        "zoom": "Zoom.exe",
        "pycharm": "pycharm64.exe",
        "obs": "obs64.exe",
        "teams": "Teams.exe",
        "file": "explorer.exe",
        "control panel": "control.exe",
        "setting": "SystemSetting.exe",
    }
    exe_name = exe_name_map.get(app_name.lower(), f"{app_name}.exe")
    try:
        result = os.system(f"taskkill /f /im {exe_name}")
        if result == 0:
            speak(f"{app_name} closed.")
        else:
            speak(f"Unable to close {app_name}.")
    except Exception:
        speak(f"Error closing {app_name}")


# -------------------- PROCESS COMMAND -------------------- #

@eel.expose
def process_command(user_text):
    global last_search_query
    request = user_text.lower().strip()
    print(f"\nYou said: {user_text}")

    # हमेशा पहले वही बोले जो यूज़र ने लिखा
    
    # ---- Known commands ---- #
    if "hello@" in request:
        speak("Welcome, Alfaaz how can I help you.")

    elif "banaya@" in request:
        speak("I have been made by a BCA group which includes Alfaaz, SATYAM, Himanshu, Deepak, Akash")

    elif "whatsapp@" in request and "bolo" in request:
        match = re.search(r"(.*?)\s*ko\s*whatsapp\s*par\s*bolo\s*(.+)", request)
        if match:
            contact = match.group(1).strip()
            message = match.group(2).strip()
            speak(f"{contact} ko WhatsApp par ye sandesh bhej raha hoon: {message}")
            webbrowser.open("https://web.whatsapp.com")
            time.sleep(25)
            try:
                pyautogui.click(150, 200)
                time.sleep(2)
                pyautogui.write(contact)
                time.sleep(3)
                pyautogui.press("enter")
                time.sleep(2)
                pyautogui.write(message)
                time.sleep(1)
                pyautogui.press("enter")
                speak("Message bhej diya gaya hai.")
            except Exception:
                speak("Message bhejne mein samasya aayi.")
        else:
            speak("WhatsApp command samajh nahi aaya. Kripya dobara try karein.")

    elif "play music@" in request:
        speak("Playing music")
        webbrowser.open("https://www.youtube.com/watch?v=8of5w7RgcTc&list=RD8of5w7RgcTc&start_radio=1")

    elif "open youtube@" in request:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "search@" in request and "youtube" in request:
        last_search_query = request.replace("search", "").replace("on youtube", "").strip()
        speak(f"Searching {last_search_query} on YouTube")
        webbrowser.open(f"https://www.youtube.com/results?search_query={last_search_query}")
        speak("Here are the results. Say 'play first video' to start.")

    elif "play first video@" in request and last_search_query:
        speak(f"Playing {last_search_query}")
        pywhatkit.playonyt(last_search_query)

    elif "stop@" in request or "play" in request:
        pyautogui.press("k")
        speak("Toggled play and pause")

    elif "full screen@" in request:
        pyautogui.press("f")
        speak("Fullscreen enabled")

    elif "half screen@" in request:
        pyautogui.press("f")
        speak("Half screen enabled")

    elif "mute@" in request:
        pyautogui.press("m")
        speak("Mute toggled")

    elif "change@" in request:
        pyautogui.hotkey("shift", "n")
        speak("Next video playing")

    elif "open instagram@" in request:
        speak("Opening Instagram")
        webbrowser.open("https://www.instagram.com")

    elif "time@" in request:
        now_time = datetime.datetime.now().strftime("%H:%M")
        speak("Current time is " + str(now_time))

    elif "date@" in request:
        now_date = datetime.datetime.now().strftime("%d:%m")
        speak("Current date is " + str(now_date))

    elif "new work@" in request:
        task = request.replace("new task", "").strip()
        if task:
            speak("Adding task: " + task)
            with open("zara.txt", "a", encoding='utf-8') as file:
                file.write(task + "\n")

    elif "speak task@" in request:
        try:
            with open("zara.txt", "r", encoding='utf-8') as file:
                speak("Work we have to do today is " + file.read())
        except FileNotFoundError:
            speak("No tasks found yet.")

    elif "so work@" in request:
        try:
            with open("zara.txt", "r", encoding='utf-8') as file:
                task = file.read()
                notification.notify(title="Today's Work", message=task)
        except FileNotFoundError:
            speak("No tasks found to show.")

    elif "open@" in request:
        query = request.replace("open", "").strip()
        pyautogui.press("super")
        pyautogui.typewrite(query)
        pyautogui.sleep(2)
        pyautogui.press("enter")
        speak(f"Opening {query}")

    elif "wikipedia@" in request:
        q = request.replace("search wikipedia", "").replace("wikipedia", "").strip()
        if q:
            try:
                result = wikipedia.summary(q, sentences=2)
                speak(result)
            except Exception:
                speak("Couldn't fetch from Wikipedia. Try another query.")
        else:
            speak("Please tell me what to search on Wikipedia.")

    elif request.startswith("search "):
        q = request.replace("search", "").strip()
        if q:
            webbrowser.open("https://www.google.com/search?q=" + q)
            speak("Here are the Google results")
        else:
            speak("Please tell me what to search.")

    #elif request.startswith("zara"):
       # query = request.replace("zara", "").strip()
      #  if query:
           # answer = ask_gemini(query)
       #   #  speak(answer)
       # else:
           # speak("Please Zara ke liye koi sawal pucho.")"""

    elif request.startswith("image"):
        query = request.replace("image", "").strip()
        if query:
            speak("Image generate kar rahi hoon Alfaz...")
            ask_gemini_image(query)
        else:
            speak("Please image ke liye koi prompt batao.")

    elif "screenshot@" in request:
        if "center" in request:
            region = (600, 300, 700, 400)
            area = "center"
        elif "left" in request or "corner" in request:
            region = (0, 0, 500, 400)
            area = "top left corner"
        elif "right" in request:
            region = (1400, 0, 500, 400)
            area = "top right corner"
        else:
            region = (0, 0, 1920, 1080)
            area = "default region"
        now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{area.replace(' ', '_')}_screenshot_{now}.png"
        screenshot = pyautogui.screenshot(region=region)
        screenshot.save(filename)
        speak(f"{area} screenshot saved as {filename}")

    elif "click@" in request:
        button_name = request.replace("click", "").strip().lower()
        if button_name:
            speak(f"Trying to click on {button_name}")
            result = click_on_text(button_name)
            if result:
                speak(f"Clicked on {button_name}")
            else:
                speak(f"Could not find any button named {button_name}")
        else:
            speak("Please tell me which text to click on.")

    elif "close" in request:
        app_name = request.replace("close", "").strip()
        if app_name:
            close_application(app_name)
        else:
            speak("Please specify an app to close.")

    elif request in ["quit", "exit", "bye", "jarvish band karo", "stop jarvish"]:
        speak("Jarvish band ho raha hai. Bye!")
        os._exit(0)
    else:
        query = request.replace("zara", "").strip()
        if query:
            answer = ask_gemini(query)
            speak(answer)
        else:
            speak("Please Zara ke liye koi sawal pucho.")

# -------------------- VOICE MODE -------------------- #
def get_command_voice():
    recognizer = sr.Recognizer()
    mics = sr.Microphone.list_microphone_names()

    if not mics:
        print("❌ No microphone found. Please connect one.")
        return ""

    # Try opening mic safely
    try:
        with sr.Microphone() as source:
            #  print(f"🎤 Using default mic: {mics[0]}")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
    except OSError:
        try:
            print(f"⚠ Default mic failed. Using: {mics[0]}")
            with sr.Microphone(device_index=0) as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
        except Exception as e:
            print(f"❌ Could not access microphone: {e}")
            return ""
    except Exception as e:
        print(f"❌ Mic error: {e}")
        return ""

    # Recognize speech
    try:
        return recognizer.recognize_google(audio, language="en-IN")
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        print("⚠ Could not connect to Google Speech API")
        return ""




def voice_loop():
    while True:
        cmd = get_command_voice()
        if cmd:
            process_command(cmd)

# -------------------- START -------------------- #
if __name__ == "__main__":
    eel.start("zara.html", size=(1000, 1200))

<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Zara A.i</title>
  <link rel="shortcut icon" href="/frontend/assets/img/logo.ico" type="image/x-icon" />

  <!-- Bootsrap -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet"
    integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous" />
  <!-- Bootsrap Icons -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css" />

  <!-- Particle js -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/modernizr/2.8.3/modernizr.min.js" type="text/javascript"></script>

  <!-- Custom CSS -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css">

  <link rel="stylesheet" href="zara.css" />

</head>

<body>
  <script type="text/javascript">
    eel.expose(stopListening);
  </script>

  <div class="container">
    <section id="Start">
      <div class="row">
        <div class="col-lg-12">
          <div class="d-flex justify-content-center align-items-center" style="height: 80vh">
            <div>
              <div id="Loader" class="svg-frame mb-4">>
                <section id="Oval" class="mb-4">
                  <div id="live-text"></div>
                </section>


                <div class="row">
                  <div class="col-md-1"></div>
                  <div class="col-md-10">
                    <div class="d-flex justify-content-center align-items-center" style="height: 80vh">
                      <canvas id="canvasOne" width="700" height="820"></canvas>

                      <div id="JavisHood">
                        <div class="square">
                          <span class="circle"></span>
                          <span class="circle"></span>
                          <span class="circle"></span>
                        </div>
                      </div>
                    </div>
                    <h5 class="typewriter" data-text="I'm ZARA AI created by Alfaz Azmi" style="margin-left: 830px;color: aqua; margin-top: 40px;"></h5>
                    <h5 class="typewriter" data-text="Ask me Anything" style="margin-left: 900px; color:aliceblue" ></h5>



                    <div class="mt-4 pt-4" style="width: 800px; margin-left: 600px;">
                      <div>
                        <div id="TextInput" class="d-flex" style="margin-left: 100px;">
                          <textarea id="chatbox" name="chatbox" placeholder="Ask me anything..." class="input-field"
                            style="height:150px; width:100%; resize:none; padding-top:30px; box-sizing:border-box; line-height:1.5; font-size:16px; overflow-y:hidden;"></textarea>

                          <button id="MicBtn" onclick="startListening()" class="glow-on-hover">
                            <i class="bi bi-mic"></i>
                          </button>
                          <button id="ChatBtn" class="glow-on-hover" style="margin-left: 10px;">
                            <i class="bi bi-send-fill"></i>
                          </button>
                          <button id="SettingBtn" class="glow-on-hover">
                            <i class="bi bi-gear-wide-connected"></i>
                          </button>
                        </div>
                      </div>
                    </div>

                  </div>
                  <div class="col-md-1"></div>
                </div>
                <script>
                  let wave = null;

                  function startListening() {
                    // Python में voice mode शुरू करो
                    eel.start_voice_mode();

                    // SiriWave को दिखाओ
                    document.getElementById("SiriWave").removeAttribute("hidden");

                    // SiriWave एनिमेशन चालू करो
                    if (!wave) {
                      wave = new SiriWave({
                        container: document.getElementById("siri-container"),
                        width: 600,
                        height: 200,
                        style: "ios",
                        speed: 0.2,
                        amplitude: 1,
                        autostart: true,
                      });
                    } else {
                      wave.start(); // अगर पहले से है तो स्टार्ट करो
                    }
                  }
                </script>
                <script>
                  function stopListening() {
                    document.getElementById("SiriWave").setAttribute("hidden", true);
                    if (wave) {
                      wave.stop();
                    }
                  }
                </script>
                <script>
                  const elements = document.querySelectorAll('.typewriter');

                  elements.forEach((el) => {
                    const text = el.getAttribute('data-text');
                    let index = 0;

                    function type() {
                      if (index < text.length) {
                        el.textContent += text.charAt(index);
                        index++;
                        setTimeout(type, 100);
                      } else {
                        // Pause before repeating
                        setTimeout(() => {
                          el.textContent = '';
                          index = 0;
                          type();
                        }, 2000);
                      }
                    }

                    type(); // Start animation
                  });
                </script>





    </section>

    <div id="SiriWave" class="mb-4" hidden>
      <div class="container">
        <div class="row">
          <div class="col-md-12">
            <div class="d-flex justify-content-center align-items-center" style="height: 100vh">
              <div class="">
                <p class="text-start text-light mb-4 siri-message">
                  Hello, I am Your Assistant
                </p>
                <div id="siri-container"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>


  <script src="https://cdnjs.cloudflare.com/ajax/libs/FitText.js/1.2.0/jquery.fittext.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/lettering.js/0.7.0/jquery.lettering.min.js"></script>

  <!--Jquery  -->
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.4/jquery.min.js"></script>

  <!-- Bootstrap -->
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js"
    integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM"
    crossorigin="anonymous"></script>

  <!-- Particle js -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
  <script src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.11.2/jquery-ui.min.js"></script>
  <script src="zara.js"></script>

  <!-- Siri wave -->
  <script src="https://unpkg.com/siriwave/dist/siriwave.umd.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/siriwave/dist/siriwave.min.js"></script>

  <!-- Texllate js -->
  <script src="assets/vendore/texllate/jquery.fittext.js"></script>
  <script src="assets/vendore/texllate/jquery.lettering.js"></script>
  <script src="http://jschr.github.io/textillate/jquery.textillate.js"></script>

  <!-- lottie files -->
  <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
  <script src="https://unpkg.com/@dotlottie/player-component@2.7.12/dist/dotlottie-player.mjs" type="module"></script>

  <script src="main.js"></script>
  <script type="text/javascript" src="/eel.js"></script>
  <script src="controller.js"></script>

</body>

</html>


body {
  background-color: black;
  overflow-y: hidden;
  overflow-x: hidden;
}

#canvasOne {
  position: absolute;

  left: 280px;


}

.square {
  width: 400px;
  height: 400px;
  left: 400px;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;

}

.square span:nth-child(1) {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: radial-gradient(#6b72ff00 50%, #000dff3b 50%);
  box-shadow: 0 0 50px rgb(25, 25, 255), inset 0 0 50px rgb(25, 25, 255);
  border-radius: 30% 60% 63% 37%/40% 45% 58% 60%;
  transition: 0.4s;
  cursor: pointer;
  animation: animate1 6s infinite linear;
}

.square span:nth-child(2) {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: radial-gradient(#6b72ff00 50%, #000dff3b 50%);
  box-shadow: 0 0 50px rgb(25, 25, 255), inset 0 0 50px rgb(25, 25, 255);
  border-radius: 30% 60% 63% 37%/40% 45% 58% 60%;
  transition: 0.4s;
  cursor: pointer;
  animation: animate2 4s infinite linear;
}

.square span:nth-child(3) {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: radial-gradient(#6b72ff00 50%, #000dff3b 50%);
  box-shadow: 0 0 50px rgb(25, 25, 255), inset 0 0 50px rgb(25, 25, 255);
  border-radius: 30% 60% 63% 37%/40% 45% 58% 60%;
  transition: 0.4s;
  cursor: pointer;
  animation: animate3 8s infinite linear;
}


@keyframes animate1 {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

@keyframes animate2 {
  0% {
    transform: rotate(90deg);
  }

  100% {
    transform: rotate(270deg);
  }
}

@keyframes animate3 {
  0% {
    transform: rotate(180deg);
  }

  100% {
    transform: rotate(180deg);
  }
}




#TextInput {
  background-color: #181818a8;
  border-color: blue;
  box-shadow: 0 0 20px rgb(25, 25, 255),
    inset 0 0 0px rgb(255, 140, 0);
  border-radius: 8px;
  color: white;
  padding: 3px 0px 3px 20px;
  margin: 0px 20%;
}

.input-field {
  background-color: transparent;
  border: none;
  width: 95%;
  outline: none;
  color: white;
  font-family: cursive;
}


.glow-on-hover {
  width: 35px;
  height: 35px;
  border: none;
  outline: none;
  color: #fff;
  background: #111;
  cursor: pointer;
  position: relative;
  z-index: 0;
  border-radius: 10px;
  padding: 0px;
  margin-left: 10px;
}

.glow-on-hover:before {
  content: '';
  background: linear-gradient(45deg, #ff0000, #ff7300, #fffb00, #48ff00, #00ffd5, #002bff, #7a00ff, #ff00c8, #ff0000);
  position: absolute;
  top: -2px;
  left: -2px;
  background-size: 400%;
  z-index: -1;
  filter: blur(5px);
  width: calc(100% + 4px);
  height: calc(100% + 4px);
  animation: glowing 20s linear infinite;
  opacity: 0;
  transition: opacity .3s ease-in-out;
  border-radius: 10px;
}

.glow-on-hover:active {
  color: #181818a8
}

.glow-on-hover:active:after {
  background: transparent;
}

.glow-on-hover:hover:before {
  opacity: 1;
}

.glow-on-hover:after {
  z-index: -1;
  content: '';
  position: absolute;
  width: 100%;
  height: 100%;
  background: #111;
  left: 0;
  top: 0;
  border-radius: 10px;
}

@keyframes glowing {
  0% {
    background-position: 0 0;
  }

  50% {
    background-position: 400% 0;
  }

  100% {
    background-position: 0 0;
  }
}


.chat-canvas {
  background-color: #191919
}

.receiver_message {
  padding: 8px;
  border: 2px solid cyan;
  border-radius: 0px 15px 15px 20px;
  width: auto;
  color: white;
  background-color: #0dcaf014;
}

.sender_message {
  padding: 8px;
  border: 1px solid #0045ff;
  border-radius: 15px 15px 0px 20px;
  width: auto;
  color: white;
  background-color: #0045ff;
}

.width-size {
  max-width: 80%;
  width: auto;
}




.svg-frame {
  position: relative;
  width: 455px;
  height: 455px;
  transform-style: preserve-3d;
  display: flex;
  justify-content: center;
  align-items: center;
  animation: change-view 2s ease-in infinite;
}

@keyframes change-view {

  0%,
  50% {
    transform: rotate(-0deg) skew(00deg) translateX(calc(0 * var(--i))) translateY(calc(-0px * var(--i)));
  }

  70%,
  100% {
    transform: rotate(-80deg) skew(30deg) translateX(calc(45px * var(--i))) translateY(calc(-35px * var(--i)));
  }
}

svg {
  position: absolute;
  transition: 0.5s;
  transform-origin: center;
  width: 450px;
  height: 450px;
  fill: none;
  animation: change-view 5s ease-in-out infinite alternate;
  filter: drop-shadow(0 0 12px #00aaff);
}

#big-centro,
#outter1,
#solo-lines,
#center,
#outter-center,
#bottom-dots,
#center-lines,
#squares,
#top-dots {
  transform-origin: center;
  animation: rotate 4s ease-in-out infinite alternate;
}

#big-centro {
  animation-delay: -1.5s;
}

#outter1 {
  animation-delay: -1.2s;
}

#center {
  animation-delay: -2.2s;
}

#bottom-dots,
#top-dots {
  animation-duration: 7s;
}

#center-lines,
#outter-center {
  animation-duration: 6s;
  animation-delay: -3s;
}

@keyframes rotate {
  to {
    transform: rotate(360deg);
  }
}

#live-text {
  position: fixed;
  /* स्क्रीन पर हमेशा दिखेगा */
  top: -25%;
  right: 200px;
  /* बाईं तरफ से gap */
  width: 950px;
  height: 900px;
  padding: 25px;
  border-radius: 15px;
  background: rgba(0, 0, 0, 0);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(197, 30, 30, 0.2);
  box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.3);

  color: #ffffff;
  font-family: "Courier New", monospace;
  font-size: 16.5px;
  line-height: 1.8;
  overflow-y: auto;
  white-space: normal;
  word-wrap: break-word;
  /* टेक्स्ट left aligned */
  z-index: 999;
}

#live-text p {
  margin-bottom: 15px;
}

/* Bold, Italic, Code */
#live-text strong {
  font-weight: bold;
}
#live-text em {
  font-style: italic;
}
#live-text code {
  background: rgba(255, 255, 255, 0.1);
  padding: 3px 6px;
  border-radius: 5px;
  font-family: monospace;
  color: #00ffcc;
}

/* Code blocks */
#live-text pre {
  background: rgba(255, 255, 255, 0.05);
  padding: 12px 16px;
  border-radius: 10px;
  overflow-x: auto;
  font-family: 'Courier New', monospace;
  color: #00ffd0;
  margin-bottom: 15px;
}

/* Headings */
#live-text h1, #live-text h2, #live-text h3 {
  color: #00ffe1;
  margin-top: 20px;
  margin-bottom: 10px;
  font-weight: bold;
}

#live-text h1 { font-size: 24px; }
#live-text h2 { font-size: 20px; }
#live-text h3 { font-size: 18px; }

/* Scrollbar */
#live-text::-webkit-scrollbar {
  width: 8px;
}
#live-text::-webkit-scrollbar-thumb {
  background: #00ffcc;
  border-radius: 10px;
}
#live-text::-webkit-scrollbar-track {
  background: transparent;
}


