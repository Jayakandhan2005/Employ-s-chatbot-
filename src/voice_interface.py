import speech_recognition as sr
import pyttsx3

class VoiceInterface:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()

    def listen(self):
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.recognizer.listen(source)
            try:
                text = self.recognizer.recognize_google(audio)
                return text
            except sr.UnknownValueError:
                return "Sorry, I couldn't understand that."
            except sr.RequestError:
                return "Sorry, there was an error processing your request."

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()