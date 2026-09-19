from pathlib import Path

class ConfiguracionJuego:
    def __init__(self):
        self.ancho_pantalla = 1280
        self.alto_pantalla = 720
        self.titulo = "VoColoroid"
        self.fps = 60

        self.directorio_base = Path(__file__).parent
        self.archivo_niveles = self.directorio_base / "niveles.txt"
        self.archivo_fuente = self.directorio_base / "assets" / "fonts" / "I-pixel-u.ttf"
        self.archivo_musica = self.directorio_base / "assets" / "sounds" / "medicine teto.mp3"
        self.archivo_sonido_rojo = self.directorio_base / "assets" / "sounds" / "sonido boton rojo.mp3"
        self.archivo_sonido_azul = self.directorio_base / "assets" / "sounds" / "sonido boton azul.mp3"
        self.archivo_sonido_verde = self.directorio_base / "assets" / "sounds" / "sonido boton verde.mp3"
        self.archivo_sonido_amarillo = self.directorio_base / "assets" / "sounds" / "sonido boton amarillo.mp3"
        self.archivo_sonido_seleccion_personaje = self.directorio_base / "assets" / "sounds" / "sonido tres.mp3"
        self.archivo_sonido_iniciar = self.directorio_base / "assets" / "sounds" / "sonido uno.mp3"
        self.archivo_sonido_nivel = self.directorio_base / "assets" / "sounds" / "sonido cuatro.mp3"
        self.archivo_sonido_reinicio = self.directorio_base / "assets" / "sounds" / "sonido dos.mp3"
        self.archivo_sonido_corazon = self.directorio_base / "assets" / "sounds" / "sonido corazon.mp3"
        self.archivo_sonido_settings = self.directorio_base / "assets" / "sounds" / "sonido tuerca.mp3"
