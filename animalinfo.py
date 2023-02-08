# animalinfo - Displays information about an animal recognized
# with Machine Learning for Kids

# Required dependencies
import os
import tkinter as tk
import tkinter.font as TkFont
import wikipediaapi

from dotenv import load_dotenv
from mlforkids import MLforKidsImageProject
from PIL import ImageTk
from tkinter import filedialog
from tkinter import scrolledtext

# Loads the API key from the .env file
load_dotenv()
key = os.getenv("API_KEY")

# Trains the ML model to recognize images
detector = MLforKidsImageProject(key)
detector.train_model()

# Creates the window
window = tk.Tk()
window.title("Animal Info")
window.resizable(False, False)

# Fonts
titleFont = TkFont.Font(family = "helvetica", size = 36, weight = "bold")
animalFont = TkFont.Font(family = "helvetica", size = 20, weight = "bold")
descFont = TkFont.Font(family = "helvetica", size = 14)

titleLabel = tk.Label(window, text = "Animal Info", font = titleFont)
titleLabel.grid(row = 1, column = 1)
button = tk.Button(window, text = "Choose an image", command = lambda:recognize_image())
button.grid(row = 2, column = 1, pady = 5)

# Chooses an image to pass to the ML model, gets the result and displays the
# appropriate image and Wikipedia description
def recognize_image():
    global img
    f_types = [('Image files', '*.bmp *.jpg *.jpeg *.png')]
    filename = filedialog.askopenfilename(filetypes = f_types)

    demo = detector.prediction(filename)
    label = demo["class_name"]
    confidence = demo["confidence"]

    animalLabel = tk.Label(window, text = label, font = animalFont)
    animalLabel.grid(row = 3, column = 1)

    img = ImageTk.PhotoImage(file = str.lower("assets/%s.jpg" % label))
    imageLabel = tk.Label(window, image = img)
    imageLabel.grid(row = 4, column = 1)

    print("I'm %d%% sure this is a %s." % (confidence, str.lower(label)))

    wiki = wikipediaapi.Wikipedia('en')
    page = wiki.page(label)
    desc = page.summary

    desc_area = scrolledtext.ScrolledText(window, wrap = tk.WORD, width = 50, height = 10, font = descFont)    
    desc_area.grid(row = 5, column = 1, pady = 10)

    desc_area.tag_configure('tag-center', justify='center')
    desc_area.insert(tk.END, desc, 'tag-center')

    desc_area.configure(state ='disabled')

# Keeps the window open
window.mainloop()
