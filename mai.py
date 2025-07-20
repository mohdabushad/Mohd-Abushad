import os
import eel
eel.init("www")
os.system('start msedge.exe --app="http://127.0.0.1:3000/jarvish.html"')
eel.start('jarvish.html', mode=None, host='localhost', block=True)
'''
from engine.features import *
from engine.command import *
from engine.auth import recoganize'''
def start():
    
    eel.init("www")

    playAssistantSound()
    @eel.expose
    def init():
        subprocess.call([r'device.bat'])
        eel.hideLoader()
        speak("Ready for Face Authentication")
        flag = recoganize.AuthenticateFace()
        if flag == 1:
            eel.hideFaceAuth()
            speak("Face Authentication Successful")
            eel.hideFaceAuthSuccess()
            speak("Hello, Welcome Sir, How can i Help You")
            eel.hideStart()
            playAssistantSound()
        else:
            speak("Face Authentication Fail")
