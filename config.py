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
