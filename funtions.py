from random import randint

class GestorSecuencia:
    def __init__(self, ruta_niveles):
        self.colores_secuencia = []
        self.colores_ingresados = []
        self.archivo_niveles = ruta_niveles
        self.asegurar_archivo_niveles()

    def asegurar_archivo_niveles(self):
        if not self.archivo_niveles.exists():
            self.archivo_niveles.write_text("1", encoding="utf-8")
            return
        actual = self.archivo_niveles.read_text(encoding="utf-8").strip()
        if actual == "":
            self.archivo_niveles.write_text("1", encoding="utf-8")

    def consultar_nivel(self):
        self.asegurar_archivo_niveles()
        try:
            with self.archivo_niveles.open("r", encoding="utf-8") as archivo:
                valor = int(archivo.read().strip())
                return valor if valor > 0 else 1
        except (OSError, ValueError):
            return 1

    def avanzar_nivel(self):
        nivel_actual = self.consultar_nivel()
        self.archivo_niveles.write_text(f"{nivel_actual + 1}", encoding="utf-8")

    def reiniciar_progreso(self):
        self.archivo_niveles.write_text("1", encoding="utf-8")
        self.colores_secuencia.clear()
        self.colores_ingresados.clear()

    def iniciar_juego(self):
        self.colores_secuencia.clear()
        self.colores_ingresados.clear()
        valor_nivel = self.consultar_nivel()
        for _ in range(valor_nivel):
            self.colores_secuencia.append(randint(1, 4))
        return self.colores_secuencia

    def verificar_color(self, numero_color):
        self.colores_ingresados.append(numero_color)
        indice = len(self.colores_ingresados) - 1
        
        if self.colores_ingresados[indice] != self.colores_secuencia[indice]:
            self.colores_ingresados.clear()
            return "ERROR"
            
        if len(self.colores_ingresados) == len(self.colores_secuencia):
            self.avanzar_nivel()
            self.colores_secuencia.clear()
            self.colores_ingresados.clear()
            return "EXITO"
            
        return "CONTINUAR"