import pygame
from score import GestorPuntuacion
from funtions import GestorSecuencia
from personajes import Miku, Teto, Neru, Gumi

class App:
    def __init__(self, config):
        self.pantalla = pygame.display.set_mode((config.ancho_pantalla, config.alto_pantalla))
        pygame.display.set_caption(config.titulo)
        self.reloj = pygame.time.Clock()
        self.fps_objetivo = config.fps
        self.ejecutando = True

        self.gestor_puntuacion = GestorPuntuacion()
        self.gestor_secuencia = GestorSecuencia(config.archivo_niveles)
        self.personaje_actual = None

        pygame.font.init()
        self.fuente_titulo = pygame.font.SysFont("Arial", 48, bold=True)
        self.fuente_normal = pygame.font.SysFont("Arial", 24, bold=True)

        self.estado_actual = "MENU" # MENU, SELECCION, MOSTRANDO_SECUENCIA, JUGANDO, GAME_OVER
        
        # Colores (1: Rojo, 2: Azul, 3: Verde, 4: Amarillo - Basado en tu Tkinter)
        self.colores_base = {
            1: (150, 0, 0),    
            2: (0, 0, 150),    
            3: (0, 150, 0),    
            4: (150, 150, 0)   
        }
        self.colores_brillantes = {
            1: (255, 50, 50),
            2: (50, 50, 255),
            3: (50, 255, 50),
            4: (255, 255, 50)
        }
        
        self.rects_botones = {
            1: pygame.Rect(350, 150, 150, 150), # Rojo (Der. Arriba)
            3: pygame.Rect(100, 150, 150, 150), # Verde (Izq. Arriba)
            2: pygame.Rect(100, 350, 150, 150), # Azul (Izq. Abajo)
            4: pygame.Rect(350, 350, 150, 150)  # Amarillo (Der. Abajo)
        }
        
        self.rect_miku = pygame.Rect(60, 250, 120, 50)
        self.rect_teto = pygame.Rect(200, 250, 120, 50)
        self.rect_neru = pygame.Rect(340, 250, 120, 50)
        self.rect_gumi = pygame.Rect(480, 250, 120, 50)
        self.rect_reinicio = pygame.Rect(200, 550, 200, 50)

        self.t_total = 10.0
        self.t_restante = 10.0
        self.mensaje = "Listo"
        
        # Variables para la animación de parpadeo de secuencia
        self.color_iluminado = None
        self.indice_secuencia = 0
        self.tiempo_ultimo_cambio = 0
        self.luz_encendida = False

    def preparar_juego(self):
        self.gestor_secuencia.iniciar_juego()
        self.personaje_actual.reiniciar_habilidad()
        self.t_total = 10.0
        self.t_restante = 10.0
        self.mensaje = f"Nivel {self.gestor_secuencia.consultar_nivel()}"
        self.iniciar_animacion()

    def iniciar_animacion(self):
        self.estado_actual = "MOSTRANDO_SECUENCIA"
        self.indice_secuencia = 0
        self.color_iluminado = None
        self.luz_encendida = False
        self.tiempo_ultimo_cambio = pygame.time.get_ticks()

    def procesar_animacion(self):
        ahora = pygame.time.get_ticks()
        if ahora - self.tiempo_ultimo_cambio > 500: # 0.5s por parpadeo
            self.tiempo_ultimo_cambio = ahora
            
            if not self.luz_encendida:
                if self.indice_secuencia < len(self.gestor_secuencia.colores_secuencia):
                    self.color_iluminado = self.gestor_secuencia.colores_secuencia[self.indice_secuencia]
                    self.luz_encendida = True
                else:
                    self.color_iluminado = None
                    self.estado_actual = "JUGANDO"
            else:
                self.color_iluminado = None
                self.luz_encendida = False
                self.indice_secuencia += 1

    def ejecutar(self):
        while self.ejecutando:
            dt = self.reloj.tick(self.fps_objetivo) / 1000.0
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.ejecutando = False
                
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    self.manejar_clic(evento.pos)

            # Restar tiempo solo si el jugador tiene el control
            if self.estado_actual == "JUGANDO":
                self.t_restante -= dt
                if self.t_restante <= 0:
                    self.t_restante = 0
                    self.estado_actual = "GAME_OVER"

            if self.estado_actual == "MOSTRANDO_SECUENCIA":
                self.procesar_animacion()
            
            self.dibujar()
            pygame.display.flip()

    def error_debe_penalizar(self):
        if not hasattr(self, "personaje_actual") or self.personaje_actual is None:
            return True

        if getattr(self.personaje_actual, "nombre", "") == "Neru":
            escudo_activo = getattr(self, "bloquear_penalizacion", False) or getattr(self, "primer_error_protegido", False) or getattr(self, "escudo_activo", False)
            if escudo_activo:
                self.bloquear_penalizacion = False
                self.primer_error_protegido = False
                self.escudo_activo = False
                self.personaje_actual.escudo_activo = False
                self.mensaje = "Escudo de Neru activado"
                return False

        return True

    def manejar_clic(self, pos):
        if self.estado_actual == "MENU":
            self.estado_actual = "SELECCION"
            
        elif self.estado_actual == "SELECCION":
            if self.rect_miku.collidepoint(pos):
                self.personaje_actual = Miku()
                self.preparar_juego()
            elif self.rect_teto.collidepoint(pos):
                self.personaje_actual = Teto()
                self.preparar_juego()
            elif self.rect_neru.collidepoint(pos):
                self.personaje_actual = Neru()
                self.preparar_juego()
            elif self.rect_gumi.collidepoint(pos):
                self.personaje_actual = Gumi()
                self.preparar_juego()
                
        elif self.estado_actual == "JUGANDO":
            self.personaje_actual.aplicar_habilidad(self)
            
            for numero, rect in self.rects_botones.items():
                if rect.collidepoint(pos):
                    resultado = self.gestor_secuencia.verificar_color(numero)
                    if resultado == "ERROR":
                        if self.error_debe_penalizar():
                            self.t_restante -= 2.0
                            if self.t_restante <= 0:
                                self.estado_actual = "GAME_OVER"
                            else:
                                self.mensaje = "¡Error! Repitiendo (-2s)"
                                self.iniciar_animacion()
                        else:
                            self.mensaje = "¡Escudo de Neru!"
                            self.iniciar_animacion()
                    elif resultado == "EXITO":
                        self.gestor_puntuacion.agregar_por_ronda(
                            self.t_restante, 
                            self.gestor_secuencia.consultar_nivel() - 1, 
                            self.personaje_actual.multiplicador_puntaje
                        )
                        self.mensaje = "¡Siguiente nivel!"
                        self.preparar_juego()
                    break

            if self.rect_reinicio.collidepoint(pos):
                self.gestor_secuencia.reiniciar_progreso()
                self.estado_actual = "SELECCION"

        elif self.estado_actual == "GAME_OVER":
            if self.rect_reinicio.collidepoint(pos):
                self.gestor_secuencia.reiniciar_progreso()
                self.gestor_puntuacion.reset()
                self.estado_actual = "SELECCION"

    def dibujar(self):
        self.pantalla.fill((189, 189, 189))
        
        if self.estado_actual == "MENU":
            self.pantalla.blit(self.fuente_titulo.render("SIMON GAME", True, (0,0,0)), (150, 200))
            self.pantalla.blit(self.fuente_normal.render("Haz clic para iniciar", True, (50,50,50)), (200, 300))
            
        elif self.estado_actual == "SELECCION":
            self.pantalla.blit(self.fuente_titulo.render("ELEGIR PERSONAJE", True, (0,0,0)), (70, 100))
            for rect in (self.rect_miku, self.rect_teto, self.rect_neru, self.rect_gumi):
                pygame.draw.rect(self.pantalla, (255,255,255), rect)

            self.pantalla.blit(self.fuente_normal.render("Miku", True, (0,0,0)), (95, 270))
            self.pantalla.blit(self.fuente_normal.render("Teto", True, (0,0,0)), (235, 270))
            self.pantalla.blit(self.fuente_normal.render("Neru", True, (0,0,0)), (375, 270))
            self.pantalla.blit(self.fuente_normal.render("Gumi", True, (0,0,0)), (515, 270))
            if self.gestor_puntuacion.total > 0:
                self.pantalla.blit(self.fuente_normal.render(f"Último Puntaje: {self.gestor_puntuacion.total}", True, (0,0,0)), (180, 450))

        elif self.estado_actual in ["MOSTRANDO_SECUENCIA", "JUGANDO"]:
            self.pantalla.blit(self.fuente_normal.render(f"Puntaje: {self.gestor_puntuacion.total}", True, (0,0,0)), (20, 20))
            self.pantalla.blit(self.fuente_normal.render(f"Tiempo: {max(0, self.t_restante):.1f}s", True, (0,0,0)), (20, 50))
            self.pantalla.blit(self.fuente_normal.render(self.mensaje, True, (0,100,0)), (200, 20))
            
            for numero, rect in self.rects_botones.items():
                color = self.colores_brillantes[numero] if self.color_iluminado == numero else self.colores_base[numero]
                pygame.draw.rect(self.pantalla, color, rect)
                pygame.draw.rect(self.pantalla, (0,0,0), rect, 3) # Borde negro

            pygame.draw.rect(self.pantalla, (0,0,0), self.rect_reinicio)
            self.pantalla.blit(self.fuente_normal.render("RESTART", True, (255,255,255)), (245, 560))

        elif self.estado_actual == "GAME_OVER":
            self.pantalla.blit(self.fuente_titulo.render("GAME OVER", True, (200,0,0)), (160, 200))
            self.pantalla.blit(self.fuente_normal.render(f"Puntaje Final: {self.gestor_puntuacion.total}", True, (0,0,0)), (200, 300))
            pygame.draw.rect(self.pantalla, (0,0,0), self.rect_reinicio)
            self.pantalla.blit(self.fuente_normal.render("Volver", True, (255,255,255)), (260, 560))
