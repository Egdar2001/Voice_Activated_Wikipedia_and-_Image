import threading
import tkinter as tk
from PIL import Image, ImageTk
import speech_recognition as sr
import pyttsx3
import wikipedia


# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1.0)  # Volume level

def speak(text):
    """Function to convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def display_logo():
    """Function to create and display a persistent logo window."""
    root = tk.Tk()
    root.title("Edgar Assistant")
    root.geometry("400x400")  # Adjust size as needed

    # Load and display the logo
    logo = Image.open("C:\\Users\\Joseph Varghese\\Desktop\\code\\Voice Activated\\edgar_logo.png")
    logo = logo.resize((300, 300), Image.Resampling.LANCZOS)
    logo_tk = ImageTk.PhotoImage(logo)

    label = tk.Label(root, image=logo_tk)
    label.pack(pady=20)

    # Add a title
    title = tk.Label(root, text="Edgar is Active!", font=("Arial", 16))
    title.pack()

    # Prevent window from blocking the main thread
    root.mainloop()

def listen_for_query():
    """Listen for the user's query."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("I'm listening. What do you want to know?")
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            query = recognizer.recognize_google(audio).lower()
            return query
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that.")
            return ""
        except sr.WaitTimeoutError:
            speak("You took too long to respond.")
            return ""

def search_wikipedia(query):
    """Search Wikipedia for a given query."""
    try:
        summary = wikipedia.summary(query, sentences=2)
        return summary
    except wikipedia.DisambiguationError:
        return "Your query is ambiguous. Please be more specific."
    except wikipedia.PageError:
        return "I couldn't find anything on that topic."
    except Exception as e:
        return f"An error occurred: {str(e)}"

def main():
    """Main function for Edgar."""
    speak("Hello, I am Edgar, your voice assistant. I am ready to assist you.")
    while True:
        query = listen_for_query()
        if query:
            if "exit" in query or "stop" in query:
                speak("Goodbye!")
                break
            else:
                result = search_wikipedia(query)
                speak(result)

# Run the GUI in a separate thread
threading.Thread(target=display_logo, daemon=True).start()

# Run the main function
if __name__ == "__main__":
    main()
