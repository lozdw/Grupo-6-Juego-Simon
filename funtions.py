from pathlib import Path
from random import randint
import threading
import time


tiempo_espera = 0.5
ARCHIVO_NIVELES = Path(__file__).with_name("niveles.txt")
colores_secuencia = []
colores_ingresados = []


def _normalizar_nivel(valor):
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


def asegurar_archivo_niveles():
    if not ARCHIVO_NIVELES.exists():
        ARCHIVO_NIVELES.write_text("1", encoding="utf-8")
        return
    actual = ARCHIVO_NIVELES.read_text(encoding="utf-8").strip()
    if actual == "":
        ARCHIVO_NIVELES.write_text("1", encoding="utf-8")


def consultar_nivel():
    asegurar_archivo_niveles()
    try:
        with ARCHIVO_NIVELES.open("r", encoding="utf-8") as archivo:
            valor_nivel = archivo.read().strip()
    except OSError:
        return "1"
    normalizado = _normalizar_nivel(valor_nivel)
    if str(normalizado) != valor_nivel:
        ARCHIVO_NIVELES.write_text(f"{normalizado}", encoding="utf-8")
    return str(normalizado)


def generar_colores():
    colores_secuencia.clear()
    valor_nivel = int(consultar_nivel())
    for _ in range(valor_nivel):
        colores_secuencia.append(randint(1, 4))


def visualizar_colores(secuencia, boton_azul, boton_verde, boton_rojo, boton_amarillo, boton_inicio, respuesta_turno):
    for boton in (boton_azul, boton_verde, boton_rojo, boton_amarillo):
        boton.config(state="disabled")
    boton_inicio.config(text=f"NIVEL: {consultar_nivel()}", state="disabled")

    botones = {1: boton_rojo, 2: boton_azul, 3: boton_verde, 4: boton_amarillo}
    colores = {1: "red", 2: "blue", 3: "green", 4: "yellow"}
    for numero_color in secuencia:
        boton = botones[numero_color]
        boton.config(background=colores[numero_color])
        time.sleep(tiempo_espera)
        boton.config(background="white")
        time.sleep(tiempo_espera)

    for boton in (boton_azul, boton_verde, boton_rojo, boton_amarillo):
        boton.config(state="normal")
    boton_inicio.config(text="START GAME!", state="normal")
    if respuesta_turno:
        respuesta_turno()


def iniciar_juego(boton_azul, boton_verde, boton_rojo, boton_amarillo, boton_inicio, respuesta_turno):
    colores_secuencia.clear()
    colores_ingresados.clear()
    generar_colores()
    hilo = threading.Thread(
        target=visualizar_colores,
        args=(colores_secuencia, boton_azul, boton_verde, boton_rojo, boton_amarillo, boton_inicio, respuesta_turno),
        daemon=True,
    )
    hilo.start()


def repetir_secuencia(boton_azul, boton_verde, boton_rojo, boton_amarillo, boton_inicio, reanudar=None):
    def tarea():
        visualizar_colores(colores_secuencia, boton_azul, boton_verde, boton_rojo, boton_amarillo, boton_inicio, None)
        if reanudar:
            reanudar()

    hilo = threading.Thread(target=tarea, daemon=True)
    hilo.start()


def obtener_color(numero_color, detener=None, exito=None, tiempo_restante=None, siguiente=None, error=None):
    colores_ingresados.append(numero_color)
    if len(colores_secuencia) != len(colores_ingresados):
        for indice in range(len(colores_ingresados)):
            if colores_secuencia[indice] != colores_ingresados[indice]:
                if error:
                    error()
                colores_ingresados.clear()
                return
    elif colores_secuencia == colores_ingresados:
        if detener:
            detener()
        nivel_actual = consultar_nivel()
        if exito:
            exito(float(tiempo_restante) if tiempo_restante is not None else 0.0, int(nivel_actual))
        avanzar_nivel()
        colores_secuencia.clear()
        colores_ingresados.clear()
        if siguiente:
            siguiente()


def avanzar_nivel():
    nivel_actual = int(consultar_nivel())
    ARCHIVO_NIVELES.write_text(f"{nivel_actual + 1}", encoding="utf-8")


def reiniciar_progreso():
    ARCHIVO_NIVELES.write_text("1", encoding="utf-8")
    colores_secuencia.clear()
    colores_ingresados.clear()
