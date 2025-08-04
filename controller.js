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

# -------------------- CONFIG -------------------- #
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
INPUT_MODE = "voice"
last_search_query = ""

# -------------------- GEMINI API -------------------- #
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
client_gemini = genai.Client(api_key=GEMINI_API_KEY)

# -------------------- INIT EEL -------------------- #
eel.init("web")  # zara.html folder

# -------------------- SPEAK FUNCTION -------------------- #
def speak(audio: str):
    print("ZARA:", audio)
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    try:
        engine.setProperty('voice', voices[2].id)
    except Exception:
        pass
    engine.setProperty("rate", 170)
    engine.say(audio)
    engine.runAndWait()

# -------------------- GEMINI TEXT -------------------- #
def ask_gemini(question: str) -> str:
    try:
        response = client_gemini.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Answer in max 150 words without markdown:\n{question}",
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=0)
            ),
        )
        answer = response.text or ""
        clean_answer = re.sub(r"\*\*|[`#*_]", "", answer)
        clean_answer = re.sub(r"\s+", " ", clean_answer).strip()
        return clean_answer
    except Exception as e:
        return f"Gemini error: {e}"

# -------------------- GEMINI IMAGE -------------------- #
def ask_gemini_image(prompt: str):
    try:
        response = client_gemini.models.generate_content(
            model="gemini-2.0-flash-preview-image-generation",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE']
            )
        )
        for part in response.candidates[0].content.parts:
            if getattr(part, "inline_data", None):
                image = Image.open(BytesIO(part.inline_data.data))
                filename = "zara_image.png"
                image.save(filename)
                image.show()
                speak(f"Image saved as {filename}")
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

    # ---- Basic Greetings ---- #
    if "hi" in request:
        speak("Welcome, Alfaaz how can I help you.")

    elif "banaya" in request:
        speak("I have been made by a BCA group which includes Alfaaz, SATYAM, Himanshu, Deepak, Akash")

    elif "whatsapp" in request and "bolo" in request:
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

    elif "play music" in request:
        speak("Playing music")
        webbrowser.open("https://www.youtube.com/watch?v=8of5w7RgcTc&list=RD8of5w7RgcTc&start_radio=1")

    elif "open youtube" in request:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "search" in request and "youtube" in request:
        last_search_query = request.replace("search", "").replace("on youtube", "").strip()
        speak(f"Searching {last_search_query} on YouTube")
        webbrowser.open(f"https://www.youtube.com/results?search_query={last_search_query}")
        speak("Here are the results. Say 'play first video' to start.")

    elif "play first video" in request and last_search_query:
        speak(f"Playing {last_search_query}")
        pywhatkit.playonyt(last_search_query)

    elif "stop" in request or "play" in request:
        pyautogui.press("k")
        speak("Toggled play and pause")

    elif "full screen" in request:
        pyautogui.press("f")
        speak("Fullscreen enabled")

    elif "half screen" in request:
        pyautogui.press("f")
        speak("Half screen enabled")

    elif "mute" in request:
        pyautogui.press("m")
        speak("Mute toggled")

    elif "change" in request:
        pyautogui.hotkey("shift", "n")
        speak("Next video playing")

    elif "open instagram" in request:
        speak("Opening Instagram")
        webbrowser.open("https://www.instagram.com")

    elif "time" in request:
        now_time = datetime.datetime.now().strftime("%H:%M")
        speak("Current time is " + str(now_time))

    elif "date" in request:
        now_date = datetime.datetime.now().strftime("%d:%m")
        speak("Current date is " + str(now_date))

    elif "new work" in request:
        task = request.replace("new task", "").strip()
        if task:
            speak("Adding task: " + task)
            with open("zara.txt", "a", encoding='utf-8') as file:
                file.write(task + "\n")

    elif "speak task" in request:
        try:
            with open("zara.txt", "r", encoding='utf-8') as file:
                speak("Work we have to do today is " + file.read())
        except FileNotFoundError:
            speak("No tasks found yet.")

    elif "so work" in request:
        try:
            with open("zara.txt", "r", encoding='utf-8') as file:
                task = file.read()
                notification.notify(title="Today's Work", message=task)
        except FileNotFoundError:
            speak("No tasks found to show.")

    elif "open" in request:
        query = request.replace("open", "").strip()
        pyautogui.press("super")
        pyautogui.typewrite(query)
        pyautogui.sleep(2)
        pyautogui.press("enter")
        speak(f"Opening {query}")

    elif "wikipedia" in request:
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

    elif request.startswith("zara"):
        query = request.replace("zara", "").strip()
        if query:
            speak("Alfaz, please wait...")
            answer = ask_gemini(query)
            speak(answer)
        else:
            speak("Please Zara ke liye koi sawal pucho.")

    elif request.startswith("image"):
        query = request.replace("image", "").strip()
        if query:
            speak("Image generate kar rahi hoon Alfaz...")
            ask_gemini_image(query)
        else:
            speak("Please image ke liye koi prompt batao.")

    elif "screenshot" in request:
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

    elif "click" in request:
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
        speak("Yeh command mujhe nahi mila hai")

