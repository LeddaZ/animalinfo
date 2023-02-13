# animalinfo - Displays information about an animal recognized
# with Machine Learning for Kids

# Required dependencies
import github3
import os
import tkinter as tk
import tkinter.font as TkFont
import wikipediaapi

from dotenv import load_dotenv
from mlforkids import MLforKidsImageProject
from PIL import ImageTk
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter import ttk

# Loads the API key from the .env file
load_dotenv()
key = os.getenv("API_KEY")

# Gets the current commit hash from GitHub
gh = github3.login(token=os.getenv("GITHUB_TOKEN"))
repository = gh.repository(owner="LeddaZ", repository="animalinfo")
lastCommitHash = repository.branch("main").latest_sha()

# Trains the ML model to recognize images
detector = MLforKidsImageProject(key)
detector.train_model()

# Creates the window
window = tk.Tk()
window.title("Animal Info " + lastCommitHash[:8])
window.resizable(False, False)

# Fonts
titleFont = TkFont.Font(family="helvetica", size=36, weight="bold")
animalFont = TkFont.Font(family="helvetica", size=20, weight="bold")
descFont = TkFont.Font(family="helvetica", size=14)

# Title
titleLabel = tk.Label(window, text="Animal Info", font=titleFont)
titleLabel.grid(row=1, column=1)

# Image chooser button
button = tk.Button(window,
                   text="Choose an image",
                   command=lambda: recognize_image())
button.grid(row=2, column=1, pady=5)

# Language selector
combo_value = tk.StringVar()
combobox = ttk.Combobox(window, textvariable=combo_value)
combobox.grid(row=3, column=1, pady=5)
combobox["values"] = ("English", "Italiano")
combobox["state"] = "readonly"
combobox.current(0)

# Language-dependent data
wiki_languages = ["en", "it"]
page_titles_en = ["Dog", "Cat", "Capybara", "Frog", "Rabbit", "Pig", "Snake"]
page_titles_it = [
    "Cane", "Gatto", "Capibara", "Rana", "Coniglio", "Maiale", "Serpente"
]


# Chooses an image to pass to the ML model, gets the result and displays the
# appropriate image and Wikipedia description
def recognize_image():
    global img
    global animalLabel
    try:
        animalLabel.config(text=" ")
    except NameError:
        pass
    f_types = [("Image files", "*.bmp *.jpg *.jpeg *.png")]
    filename = filedialog.askopenfilename(filetypes=f_types)

    demo = detector.prediction(filename)
    label = demo["class_name"]
    confidence = demo["confidence"]

    if (label != "Other"):
        img = ImageTk.PhotoImage(file=str.lower("assets/%s.jpg" % label))
        imagelabel = tk.Label(window, image=img)
        imagelabel.grid(row=5, column=1)

        print("I'm %d%% sure this is a %s." % (confidence, str.lower(label)))

        if (combobox.current() == 1):
            if (label == page_titles_en[0]):
                label = page_titles_it[0]
            elif (label == page_titles_en[1]):
                label = page_titles_it[1]
            elif (label == page_titles_en[2]):
                label = page_titles_it[2]
            elif (label == page_titles_en[3]):
                label = page_titles_it[3]
            elif (label == page_titles_en[4]):
                label = page_titles_it[4]
            elif (label == page_titles_en[5]):
                label = page_titles_it[5]
            elif (label == page_titles_en[6]):
                label = page_titles_it[6]

        wiki = wikipediaapi.Wikipedia(wiki_languages[combobox.current()])
        page = wiki.page(label)
        desc = page.summary

        desc_area = scrolledtext.ScrolledText(window,
                                              wrap=tk.WORD,
                                              width=50,
                                              height=10,
                                              font=descFont)
        desc_area.grid(row=6, column=1, pady=10)

        desc_area.tag_configure("tag-center", justify="center")
        desc_area.insert(tk.END, desc, "tag-center")

        desc_area.configure(state="disabled")
    else:
        desc_area = scrolledtext.ScrolledText(window,
                                              wrap=tk.WORD,
                                              width=50,
                                              height=10,
                                              font=descFont)
        desc_area.grid(row=6, column=1, pady=10)

        desc_area.tag_configure("tag-center", justify="center")
        desc_area.insert(tk.END, "This animal is not supported by the model.",
                         "tag-center")

        desc_area.configure(state="disabled")

        print("I'm %d%% sure this isn't a supported animal." % (confidence))

    animalLabel = tk.Label(window, text=label, font=animalFont)
    animalLabel.grid(row=4, column=1)


# Keeps the window open
window.mainloop()
