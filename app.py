import funtions
from score import GestorPuntuacion
from personajes import Miku, Teto
from tkinter import *
from tkinter import ttk


class App:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.config(bg="#BDBDBD")
        self.gestor_puntuacion = GestorPuntuacion()
        self.personaje_actual = None
        self.t_total = 10.0
        self.t_restante = self.t_total
        self.t_faltante = 0.0
        self.temporizador_activo = False

        self.contenedor = Frame(self.ventana, bg="#BDBDBD")
        self.contenedor.pack(fill="both", expand=True)
        self.pantalla_titulo = Frame(self.contenedor, bg="#BDBDBD")
        self.pantalla_personaje = Frame(self.contenedor, bg="#BDBDBD")
        self.pantalla_juego = Frame(self.contenedor, bg="#BDBDBD")
        self.crear_pantalla_titulo()
        self.crear_pantalla_personaje()
        self.crear_pantalla_juego()
        self.mostrar_titulo()

    def crear_pantalla_titulo(self):
        self.etiqueta_titulo = Label(self.pantalla_titulo, text="insertar título del juego", font=("Arial", 28, "bold"), bg="#BDBDBD", fg="#111111", padx=30, pady=30)
        self.etiqueta_titulo.pack(pady=(100, 30))
        Button(self.pantalla_titulo, text="iniciar", font=("Arial", 14, "bold"), command=self.mostrar_seleccion_personaje, padx=30, pady=8).pack()

    def crear_pantalla_personaje(self):
        Label(self.pantalla_personaje, text="elegir personaje", font=("Arial", 24, "bold"), bg="#BDBDBD", fg="#111111").pack(pady=(90, 30))
        self.etiqueta_puntaje_final = Label(self.pantalla_personaje, text="", font=("Arial", 14, "bold"), bg="#BDBDBD", fg="#111111")
        self.etiqueta_puntaje_final.pack(pady=(0, 20))
        marco = Frame(self.pantalla_personaje, bg="#BDBDBD")
        marco.pack()
        Button(marco, text="Miku", font=("Arial", 14, "bold"), width=12, command=lambda: self.seleccionar_personaje("Miku")).grid(row=0, column=0, padx=10)
        Button(marco, text="Teto", font=("Arial", 14, "bold"), width=12, command=lambda: self.seleccionar_personaje("Teto")).grid(row=0, column=1, padx=10)

    def crear_pantalla_juego(self):
        self.etiqueta_puntuacion = Label(self.pantalla_juego, text="Puntaje: 0", font=("Arial", 12, "bold"), bg="#BDBDBD")
        self.etiqueta_puntuacion.grid(row=0, column=0, columnspan=2, pady=(10, 0))

        def obtener_color_boton(numero_color):
            def pulsar_boton():
                self.personaje_actual.aplicar_habilidad(self)
                funtions.obtener_color(numero_color, self.detener_temporizador, self.al_completar_ronda, self.t_restante, self.mostrar_siguiente_nivel, self.reiniciar_ronda_erronea)
            return pulsar_boton

        self.rojo = Button(self.pantalla_juego, text="RED", height=10, width=20, font="BOLD", background="white", command=obtener_color_boton(1))
        self.rojo.grid(row=1, column=0)
        self.azul = Button(self.pantalla_juego, text="BLUE", height=10, width=20, font="BOLD", background="white", command=obtener_color_boton(2))
        self.azul.grid(row=2, column=0)
        self.verde = Button(self.pantalla_juego, text="GREEN", height=10, width=20, font="BOLD", background="white", command=obtener_color_boton(3))
        self.verde.grid(row=1, column=1)
        self.amarillo = Button(self.pantalla_juego, text="YELLOW", height=10, width=20, font="BOLD", background="white", command=obtener_color_boton(4))
        self.amarillo.grid(row=2, column=1)
        self.boton_inicio = Button(self.pantalla_juego, text="RESTART", background="black", foreground="white", command=self.volver_a_seleccion)
        self.boton_inicio.grid(row=3, column=0, columnspan=2, pady=10)
        self.etiqueta_estado = Label(self.pantalla_juego, text="Listo para empezar", font=("Arial", 13, "bold"), bg="#FFD54A", fg="#111111", padx=12, pady=6, relief="solid", borderwidth=2)
        self.etiqueta_estado.grid(row=4, column=0, columnspan=2, pady=(0, 10))
        self.etiqueta_tiempo = Label(self.pantalla_juego, text="Tiempo: 10.0s", font=("Arial", 12, "bold"), bg="#BDBDBD", fg="#111111")
        self.etiqueta_tiempo.grid(row=5, column=0, columnspan=2, pady=(0, 5))
        self.progreso = ttk.Progressbar(self.pantalla_juego, orient=HORIZONTAL, length=300, mode="determinate")
        self.progreso.grid(row=6, column=0, columnspan=2, pady=10)

    def ocultar_pantallas(self):
        for pantalla in (self.pantalla_titulo, self.pantalla_personaje, self.pantalla_juego):
            pantalla.pack_forget()

    def mostrar_titulo(self):
        self.ocultar_pantallas()
        self.pantalla_titulo.pack(fill="both", expand=True)

    def mostrar_seleccion_personaje(self, puntaje_final=None):
        if puntaje_final is not None:
            self.etiqueta_puntaje_final.config(text=f"Puntaje final: {puntaje_final}")
        self.ocultar_pantallas()
        self.pantalla_personaje.pack(fill="both", expand=True)

    def seleccionar_personaje(self, nombre):
        self.personaje_actual = Miku() if nombre == "Miku" else Teto()
        self.ocultar_pantallas()
        self.pantalla_juego.pack(fill="both", expand=True)
        self.preparar_juego()

    def al_completar_ronda(self, tiempo_restante, nivel):
        puntos = self.gestor_puntuacion.agregar_por_ronda(tiempo_restante, nivel, self.personaje_actual.multiplicador_puntaje)
        self.etiqueta_puntuacion.config(text=f"Puntaje: {self.gestor_puntuacion.total}")
        return puntos

    def actualizar_interfaz_tiempo(self):
        self.etiqueta_tiempo.config(text=f"Tiempo: {self.t_restante:.1f}s")
        self.progreso["value"] = min(100, (self.t_restante / self.t_total) * 100)

    def preparar_juego(self):
        self.temporizador_activo = False
        self.t_total = 10.0
        self.t_restante = self.t_total
        self.t_faltante = 0.0
        self.personaje_actual.reiniciar_habilidad()
        self.progreso["value"] = 100
        self.etiqueta_puntuacion.config(text=f"Puntaje: {self.gestor_puntuacion.total}")
        self.actualizar_interfaz_tiempo()
        self.etiqueta_estado.config(text=f"Nivel {funtions.consultar_nivel()}", bg="#A5D6A7", fg="#111111")
        funtions.iniciar_juego(self.azul, self.verde, self.rojo, self.amarillo, self.boton_inicio, self.iniciar_temporizador)

    def pausar_temporizador(self):
        self.temporizador_activo = False

    def reanudar_temporizador(self):
        self.temporizador_activo = True
        self.actualizar_tiempo()

    def nueva_partida(self):
        self.gestor_puntuacion.reset()
        self.etiqueta_puntuacion.config(text="Puntaje: 0")
        funtions.reiniciar_progreso()
        self.etiqueta_estado.config(text="Nueva partida", bg="#90CAF9", fg="#111111")
        self.preparar_juego()

    def volver_a_seleccion(self):
        self.detener_temporizador()
        funtions.reiniciar_progreso()
        self.gestor_puntuacion.reset()
        self.etiqueta_puntuacion.config(text="Puntaje: 0")
        self.personaje_actual = None
        self.mostrar_seleccion_personaje()

    def finalizar_partida(self):
        puntaje_final = self.gestor_puntuacion.total
        self.detener_temporizador()
        funtions.reiniciar_progreso()
        self.gestor_puntuacion.reset()
        self.etiqueta_puntuacion.config(text="Puntaje: 0")
        self.personaje_actual = None
        self.mostrar_seleccion_personaje(puntaje_final)

    def mostrar_siguiente_nivel(self):
        self.etiqueta_estado.config(text="¡Siguiente nivel!", bg="#66BB6A", fg="#111111")
        self.ventana.after(800, self.preparar_juego)

    def reiniciar_ronda_erronea(self):
        self.t_restante = max(0.0, self.t_restante - 2.0)
        self.progreso["value"] = (self.t_restante / self.t_total) * 100
        self.etiqueta_estado.config(text="¡Error! Secuencia reiniciada (-2s)", bg="#E53935", fg="white")
        if self.t_restante <= 0:
            self.progreso["value"] = 0
            self.finalizar_partida()
            return
        self.pausar_temporizador()
        self.ventana.after(700, lambda: self.etiqueta_estado.config(text="Repitiendo secuencia...", bg="#FFB300", fg="#111111"))
        self.ventana.after(900, lambda: funtions.repetir_secuencia(self.azul, self.verde, self.rojo, self.amarillo, self.boton_inicio, self.reanudar_temporizador))
        self.ventana.after(1500, lambda: self.etiqueta_estado.config(text=f"Nivel {funtions.consultar_nivel()}", bg="#A5D6A7", fg="#111111"))

    def iniciar_temporizador(self):
        self.temporizador_activo = True
        self.t_restante = self.t_total
        self.actualizar_tiempo()

    def detener_temporizador(self):
        self.temporizador_activo = False

    def actualizar_tiempo(self):
        if self.temporizador_activo and self.t_restante > 0:
            self.t_restante -= 0.1
            self.t_faltante = self.t_total - self.t_restante
            self.actualizar_interfaz_tiempo()
            if round(self.t_restante, 2) <= 0:
                self.progreso["value"] = 0
                self.etiqueta_tiempo.config(text="Tiempo: 0.0s")
                self.finalizar_partida()
            else:
                self.ventana.after(100, self.actualizar_tiempo)


if __name__ == "__main__":
    ventana = Tk()
    ventana.title("Simon Game")
    root = App(ventana)
    ventana.mainloop()
