import csv
import datetime
import pyttsx3
import speech_recognition as sr
import tkinter as tk
from tkinter import messagebox

from main import intro, wish, main

# ... (existing code up to main)

# Create a tkinter window
window = tk.Tk()
window.title("ATM System for the Visually Impaired")
window.geometry("400x300")

# Create a label for displaying messages
message_label = tk.Label(window, text="", wraplength=300)
message_label.pack()


# Create a function to update the message label
def update_message(message):
    message_label.config(text=message)


# Create a function to get user input using tkinter Entry widget
user_input = tk.Entry(window)
user_input.pack()


def get_user_input():
    return user_input.get()


# ... (other existing functions)

# Modify the inputCommand function to use tkinter
def inputCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        update_message("Listening...")
        window.update()
        audio = r.listen(source)

    try:
        update_message("Recognizing...")
        window.update()
        said = r.recognize_google(audio, language="en-in")
        update_message(f"You said: {said}")
        window.update()
    except Exception as e:
        print(e)
        update_message("Can you please say that again...")
        window.update()
        said = "Sorry, I did not understand that!"
    return said


# Modify the main function to display messages and get user inputs in the GUI
def entry():
    intro()
    wish()
    main()

    # ... (rest of your existing code)


# Add a button to start the ATM system
start_button = tk.Button(window, text="Start ATM System", command=entry)
start_button.pack()

# Run the tkinter main loop
window.mainloop()
