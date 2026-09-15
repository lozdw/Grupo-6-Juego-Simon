from score import GestorPuntuacion
from personajes import Miku, Teto
from engine import MotorSimon
from visual import RenderizadorSimon
import constants as const

class App:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.config(bg=const.COLOR_FONDO)
        self.gestor_puntuacion = GestorPuntuacion()
        self.motor = MotorSimon(self.gestor_puntuacion)
        self.view = RenderizadorSimon(self.ventana, self.motor, self)

        self.t_total = const.TIEMPO_TOTAL_TEMPORIZADOR
        self.t_restante = self.t_total
        self.t_faltante = 0.0
        self.temporizador_activo = False

        self.mostrar_titulo()

    def mostrar_titulo(self):
        self.view.ocultar_pantallas()
        self.view.pantalla_titulo.pack(fill="both", expand=True)

    def mostrar_seleccion_personaje(self, puntaje_final=None):
        if puntaje_final is not None:
            self.view.etiqueta_puntaje_final.config(text=f"Puntaje final: {puntaje_final}")
        self.view.ocultar_pantallas()
        self.view.pantalla_personaje.pack(fill="both", expand=True)

    def seleccionar_personaje(self, nombre):
        self.motor.personaje_actual = Miku() if nombre == "Miku" else Teto()
        self.view.ocultar_pantallas()
        self.view.pantalla_juego.pack(fill="both", expand=True)
        self.preparar_juego()

    def pulsar_color(self, numero_color):
        self.motor.personaje_actual.aplicar_habilidad(self)
        self.motor.registrar_color(
            numero_color,
            self.detener_temporizador,
            self.al_completar_ronda,
            self.mostrar_siguiente_nivel,
            self.reiniciar_ronda_erronea
        )

    def al_completar_ronda(self, tiempo_restante, nivel):
        puntos = self.gestor_puntuacion.agregar_por_ronda(
            tiempo_restante, nivel, self.motor.personaje_actual.multiplicador_puntaje
        )
        self.view.etiqueta_puntuacion.config(text=f"Puntaje: {self.gestor_puntuacion.total}")
        return puntos

    def actualizar_interfaz_tiempo(self):
        self.view.etiqueta_tiempo.config(text=f"Tiempo: {self.t_restante:.1f}s")
        self.view.progreso["value"] = min(100, (self.t_restante / self.t_total) * 100)

    def preparar_juego(self):
        self.temporizador_activo = False
        self.t_total = const.TIEMPO_TOTAL_TEMPORIZADOR
        self.t_restante = self.t_total
        self.t_faltante = 0.0
        self.motor.personaje_actual.reiniciar_habilidad()
        self.view.progreso["value"] = 100
        self.view.etiqueta_puntuacion.config(text=f"Puntaje: {self.gestor_puntuacion.total}")
        self.actualizar_interfaz_tiempo()
        self.view.etiqueta_estado.config(
            text=f"Nivel {self.motor.consultar_nivel()}", 
            bg=const.COLOR_ESTADO_NIVEL, fg=const.COLOR_TEXTO_OSCURO
        )
        self.motor.iniciar_juego(self.view.animar_secuencia, self.iniciar_temporizador)

    def pausar_temporizador(self):
        self.temporizador_activo = False

    def reanudar_temporizador(self):
        self.temporizador_activo = True
        self.actualizar_tiempo()

    def volver_a_seleccion(self):
        self.detener_temporizador()
        self.motor.reiniciar_progreso()
        self.gestor_puntuacion.reset()
        self.view.etiqueta_puntuacion.config(text="Puntaje: 0")
        self.motor.personaje_actual = None
        self.mostrar_seleccion_personaje()

    def finalizar_partida(self):
        puntaje_final = self.gestor_puntuacion.total
        self.detener_temporizador()
        self.motor.reiniciar_progreso()
        self.gestor_puntuacion.reset()
        self.view.etiqueta_puntuacion.config(text="Puntaje: 0")
        self.motor.personaje_actual = None
        self.mostrar_seleccion_personaje(puntaje_final)

    def mostrar_siguiente_nivel(self):
        self.view.etiqueta_estado.config(text="¡Siguiente nivel!", bg=const.COLOR_ESTADO_AVANZA, fg=const.COLOR_TEXTO_OSCURO)
        self.ventana.after(800, self.preparar_juego)

    def reiniciar_ronda_erronea(self):
        self.t_restante = max(0.0, self.t_restante - 2.0)
        self.view.progreso["value"] = (self.t_restante / self.t_total) * 100
        self.view.etiqueta_estado.config(text="¡Error! Secuencia reiniciada (-2s)", bg=const.COLOR_ESTADO_ERROR, fg="white")
        if self.t_restante <= 0:
            self.view.progreso["value"] = 0
            self.finalizar_partida()
            return
        self.pausar_temporizador()
        self.ventana.after(700, lambda: self.view.etiqueta_estado.config(text="Repitiendo secuencia...", bg=const.COLOR_ESTADO_REPETIR, fg=const.COLOR_TEXTO_OSCURO))
        self.ventana.after(900, lambda: self.motor.repetir_secuencia(self.view.animar_secuencia, self.reanudar_temporizador))
        self.ventana.after(1500, lambda: self.view.etiqueta_estado.config(text=f"Nivel {self.motor.consultar_nivel()}", bg=const.COLOR_ESTADO_NIVEL, fg=const.COLOR_TEXTO_OSCURO))

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
                self.view.progreso["value"] = 0
                self.view.etiqueta_tiempo.config(text="Tiempo: 0.0s")
                self.finalizar_partida()
            else:
                self.ventana.after(100, self.actualizar_tiempo)