from pathlib import Path

# Configuración de Ventana
ANCHO_PANTALLA = 1280
ALTO_PANTALLA = 720
TITULO_JUEGO = "Simon Game - Classic Edition"

# Rutas
BASE_DIR = Path(__file__).parent
ARCHIVO_NIVELES = BASE_DIR / "niveles.txt"
RUTA_IMAGEN_SIMON = BASE_DIR / "simon_img.png"

# Estados del Juego
ESTADO_TITULO = "TITULO"
ESTADO_PERSONAJE = "PERSONAJE"
ESTADO_JUEGO = "JUEGO"

# Tiempos
TIEMPO_ESPERA = 0.5
TIEMPO_TOTAL_TEMPORIZADOR = 10.0

# Estilos y Fuentes
FUENTE_TITULO = ("Arial", 28, "bold")
FUENTE_SUBTITULO = ("Arial", 24, "bold")
FUENTE_BOTONES = ("Arial", 14, "bold")
FUENTE_ESTADO = ("Arial", 13, "bold")
FUENTE_PUNTAJE = ("Arial", 12, "bold")

# Colores
COLOR_FONDO = "#BDBDBD"
COLOR_TEXTO_OSCURO = "#111111"
COLOR_BOTON_NORMAL = "white"

COLOR_ROJO = "red"
COLOR_AZUL = "blue"
COLOR_VERDE = "green"
COLOR_AMARILLO = "yellow"

COLOR_ESTADO_LISTO = "#FFD54A"
COLOR_ESTADO_NIVEL = "#A5D6A7"
COLOR_ESTADO_ERROR = "#E53935"
COLOR_ESTADO_REPETIR = "#FFB300"
COLOR_ESTADO_AVANZA = "#66BB6A"
COLOR_ESTADO_NUEVO = "#90CAF9"