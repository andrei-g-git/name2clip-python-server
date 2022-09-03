from tkinter import Tk, Canvas, Label
#from main import Main
from server import ScrapingServer
import threading

root = Tk()

canvas = Canvas(
    root,
    width=500,
    height=300
)
canvas.grid(columnspan=3, rowspan=3)

label_1 = Label(root, text="running...")
label_1.grid(column=1, row=1)

thread_2 = threading.Thread(target=ScrapingServer.init_server, args=("localhost", 9999))
thread_2.start()

root.mainloop()


