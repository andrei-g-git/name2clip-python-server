from copyreg import pickle
from tkinter import Button, OptionMenu, StringVar, Tk, Canvas, Label
#from main import Main
from server import ScrapingServer
import threading
import spacy 
import pickle

root = Tk()

canvas = Canvas(
    root,
    width=500,
    height=300
)
canvas.grid(columnspan=3, rowspan=3)

clicked = StringVar()

choices = [
    "Custom w/ vectors",
    "en_core_web_sm",
    "en_core_web_lg"
]
models = [
    "G:/portfolio/projects/scraper/models/woman_first_names_and_surnames_ner_model_5",
    "en_core_web_sm",
    "en_core_web_lg"
]

language_model_dropdown = OptionMenu(
    root, 
    clicked,
    *choices
)
clicked.set("en_core_web_lg")

language_model = spacy.load("en_core_web_lg")
with open("C:/My_Data/language_model_tkinter.pkl", "wb") as file:
    pickle.dump(language_model, file)

def handle_change():
    choice = clicked.get()    
    #index = [i for i in range(len(choices)) if choices[i] == choice]
    for i in range(len(choices)):
        if choices[i] == choice:
            global language_model
            language_model = spacy.load(models[i]) #aaaand I have no idea how to pass this to an instance of the server, especially on every change...
            #guess it's writing to disk like a sap then...
            with open("C:/My_Data/language_model_tkinter.pkl", "wb") as file:
                pickle.dump(language_model, file)

button = Button(root, text="switch model" , command=handle_change)
button.grid(column=2, row=0)

language_model_dropdown.grid(column=1, row=0)

label_1 = Label(root, text="running...")
label_1.grid(column=1, row=1)

thread_2 = threading.Thread(target=ScrapingServer.init_server, args=("localhost", 9999))
thread_2.start()

root.mainloop()


