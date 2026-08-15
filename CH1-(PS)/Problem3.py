# install an external module and use it to perform an operation of your interest
# pyttsx(python text to speech)-module use
import pyttsx3
engine = pyttsx3.init()

# For Mac, If you face error related to "pyobjc" when running the `init()` method :
# Install 9.0.1 version of pyobjc : "pip install pyobjc>=9.0.1"

engine.say("Aniket is a student of computer science department")
engine.runAndWait()