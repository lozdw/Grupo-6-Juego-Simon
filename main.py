import funtions 
from score import GestorPuntuacion
from tkinter import *
from tkinter import ttk


class App():
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.config(bg="#BDBDBD")
        self.gestor_puntuacion = GestorPuntuacion()

        self.etiqueta_puntuacion = Label(self.ventana, text="Puntaje: 0", font=("Arial", 12, "bold"), bg="#BDBDBD")
        self.etiqueta_puntuacion.grid(row=0, column=0, columnspan=2, pady=(10, 0))

        def obtener_color_boton(numero_color):
            return lambda: funtions.obtener_color(
            numero_color,
                self.detener_temporizador,
                self.al_completar_ronda,
                self.t_restante,
                self.mostrar_siguiente_nivel,
                self.reiniciar_ronda_erronea,
            )

        # Se envía self.detener_temporizador en los botones lambda
        self.rojo = Button(self.ventana, text = "RED", height= 10, width= 20, font= "BOLD", background="white", command=obtener_color_boton(1))
        self.rojo.grid(row = 1, column = 0)
        
        self.azul = Button(self.ventana, text = "BLUE", height= 10, width= 20, font= "BOLD", background="white", command=obtener_color_boton(2))
        self.azul.grid(row = 2, column = 0)
        
        self.verde = Button(self.ventana, text = "GREEN", height= 10, width= 20, font= "BOLD", background="white", command=obtener_color_boton(3))
        self.verde.grid(row = 1, column = 1)
        
        self.amarillo = Button(self.ventana, text = "YELLOW", height= 10, width= 20, font= "BOLD", background="white", command=obtener_color_boton(4))
        self.amarillo.grid(row = 2, column = 1)
        
        # Se cambia el command a preparar_juego
        self.boton_inicio = Button(self.ventana, text = "REINICIAR", background = "black",foreground="white", command= self.nueva_partida)
        self.boton_inicio.grid(row= 3, column= 0, columnspan= 2, pady = 10)

        self.etiqueta_estado = Label(self.ventana, text="Listo para empezar", font=("Arial", 13, "bold"), bg="#FFD54A", fg="#111111", padx=12, pady=6, relief="solid", borderwidth=2)
        self.etiqueta_estado.grid(row=4, column=0, columnspan=2, pady=(0, 10))

        self.etiqueta_tiempo = Label(self.ventana, text="Tiempo: 10.0s", font=("Arial", 12, "bold"), bg="#BDBDBD", fg="#111111")
        self.etiqueta_tiempo.grid(row=5, column=0, columnspan=2, pady=(0, 5))

        # Módulo de tiempo
        self.progreso = ttk.Progressbar(self.ventana, orient=HORIZONTAL, length=300, mode='determinate')
        self.progreso.grid(row=6, column=0, columnspan=2, pady=10)
        
        self.t_total = 10.0 # Tiempo total para responder
        self.t_restante = self.t_total
        self.t_faltante = 0.0
        self.temporizador_activo = False

    def al_completar_ronda(self, tiempo_restante, nivel):
        puntos = self.gestor_puntuacion.agregar_por_ronda(tiempo_restante, nivel)
        self.etiqueta_puntuacion.config(text=f"Puntaje: {self.gestor_puntuacion.total}")
        return puntos

    def preparar_juego(self):
        self.temporizador_activo = False
        self.t_restante = float(self.t_total)
        self.t_faltante = 0.0
        self.progreso['value'] = 100
        self.etiqueta_puntuacion.config(text=f"Puntaje: {self.gestor_puntuacion.total}")
        self.etiqueta_tiempo.config(text=f"Tiempo: {self.t_restante:.1f}s")
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

    def mostrar_siguiente_nivel(self):
        self.etiqueta_estado.config(text="¡Siguiente nivel!", bg="#66BB6A", fg="#111111")
        self.ventana.after(800, self.preparar_juego)

    def reiniciar_ronda_erronea(self):
        self.t_restante = max(0.0, self.t_restante - 2.0)
        self.progreso['value'] = (self.t_restante / self.t_total) * 100
        self.etiqueta_estado.config(text="¡Error! Secuencia reiniciada (-2s)", bg="#E53935", fg="white", font=("Arial", 13, "bold"))

        if self.t_restante <= 0:
            self.detener_temporizador()
            self.progreso['value'] = 0
            self.etiqueta_estado.config(text="Tiempo agotado", bg="#B71C1C", fg="white")
            from tkinter import messagebox
            messagebox.showwarning(title="Tiempo Agotado", message="¡Se acabó el tiempo! Perdiste.")
            funtions.reiniciar_progreso()
            self.gestor_puntuacion.reset()
            self.etiqueta_puntuacion.config(text="Puntaje: 0")
            return

        self.pausar_temporizador()
        self.ventana.after(700, lambda: self.etiqueta_estado.config(text="Repitiendo secuencia...", bg="#FFB300", fg="#111111", font=("Arial", 14, "bold")))
        self.ventana.after(900, lambda: funtions.repetir_secuencia(self.azul, self.verde, self.rojo, self.amarillo, self.boton_inicio, self.reanudar_temporizador))
        self.ventana.after(1500, lambda: self.etiqueta_estado.config(text=f"Nivel {funtions.consultar_nivel()}", bg="#A5D6A7", fg="#111111", font=("Arial", 13, "bold")))

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
            self.etiqueta_tiempo.config(text=f"Tiempo: {self.t_restante:.1f}s")

            self.progreso['value'] = (self.t_restante / self.t_total) * 100

            if round(self.t_restante, 2) <= 0:
                self.detener_temporizador()
                self.progreso['value'] = 0
                self.etiqueta_tiempo.config(text="Tiempo: 0.0s")

                from tkinter import messagebox
                messagebox.showwarning(title="Tiempo Agotado", message="¡Se acabó el tiempo! Perdiste.")
                funtions.reiniciar_progreso()
                self.gestor_puntuacion.reset()
                self.etiqueta_puntuacion.config(text="Puntaje: 0")
            else:
                self.ventana.after(100, self.actualizar_tiempo)

if ("__main__" == __name__):
    ventana = Tk()
    ventana.title("Simon Game")
    root = App(ventana)
    ventana.mainloop()
