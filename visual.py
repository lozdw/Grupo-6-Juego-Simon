from tkinter import *
from tkinter import ttk
import time
import constants as const

class RenderizadorSimon:
    def __init__(self, ventana, motor, app_controller):
        self.ventana = ventana
        self.motor = motor
        self.app = app_controller

        self.contenedor = Frame(self.ventana, bg=const.COLOR_FONDO)
        self.contenedor.pack(fill="both", expand=True)

        self.pantalla_titulo = Frame(self.contenedor, bg=const.COLOR_FONDO)
        self.pantalla_personaje = Frame(self.contenedor, bg=const.COLOR_FONDO)
        self.pantalla_juego = Frame(self.contenedor, bg=const.COLOR_FONDO)

        self.crear_pantalla_titulo()
        self.crear_pantalla_personaje()
        self.crear_pantalla_juego()

    def crear_pantalla_titulo(self):
        self.etiqueta_titulo = Label(
            self.pantalla_titulo, text=const.TITULO_JUEGO, 
            font=const.FUENTE_TITULO, bg=const.COLOR_FONDO, fg=const.COLOR_TEXTO_OSCURO, 
            padx=30, pady=30
        )
        self.etiqueta_titulo.pack(pady=(100, 30))
        Button(
            self.pantalla_titulo, text="iniciar", font=const.FUENTE_BOTONES, 
            command=self.app.mostrar_seleccion_personaje, padx=30, pady=8
        ).pack()

    def crear_pantalla_personaje(self):
        Label(
            self.pantalla_personaje, text="elegir personaje", 
            font=const.FUENTE_SUBTITULO, bg=const.COLOR_FONDO, fg=const.COLOR_TEXTO_OSCURO
        ).pack(pady=(90, 30))
        
        self.etiqueta_puntaje_final = Label(
            self.pantalla_personaje, text="", font=const.FUENTE_BOTONES, 
            bg=const.COLOR_FONDO, fg=const.COLOR_TEXTO_OSCURO
        )
        self.etiqueta_puntaje_final.pack(pady=(0, 20))
        
        marco = Frame(self.pantalla_personaje, bg=const.COLOR_FONDO)
        marco.pack()
        Button(marco, text="Miku", font=const.FUENTE_BOTONES, width=12, command=lambda: self.app.seleccionar_personaje("Miku")).grid(row=0, column=0, padx=10)
        Button(marco, text="Teto", font=const.FUENTE_BOTONES, width=12, command=lambda: self.app.seleccionar_personaje("Teto")).grid(row=0, column=1, padx=10)

    def crear_pantalla_juego(self):
        self.etiqueta_puntuacion = Label(self.pantalla_juego, text="Puntaje: 0", font=const.FUENTE_PUNTAJE, bg=const.COLOR_FONDO)
        self.etiqueta_puntuacion.grid(row=0, column=0, columnspan=2, pady=(10, 0))

        def obtener_color_boton(num):
            return lambda: self.app.pulsar_color(num)

        self.rojo = Button(self.pantalla_juego, text="RED", height=10, width=20, font="BOLD", background=const.COLOR_BOTON_NORMAL, command=obtener_color_boton(1))
        self.rojo.grid(row=1, column=0)
        self.azul = Button(self.pantalla_juego, text="BLUE", height=10, width=20, font="BOLD", background=const.COLOR_BOTON_NORMAL, command=obtener_color_boton(2))
        self.azul.grid(row=2, column=0)
        self.verde = Button(self.pantalla_juego, text="GREEN", height=10, width=20, font="BOLD", background=const.COLOR_BOTON_NORMAL, command=obtener_color_boton(3))
        self.verde.grid(row=1, column=1)
        self.amarillo = Button(self.pantalla_juego, text="YELLOW", height=10, width=20, font="BOLD", background=const.COLOR_BOTON_NORMAL, command=obtener_color_boton(4))
        self.amarillo.grid(row=2, column=1)

        self.boton_inicio = Button(self.pantalla_juego, text="RESTART", background="black", foreground="white", command=self.app.volver_a_seleccion)
        self.boton_inicio.grid(row=3, column=0, columnspan=2, pady=10)

        self.etiqueta_estado = Label(
            self.pantalla_juego, text="Listo para empezar", font=const.FUENTE_ESTADO, 
            bg=const.COLOR_ESTADO_LISTO, fg=const.COLOR_TEXTO_OSCURO, padx=12, pady=6, relief="solid", borderwidth=2
        )
        self.etiqueta_estado.grid(row=4, column=0, columnspan=2, pady=(0, 10))

        self.etiqueta_tiempo = Label(self.pantalla_juego, text="Tiempo: 10.0s", font=const.FUENTE_PUNTAJE, bg=const.COLOR_FONDO, fg=const.COLOR_TEXTO_OSCURO)
        self.etiqueta_tiempo.grid(row=5, column=0, columnspan=2, pady=(0, 5))

        self.progreso = ttk.Progressbar(self.pantalla_juego, orient=HORIZONTAL, length=300, mode="determinate")
        self.progreso.grid(row=6, column=0, columnspan=2, pady=10)

    def ocultar_pantallas(self):
        for pantalla in (self.pantalla_titulo, self.pantalla_personaje, self.pantalla_juego):
            pantalla.pack_forget()

    def animar_secuencia(self, secuencia, respuesta_turno):
        for boton in (self.azul, self.verde, self.rojo, self.amarillo):
            boton.config(state="disabled")
        self.boton_inicio.config(text=f"NIVEL: {self.motor.consultar_nivel()}", state="disabled")

        botones = {1: self.rojo, 2: self.azul, 3: self.verde, 4: self.amarillo}
        colores = {1: const.COLOR_ROJO, 2: const.COLOR_AZUL, 3: const.COLOR_VERDE, 4: const.COLOR_AMARILLO}

        for numero in secuencia:
            btn = botones[numero]
            btn.config(background=colores[numero])
            time.sleep(const.TIEMPO_ESPERA)
            btn.config(background=const.COLOR_BOTON_NORMAL)
            time.sleep(const.TIEMPO_ESPERA)

        for boton in (self.azul, self.verde, self.rojo, self.amarillo):
            boton.config(state="normal")
        self.boton_inicio.config(text="RESTART", state="normal")

        if respuesta_turno:
            respuesta_turno()