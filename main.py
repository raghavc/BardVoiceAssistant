from Bard import Chatbot
from playsound import playsound
import speech_recognition as sr
from os import system
import time
import whisper
import warnings
import sys

token = 'Enter Token'
tokents = 'Enter Tokents'
Chatbot = Chatbot(token,tokents)
r = sr.Recognizer()

tiny_model = whisper.load_model('tiny_model')
base_model = whisper.load_model('base_model')
warnings.filterwarnings("ignore",message="FP16 is not supported on CPU, use FP32 instead") 
#Windows & Linux Machines 
if sys.platform != 'darwin':
    import pyttsx3
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-50)

def prompt_bard(prompt):
    response = Chatbot.ask(prompt)
    return response['content']



def speak(text):
    if sys.platform == 'darwin':
        ALLOWED_CHARS = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-,.!? ')
        clean_text = ''.join(c for c in text if c in ALLOWED_CHARS)
        system(f'say "{clean_text}"')
    else:
        engine.say(text)
        engine.runAndWait()

def main():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        while True:
            while True:
                try: 
                    print('\n Say "Bard" to activate the chatbot')
                    audio = r.listen(source)
                    with open("wake_detect.wav", wb ) as f:
                        f.write(audio.get_wav_data())
                        result = whisper.predict(audio, tiny_model)
                        text_input = result['text']
                        if ('bard' in text_input.lower().strip()):
                            speak('Bard Activated')
                            break
                        else:
                            print('Try again')
                except Exception as e:
                    print("Error",e)
                    continue
                try:
                    playsound('wake_detect.mp3')
                    print('Confirmation Recived')
                    time.sleep(1)
                    print('Listening')
                    audio = r.listen(source)
                    with open ("prompt.wav", "wb") as f:
                        f.write(audio.get_wav_data())
                        result = whisper.predict(audio, base_model)
                        text_input = result['text']
                        print("Sending Data to Bard API" + " " + text_input + " ")
                        time.sleep(1)
                        if (len(text_input) == 0):
                            print("No Input Try Again")
                            speak("No Input Try Again")
                            continue
                except Exception as e:
                    print("Error Transcribing Audio ",e)
                    continue
                response = prompt_bard(text_input)
                if (sys.platform.startswith('win')):
                    print("Bard: " + response)
                else:
                   print("\033[31m" + 'Bards Response: ', response, '\n' + "\033[0m")
                speak(response)
main()
                      




        
