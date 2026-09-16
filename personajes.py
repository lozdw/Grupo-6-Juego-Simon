from abc import ABC, abstractmethod

class Personaje(ABC):
    def __init__(self, nombre):
        self.nombre = nombre
        self.habilidad_aplicada = False
        self.multiplicador_puntaje = 1.0

    def aplicar_habilidad(self, estado_juego):
        if self.habilidad_aplicada:
            return
        self._aplicar_habilidad(estado_juego)
        self.habilidad_aplicada = True

    def reiniciar_habilidad(self):
        self.habilidad_aplicada = False
        self.multiplicador_puntaje = 1.0

    @abstractmethod
    def _aplicar_habilidad(self, estado_juego):
        pass

class Miku(Personaje):
    def __init__(self):
        super().__init__("Miku")

    def _aplicar_habilidad(self, estado_juego):
        estado_juego.t_total += 5.0
        estado_juego.t_restante += 5.0

class Teto(Personaje):
    def __init__(self):
        super().__init__("Teto")

    def _aplicar_habilidad(self, estado_juego):
        self.multiplicador_puntaje = 1.5
