import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import client
import requests
import time
from difflib import get_close_matches

# pip install pocketsphinx

recognizer = sr.Recognizer()

newsapi = "54ee3e0b234d4919bccb2263f9dc2e20"


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()


def normalize_text(text):
    """
    Convert text into a clean format.
    This helps with spaces and capital/small letters.
    """

    text = str(text).lower().strip()

    # Remove extra spaces
    text = " ".join(text.split())

    return text


def find_song(song):

    # Normalize the song requested by the user
    song = normalize_text(song)

    print("Requested song:", song)

    # Store normalized song names
    song_names = {}

    for name in musiclibrary.music:

        clean_name = normalize_text(name)

        song_names[clean_name] = name

    # -----------------------------------------
    # First try: Exact match
    # -----------------------------------------

    if song in song_names:

        original_name = song_names[song]

        print("Exact match found:", original_name)

        return musiclibrary.music[original_name], original_name

    # -----------------------------------------
    # Second try: Fuzzy match
    # -----------------------------------------

    close_matches = get_close_matches(
        song,
        song_names.keys(),
        n=1,
        cutoff=0.55
    )

    if close_matches:

        matched_song = close_matches[0]

        original_name = song_names[matched_song]

        print("Fuzzy match found:", original_name)

        return musiclibrary.music[original_name], original_name

    # -----------------------------------------
    # Song not found
    # -----------------------------------------

    return None, None


def processCommand(c):

    # Convert command into lowercase
    command = normalize_text(c)

    print("Processing command:", command)

    # -----------------------------------------
    # Open Google
    # -----------------------------------------

    if "open google" in command:

        print("Opening Google")

        speak("Opening Google")

        webbrowser.open("https://google.com")

    # -----------------------------------------
    # Open Facebook
    # -----------------------------------------

    elif "open facebook" in command:

        print("Opening Facebook")

        speak("Opening Facebook")

        webbrowser.open("https://facebook.com")

    # -----------------------------------------
    # Open YouTube
    # -----------------------------------------

    elif "open youtube" in command:

        print("Opening YouTube")

        speak("Opening YouTube")

        webbrowser.open("https://youtube.com")

    # -----------------------------------------
    # Open LinkedIn
    # -----------------------------------------

    elif "open linkedin" in command:

        print("Opening LinkedIn")

        speak("Opening LinkedIn")

        webbrowser.open("https://linkedin.com")

    # -----------------------------------------
    # Play music
    # -----------------------------------------

    elif command.startswith("play"):

        # Remove the word "play"
        song = command[4:].strip()

        # Check if user actually gave a song name
        if not song:

            speak("Please tell me the song name")

            return

        # Find the song
        link, song_name = find_song(song)

        # -----------------------------------------
        # If song is found
        # -----------------------------------------

        if link:

            print("Playing:", song_name)

            speak("Playing " + str(song_name))

            webbrowser.open(link)

        # -----------------------------------------
        # If song is not found
        # -----------------------------------------

        else:

            print("Song not found:", song)

            print("Available songs:")

            for name in musiclibrary.music:

                print("-", name)

            speak("Sorry, I could not find that song")

    # -----------------------------------------
    # News command
    # -----------------------------------------

    elif "news" in command:

        print("News command received")

        # Tell the user that Jarvis is fetching the news
        speak("I am fetching the news")

        try:

            # Get the latest news from NewsAPI
            r = requests.get(
                f"https://newsapi.org/v2/everything?q=news&language=en&sortBy=publishedAt&pageSize=5&apiKey={newsapi}",
                timeout=10
            )

            # Print the status code
            print("Status Code:", r.status_code)

            if r.status_code == 200:

                # Parse the JSON response
                data = r.json()

                # Extract the articles
                articles = data.get("articles", [])

                # Print the number of articles
                print("Number of articles:", len(articles))

                # Check if articles are available
                if articles:

                    # Tell the user that news is available
                    speak("Here are the latest news headlines")

                    # Print and speak the headlines
                    for article in articles:

                        # Extract the title
                        title = article.get("title")

                        # Check if title exists
                        if title:

                            print(title)

                            speak(title)

                else:

                    # If no articles are found
                    speak("No news found")

            else:

                # Print the error details
                print("News API Error:")
                print(r.text)

                # Tell the user that news could not be fetched
                speak("There is a problem with the news API")

        except requests.exceptions.RequestException as e:

            print("News request error:", e)

            speak("I could not connect to the news service")

    # -----------------------------------------
    # Ollama AI
    # -----------------------------------------

    else:

        print("Sending command to Ollama...")

        answer = client.ask_ollama(command)

        print("Ollama:", answer)

        speak(answer)


if __name__ == "__main__":

    speak("Initializing Hello....")

    while True:

        # -----------------------------------------
        # Wake word recognizer
        # -----------------------------------------

        wake_recognizer = sr.Recognizer()

        # Wake word recognition settings
        wake_recognizer.energy_threshold = 250
        wake_recognizer.dynamic_energy_threshold = True

        wake_recognizer.pause_threshold = 0.8
        wake_recognizer.phrase_threshold = 0.1
        wake_recognizer.non_speaking_duration = 0.3

        print("\n-----------------------------")
        print("Waiting for wake word...")
        print("-----------------------------")

        try:

            with sr.Microphone() as source:

                print("Listening for 'hello'...")

                # Adjust microphone for background noise
                wake_recognizer.adjust_for_ambient_noise(
                    source,
                    duration=0.5
                )

                audio = wake_recognizer.listen(
                    source,
                    timeout=10,
                    phrase_time_limit=5
                )

            # Recognize wake word
            word = wake_recognizer.recognize_google(
                audio,
                language="en-IN"
            )

            print("You said:", word)

            # Check wake word
            if "hello" in word.lower():

                speak("Ya")

                # Wait until voice output is completely finished
                time.sleep(1.5)

                # -----------------------------------------
                # Command recognizer
                # -----------------------------------------

                command_recognizer = sr.Recognizer()

                # Command recognition settings
                command_recognizer.energy_threshold = 250
                command_recognizer.dynamic_energy_threshold = True

                # Give more time before deciding
                # that the user has stopped speaking
                command_recognizer.pause_threshold = 2

                command_recognizer.phrase_threshold = 0.2
                command_recognizer.non_speaking_duration = 0.5

                try:

                    with sr.Microphone() as source:

                        print("\nhello active...")
                        print("Adjusting microphone...")

                        # Adjust microphone for background noise
                        command_recognizer.adjust_for_ambient_noise(
                            source,
                            duration=0.7
                        )

                        print("Speak your command...")

                        # Listen for command
                        audio = command_recognizer.listen(
                            source,
                            timeout=10,
                            phrase_time_limit=15
                        )

                    # Recognize command
                    command = command_recognizer.recognize_google(
                        audio,
                        language="en-IN"
                    )

                    print("Command:", command)

                    # Process command
                    processCommand(command)

                except sr.UnknownValueError:

                    print("Could not understand command")

                    speak(
                        "Sorry, I did not understand. Please try again."
                    )

                except sr.WaitTimeoutError:

                    print("Command listening timed out")

                    speak("I did not hear a command")

                except sr.RequestError as e:

                    print(
                        "Google Speech Recognition error:",
                        e
                    )

                    speak(
                        "Speech recognition service is not available"
                    )

                except Exception as e:

                    print("Command Error:", e)

        except sr.UnknownValueError:

            print("Could not understand audio")

        except sr.WaitTimeoutError:

            print("Listening timed out")

        except sr.RequestError as e:

            print(
                "Google Speech Recognition error:",
                e
            )

        except Exception as e:

            print("Error:", e)