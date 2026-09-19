class GestorPuntuacion:
    def __init__(self):
        self.total = 0

    def reset(self):
        self.total = 0

    def agregar_por_ronda(self, tiempo_restante, nivel, multiplicador=1.0):
        puntos_base = max(0.0, float(tiempo_restante)) * 100 + max(1, int(nivel)) * 50
        puntos = int(puntos_base * float(multiplicador))
        self.total += puntos
        return puntos 

    def agregar_por_acierto(self, tiempo_restante, nivel, multiplicador=1.0):
        return self.agregar_por_ronda(tiempo_restante, nivel, multiplicador)
