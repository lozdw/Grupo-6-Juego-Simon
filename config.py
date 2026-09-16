from pathlib import Path

class ConfiguracionJuego:
    def __init__(self):
        self.ancho_pantalla = 600
        self.alto_pantalla = 700
        self.titulo = "Simon Game - Miku & Teto"
        self.fps = 60

        self.directorio_base = Path(__file__).parent
        self.archivo_niveles = self.directorio_base / "niveles.txt"