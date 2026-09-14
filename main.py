from tkinter import Tk

from app import App


if __name__ == "__main__":
    ventana = Tk()
    ventana.title("Simon Game")
    App(ventana)
    ventana.mainloop()
