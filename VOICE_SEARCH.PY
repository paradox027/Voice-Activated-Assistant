import os
import speech_recognition as sr
import pyttsx3
import webbrowser
import time

def speak(text):
    """Convert text to speech."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def find_file(filename):
    """Search for a file across all drives and open it if found."""
    # List of root directories (e.g., drives on your system)
    root_dirs = ["D:/", "E:/"]
    for drive in root_dirs:
        for root, dirs, files in os.walk(drive):
            if filename in files:
                file_path = os.path.join(root, filename)
                return file_path
    return None


def perform_action(query, recognizer, source):
    """Perform actions based on the query."""
    if "search file" in query:
        speak("Which file do you want to search for?")
        print("Listening for file name...")
        file_audio = recognizer.listen(source)
        try:
            file_name = recognizer.recognize_google(file_audio).lower()
            repla_dot = file_name.replace(" dot ",".")
            file_name_with_extension = f"{repla_dot}"  # Take exact input as file name
            print("Searching for",file_name_with_extension)
            speak("Searching for the file across your system. This might take some time.")
            file_path = find_file(file_name_with_extension)
            if file_path:
                speak(f"File found: {file_path}")
                print(f"Opening file: {file_path}")
                os.startfile(file_path)
            else:
                speak("File not found.")
                print("File not found.")
        except sr.UnknownValueError:
            speak("I couldn't understand the file name.")
        except sr.RequestError:
            speak("Error in processing the file search request.")

    elif "search on youtube" in query:
        speak("What would you like to search for on YouTube?")
        print("Listening for YouTube search...")
        yt_audio = recognizer.listen(source)
        try:
            yt_query = recognizer.recognize_google(yt_audio).lower()
            speak(f"Searching YouTube for {yt_query}")
            webbrowser.open(f"https://www.youtube.com/results?search_query={yt_query}")
            print(f"Opening YouTube search for: {yt_query}")
        except sr.UnknownValueError:
            speak("I couldn't understand your YouTube query.")
        except sr.RequestError:
            speak("Error in processing the YouTube search request.")

    elif "search on google" in query:
        speak("What would you like to search for on Google?")
        print("Listening for Google search...")
        google_audio = recognizer.listen(source)
        try:
            google_query = recognizer.recognize_google(google_audio).lower()
            speak(f"Searching Google for {google_query}")
            webbrowser.open(f"https://www.google.com/search?q={google_query}")
            print(f"Opening Google search for: {google_query}")
        except sr.UnknownValueError:
            speak("I couldn't understand your Google query.")
        except sr.RequestError:
            speak("Error in processing the Google search request.")

    else:
        speak("Command not recognized. Try saying 'search file', 'search on YouTube', or 'search on Google'.")

def voice_search_loop():
    """Main loop for the voice search with sleep mode."""
    recognizer = sr.Recognizer()
    speak("Voice search system is now active. Say 'wake up' to start or 'exit' to terminate.")

    while True:
        with sr.Microphone() as source:
            try:
                print("Listening for wake-up command...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
                wake_up_command = recognizer.recognize_google(audio).lower()

                if "wake up" in wake_up_command:
                    speak("I'm listening. What would you like to do?")
                    print("Listening for your query...")
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source)
                    query = recognizer.recognize_google(audio).lower()
                    perform_action(query, recognizer, source)

                elif "exit" in wake_up_command:
                    speak("Goodbye!")
                    print("Exiting the program...")
                    break

                else:
                    print("System is in sleep mode. Say 'wake up' to activate.")
                    time.sleep(2)

            except sr.UnknownValueError:
                print("No recognizable input. System remains in sleep mode.")
            except sr.RequestError:
                speak("Error in processing the request. Check your internet connection.")

if __name__ == "__main__":
    voice_search_loop()
