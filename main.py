from tkinter import Tk
from app import App
import constants as const

if __name__ == "__main__":
    ventana = Tk()
    ventana.title(const.TITULO_JUEGO)
    ventana.geometry(f"{const.ANCHO_PANTALLA}x{const.ALTO_PANTALLA}")
    App(ventana)
    ventana.mainloop()