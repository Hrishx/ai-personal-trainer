import pyttsx3
import threading


class VoiceCoach:

    def __init__(self):

        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 170)
        self.engine.setProperty("volume", 1)

        self.lock = threading.Lock()
        self.speaking = False

    def speak(self, text):

        def run():

            with self.lock:

                self.speaking = True

                try:
                    self.engine.say(text)
                    self.engine.runAndWait()
                except:
                    pass

                self.speaking = False

        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()

    def is_speaking(self):

        
        return self.speaking