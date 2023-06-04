import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import speech_recognition as sr
from pygame import mixer
from pywin.framework.editor import frame


def recognize_file():
    pass


def save_file():
    pass


def select_file():
    pass


root = tk.Tk()
root.title("Speech Recognition")

text_widget = tk.Text(font=("Arial", 15))
text_widget.grid(column=0, row=0)

button_frame = tk.Frame()
button_frame.grid(column=0, row=1)

recognize_button = ttk.Button(button_frame, text="Recognize", command=recognize_file)
save_button = ttk.Button(button_frame, text="Save As", command=save_file)

recognize_button.grid(column=0, row=0)
save_button.grid(column=1, row=0)

root.mainloop()
