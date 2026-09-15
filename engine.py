from random import randint
import threading
import time
import constants as const

class MotorSimon:
    def __init__(self, gestor_puntuacion):
        self.gestor_puntuacion = gestor_puntuacion
        self.colores_secuencia = []
        self.colores_ingresados = []
        self.personaje_actual = None
        
        # Estado del temporizador
        self.t_total = const.TIEMPO_TOTAL_TEMPORIZADOR
        self.t_restante = self.t_total
        self.t_faltante = 0.0
        self.temporizador_activo = False

    def _normalizar_nivel(self, valor):
        if valor is None:
            return 1
        valor = str(valor).strip()
        if valor == "":
            return 1
        try:
            convertido = int(valor)
            return convertido if convertido > 0 else 1
        except ValueError:
            return 1

    def asegurar_archivo_niveles(self):
        if not const.ARCHIVO_NIVELES.exists():
            const.ARCHIVO_NIVELES.write_text("1", encoding="utf-8")
            return
        actual = const.ARCHIVO_NIVELES.read_text(encoding="utf-8").strip()
        if actual == "":
            const.ARCHIVO_NIVELES.write_text("1", encoding="utf-8")

    def consultar_nivel(self):
        self.asegurar_archivo_niveles()
        try:
            with const.ARCHIVO_NIVELES.open("r", encoding="utf-8") as archivo:
                valor_nivel = archivo.read().strip()
        except OSError:
            return "1"
        normalizado = self._normalizar_nivel(valor_nivel)
        if str(normalizado) != valor_nivel:
            const.ARCHIVO_NIVELES.write_text(f"{normalizado}", encoding="utf-8")
        return str(normalizado)

    def avanzar_nivel(self):
        nivel_actual = int(self.consultar_nivel())
        const.ARCHIVO_NIVELES.write_text(f"{nivel_actual + 1}", encoding="utf-8")

    def reiniciar_progreso(self):
        const.ARCHIVO_NIVELES.write_text("1", encoding="utf-8")
        self.colores_secuencia.clear()
        self.colores_ingresados.clear()

    def generar_colores(self):
        self.colores_secuencia.clear()
        valor_nivel = int(self.consultar_nivel())
        for _ in range(valor_nivel):
            self.colores_secuencia.append(randint(1, 4))

    def iniciar_juego(self, callback_visualizar, callback_fin):
        self.colores_secuencia.clear()
        self.colores_ingresados.clear()
        self.generar_colores()
        hilo = threading.Thread(
            target=callback_visualizar,
            args=(self.colores_secuencia, callback_fin),
            daemon=True
        )
        hilo.start()

    def repetir_secuencia(self, callback_visualizar, callback_reanudar=None):
        def tarea():
            callback_visualizar(self.colores_secuencia, None)
            if callback_reanudar:
                callback_reanudar()
        hilo = threading.Thread(target=tarea, daemon=True)
        hilo.start()

    def registrar_color(self, numero_color, detener_cb, exito_cb, siguiente_cb, error_cb):
        self.colores_ingresados.append(numero_color)
        if len(self.colores_secuencia) != len(self.colores_ingresados):
            for indice in range(len(self.colores_ingresados)):
                if self.colores_secuencia[indice] != self.colores_ingresados[indice]:
                    if error_cb:
                        error_cb()
                    self.colores_ingresados.clear()
                    return
        elif self.colores_secuencia == self.colores_ingresados:
            if detener_cb:
                detener_cb()
            nivel_actual = self.consultar_nivel()
            if exito_cb:
                exito_cb(float(self.t_restante), int(nivel_actual))
            self.avanzar_nivel()
            self.colores_secuencia.clear()
            self.colores_ingresados.clear()
            if siguiente_cb:
                siguiente_cb()