# -------------------- VOICE MODE -------------------- #
def get_command_voice() -> str:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        speak("I am listening")
        try:
            audio = r.listen(source, phrase_time_limit=4)
            content = r.recognize_google(audio, language='en-IN')
            print("You said:", content)
            return content
        except:
            return ""

def voice_loop():
    while True:
        cmd = get_command_voice()
        if cmd:
            process_command(cmd)

# -------------------- START -------------------- #
if __name__ == "__main__":
    import threading
    threading.Thread(target=voice_loop, daemon=True).start()
    eel.start("zara.html", size=(1000, 1200))



$(document).ready(function () {

    var siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        width: 640,
        style: "ios9",
        amplitude: 1,
        speed: 0.3,
        height: 200,
        autostart: false
    });

    let audioContext, analyser, microphone, dataArray;

    // Start mic amplitude analyser
    async function startAmplitudeTracker() {
        try {
            audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true, video: false });
            microphone = audioContext.createMediaStreamSource(stream);
            analyser = audioContext.createAnalyser();
            analyser.fftSize = 256;
            dataArray = new Uint8Array(analyser.frequencyBinCount);

            microphone.connect(analyser);

            function updateAmplitude() {
                analyser.getByteTimeDomainData(dataArray);
                let sum = 0;
                for (let i = 0; i < dataArray.length; i++) {
                    sum += Math.abs(dataArray[i] - 128);
                }
                let avg = sum / dataArray.length;
                siriWave.setAmplitude(Math.min(avg / 5, 5)); // limit amplitude
                requestAnimationFrame(updateAmplitude);
            }
            updateAmplitude();

        } catch (err) {
            console.error("Mic error for amplitude tracking:", err);
        }
    }

    function startListening() {
        if (!('webkitSpeechRecognition' in window)) {
            alert("Speech Recognition API is not supported in this browser. Use Chrome or Edge.");
            return;
        }

        const recognition = new webkitSpeechRecognition();
        recognition.lang = "hi-IN";  // Change to en-IN for English
        recognition.interimResults = true;
        recognition.continuous = true;

        $(".siri-message").text("🎤 Listening...");
        siriWave.start();
        startAmplitudeTracker();

        let finalTranscript = "";
        let lastSpokenTime = Date.now();

        recognition.onresult = function (event) {
            let interimTranscript = "";
            for (let i = event.resultIndex; i < event.results.length; ++i) {
                if (event.results[i].isFinal) {
                    finalTranscript += event.results[i][0].transcript + " ";
                    lastSpokenTime = Date.now();
                } else {
                    interimTranscript += event.results[i][0].transcript;
                    lastSpokenTime = Date.now();
                }
            }
            $(".siri-message").text(interimTranscript || finalTranscript);
        };

        recognition.onerror = function (event) {
            $(".siri-message").text("⚠ Mic error: " + event.error);
            siriWave.stop();
        };

        recognition.onend = function () {
            siriWave.stop();
            if (finalTranscript.trim() === "") {
                $(".siri-message").text("❌ No voice detected");
            } else {
                $(".siri-message").text("✅ You said: " + finalTranscript);
                eel.process_command(finalTranscript);
            }
        };

        recognition.start();

        const silenceCheck = setInterval(() => {
            if (Date.now() - lastSpokenTime > 3000) {
                recognition.stop();
                clearInterval(silenceCheck);
            }
        }, 500);
    }

    // Mic Button Click
    $("#MicBtn").click(function () {
        $("#Oval").attr("hidden", true);
        $("#SiriWave").attr("hidden", false);
        startListening();
    });

});




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
  <link rel="stylesheet" href="assets/vendore/texllate/animate.css" />
  <link rel="stylesheet" href="zara.css" />
