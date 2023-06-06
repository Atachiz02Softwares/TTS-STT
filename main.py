import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import speech_recognition as sr
from pygame import mixer

r = sr.Recognizer()

mixer.init()


def recognize_file():
    with sr.Microphone() as source:
        audio = r.listen(source)

    try:
        text_widget.delete("0.0", "end")
        # Performs speech recognition on audio_data (an AudioData instance), using the Google Speech Recognition
        # API.
        text = r.recognize_google(audio)
        text_widget.insert("0.0", f"{text}")

    except sr.UnknownValueError:
        text_widget.insert("0.0", "Couldn't recognize the audio file...")

    except sr.RequestError as error:
        text_widget.insert("0.0", f"{error}")


def open_file():
    f = select_file()

    mixer.music.load(f)
    mixer.music.play()

    with sr.AudioFile(f) as source:
        audio = r.record(source)

    try:
        text_widget.delete("0.0", "end")
        # Performs speech recognition on audio_data (an AudioData instance), using the Google Speech Recognition
        # API.
        text = r.recognize_google(audio)
        text_widget.insert("0.0", text)

    except sr.UnknownValueError:
        print("Couldn't recognize the audio file")

    except sr.RequestError as error:
        print(error)


def save_file():
    f = select_file()

    with open(f, "w") as file:
        file.write(text_widget.get("0.0", "end"))


def select_file():
    file_path = filedialog.askopenfilename(title="Select file")
    return file_path


root = tk.Tk()
root.title("Speech Recognition")

text_widget = tk.Text(font=("Arial", 15))
text_widget.grid(column=0, row=0)

button_frame = tk.Frame()
button_frame.grid(column=0, row=1)

open_button = ttk.Button(button_frame, text="Open", command=open_file)
recognize_button = ttk.Button(button_frame, text="Recognize", command=recognize_file)
save_button = ttk.Button(button_frame, text="Save", command=save_file)

open_button.grid(column=0, row=0)
recognize_button.grid(column=1, row=0)
save_button.grid(column=2, row=0)

root.mainloop()
