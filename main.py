from tkinter import Tk, Canvas, Label

class Main(Label): #doesn't work for now...
    def __inin__(self, parent):
        super().__init__(parent)

        canvas = Canvas(
            self,

        )
        self.test_label = Label(self, text="this is the main label component")

        #self.test_label.grid(column=1, row=1)