</head>

<body>
  <div class="container">
    <section id="Start">
      <div class="row">
        <div class="col-lg-12">
          <div class="d-flex justify-content-center align-items-center" style="height: 80vh">
            <div>
              <div id="Loader" class="svg-frame mb-4">>
                <section id="Oval" class="mb-4">
                  <div class="row">
                    <div class="col-md-1"></div>
                    <div class="col-md-10">
                      <div class="d-flex justify-content-center align-items-center" style="height: 80vh">
                        <canvas id="canvasOne" width="700" height="420" style="position: absolute"></canvas>
                        <div id="JarvisHood">
                          <div class="square">
                            <span class="circle"></span>
                            <span class="circle"></span>
                            <span class="circle"></span>
                          </div>
                        </div>
                      </div>
                      <h4 class="text-light text-center">Ask me Anything</h4>>

                      <div class="col-md-12 mt-4 pt-4">
                        <div class="text-center">
                          <div id="TextInput" class="d-flex">
                            <input type="text" id="chatbox" name="chatbox" placeholder="Ask me anything..."
                              class="input-field" />
                            <button id="MicBtn" class="glow-on-hover">
                              <i class="bi bi-mic"></i>
                            </button>
                            <button id="ChatBtn" class="glow-on-hover">
                              <i class="bi bi-chat-dots"></i>
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
              <script type="text/javascript" src="/eel.js"></script>
              <script type="text/javascript" src="/eel.js"></script>
              <script>
                // Chat button पर click event
                document.getElementById("ChatBtn").addEventListener("click", function () {
                  let text = document.getElementById("chatbox").value;
                  if (text.trim() !== "") {
                    eel.process_command(text);
                    document.getElementById("chatbox").value = "";
                  }
                });

                // Python से reply आने पर HTML में show करना
                eel.expose(show_reply);
                function show_reply(user_text, reply) {
                  let chatArea = document.getElementById("chat-area");

                  // User message
                  let userMsg = document.createElement("div");
                  userMsg.style.textAlign = "right";
                  userMsg.innerHTML = `<b>You:</b> ${user_text}`;
                  chatArea.appendChild(userMsg);

                  // Zara reply
                  let botMsg = document.createElement("div");
                  botMsg.style.textAlign = "left";
                  botMsg.innerHTML = `<b>Zara:</b> ${reply}`;
                  chatArea.appendChild(botMsg);

                  chatArea.scrollTop = chatArea.scrollHeight; // Auto-scroll
                }
              </script>



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

              <!-- Texllate js -->
              <script src="assets/vendore/texllate/jquery.fittext.js"></script>
              <script src="assets/vendore/texllate/jquery.lettering.js"></script>
              <script src="http://jschr.github.io/textillate/jquery.textillate.js"></script>

              <!-- lottie files -->
              <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
              <script src="https://unpkg.com/@dotlottie/player-component@2.7.12/dist/dotlottie-player.mjs"
                type="module"></script>

              <script src="main.js"></script>
              <script type="text/javascript" src="/eel.js"></script>
              <script src="controller.js"></script>

</body>

</html>




