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
        self.fuente_titulo = pygame.font.Font(str(config.archivo_fuente), 48)
        self.fuente_normal = pygame.font.Font(str(config.archivo_fuente), 24)

        directorio_imagenes = config.directorio_base / "assets" / "images"
        nombres_colores = {
            1: "rojo",
            2: "azul",
            3: "verde",
            4: "amarillo",
        }
        tamano_boton_juego = 300
        self.imagenes_botones = {
            numero: {
                "normal": pygame.transform.smoothscale(
                    pygame.image.load(
                        directorio_imagenes / f"asset {nombre} final.png"
                    ).convert_alpha(),
                    (tamano_boton_juego, tamano_boton_juego),
                ),
                "presionado": pygame.transform.smoothscale(
                    pygame.image.load(
                        directorio_imagenes / f"asset {nombre} pressed final.png"
                    ).convert_alpha(),
                    (tamano_boton_juego, tamano_boton_juego),
                ),
            }
            for numero, nombre in nombres_colores.items()
        }

        self.estado_actual = "MENU" # MENU, SELECCION, TRANSICION_NIVEL, MOSTRANDO_SECUENCIA, JUGANDO, GAME_OVER
        
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
        
        centro_juego = self.pantalla.get_rect().center
        inicio_juego_x = centro_juego[0] - 300
        inicio_juego_y = centro_juego[1] - 300
        self.rects_botones = {
            3: pygame.Rect(inicio_juego_x, inicio_juego_y, 300, 300), # Verde (Arriba izquierda)
            2: pygame.Rect(inicio_juego_x + 300, inicio_juego_y, 300, 300), # Azul (Arriba derecha)
            4: pygame.Rect(inicio_juego_x, inicio_juego_y + 300, 300, 300), # Amarillo (Abajo izquierda)
            1: pygame.Rect(inicio_juego_x + 300, inicio_juego_y + 300, 300, 300), # Rojo (Abajo derecha)
        }
        
        centro_x = self.pantalla.get_rect().centerx
        centro_y = self.pantalla.get_rect().centery
        self.rect_iniciar = pygame.Rect(centro_x - 200, centro_y - 35, 400, 70)
        ancho_boton_personaje = 140
        espacio_boton_personaje = 20
        ancho_grupo_personajes = (ancho_boton_personaje * 4) + (espacio_boton_personaje * 3)
        inicio_x = centro_x - (ancho_grupo_personajes // 2)
        y_botones_personaje = centro_y - 30
        self.rect_miku = pygame.Rect(inicio_x, y_botones_personaje, ancho_boton_personaje, 60)
        self.rect_teto = pygame.Rect(inicio_x + ancho_boton_personaje + espacio_boton_personaje, y_botones_personaje, ancho_boton_personaje, 60)
        self.rect_neru = pygame.Rect(inicio_x + (ancho_boton_personaje + espacio_boton_personaje) * 2, y_botones_personaje, ancho_boton_personaje, 60)
        self.rect_gumi = pygame.Rect(inicio_x + (ancho_boton_personaje + espacio_boton_personaje) * 3, y_botones_personaje, ancho_boton_personaje, 60)
        posicion_lateral_x = self.pantalla.get_rect().right - 230
        self.rect_reinicio = pygame.Rect(posicion_lateral_x, centro_y - 55, 200, 50)
        self.rect_volver = pygame.Rect(posicion_lateral_x, centro_y + 5, 200, 50)

        self.t_total = 10.0
        self.t_restante = 10.0
        self.mensaje = "Listo"
        
        # Variables para la animación de parpadeo de secuencia
        self.color_iluminado = None
        self.indice_secuencia = 0
        self.tiempo_ultimo_cambio = 0
        self.luz_encendida = False
        self.boton_presionado = None
        self.tiempo_boton_presionado = 0
        self.tiempo_espera_transicion = 0
        self.tiempo_transicion_nivel = 0

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

    def iniciar_transicion_nivel(self):
        self.estado_actual = "TRANSICION_NIVEL"
        self.tiempo_transicion_nivel = pygame.time.get_ticks()

    def iniciar_espera_transicion(self):
        self.estado_actual = "ESPERANDO_TRANSICION"
        self.tiempo_espera_transicion = pygame.time.get_ticks() + 150

    def procesar_espera_transicion(self):
        if pygame.time.get_ticks() >= self.tiempo_espera_transicion:
            self.iniciar_transicion_nivel()

    def procesar_transicion_nivel(self):
        tiempo_transcurrido = (pygame.time.get_ticks() - self.tiempo_transicion_nivel) / 1000
        if tiempo_transcurrido >= 3.3:
            self.preparar_juego()

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
                    self.gestor_secuencia.reiniciar_progreso()
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

            if self.estado_actual == "TRANSICION_NIVEL":
                self.procesar_transicion_nivel()

            if self.estado_actual == "ESPERANDO_TRANSICION":
                self.procesar_espera_transicion()

            if self.boton_presionado is not None and pygame.time.get_ticks() >= self.tiempo_boton_presionado:
                self.boton_presionado = None
            
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
            if self.rect_iniciar.collidepoint(pos):
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
                    self.boton_presionado = numero
                    self.tiempo_boton_presionado = pygame.time.get_ticks() + 150
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
                        self.mensaje = "¡¡Siguiente nivel!!"
                        self.iniciar_espera_transicion()
                    break

            if self.rect_reinicio.collidepoint(pos):
                self.gestor_secuencia.reiniciar_progreso()
                self.estado_actual = "SELECCION"
            elif self.rect_volver.collidepoint(pos):
                self.gestor_secuencia.reiniciar_progreso()
                self.gestor_puntuacion.reset()
                self.estado_actual = "MENU"

        elif self.estado_actual == "GAME_OVER":
            if self.rect_reinicio.collidepoint(pos):
                self.gestor_secuencia.reiniciar_progreso()
                self.gestor_puntuacion.reset()
                self.estado_actual = "SELECCION"
            elif self.rect_volver.collidepoint(pos):
                self.gestor_secuencia.reiniciar_progreso()
                self.gestor_puntuacion.reset()
                self.estado_actual = "MENU"

    def dibujar_texto_centrado(self, texto, fuente, color, centro):
        superficie = fuente.render(texto, True, color)
        rect_texto = superficie.get_rect(center=centro)
        self.pantalla.blit(superficie, rect_texto)

    def dibujar_boton(self, rect, texto, color_fondo=(255, 255, 255), color_texto=(0, 0, 0)):
        pygame.draw.rect(self.pantalla, color_fondo, rect)
        pygame.draw.rect(self.pantalla, (0, 0, 0), rect, 2)
        self.dibujar_texto_centrado(texto, self.fuente_normal, color_texto, rect.center)

    def dibujar_texto_lateral(self, texto, fuente, color, y, lado):
        superficie = fuente.render(texto, True, color)
        if lado == "izquierda":
            rect_texto = superficie.get_rect(topleft=(30, y))
        else:
            rect_texto = superficie.get_rect(topright=(self.pantalla.get_rect().right - 30, y))
        self.pantalla.blit(superficie, rect_texto)

    def dibujar_transicion_nivel(self):
        tiempo_transcurrido = (pygame.time.get_ticks() - self.tiempo_transicion_nivel) / 1000
        panel = pygame.Surface((460, 190), pygame.SRCALPHA)
        panel.fill((20, 20, 20, 230))
        rect_panel = panel.get_rect(center=self.pantalla.get_rect().center)
        self.pantalla.blit(panel, rect_panel)

        if tiempo_transcurrido < 1:
            texto = "¡¡Siguiente nivel!!"
            fuente = self.fuente_normal
        elif tiempo_transcurrido < 2.5:
            texto = str(3 - int((tiempo_transcurrido - 1) / 0.5))
            fuente = self.fuente_titulo
        else:
            texto = "¡¡VAMOS!!"
            fuente = self.fuente_titulo

        self.dibujar_texto_centrado(texto, fuente, (255, 255, 255), rect_panel.center)

    def dibujar(self):
        self.pantalla.fill((189, 189, 189))
        
        if self.estado_actual == "MENU":
            centro_x = self.pantalla.get_rect().centerx
            centro_y = self.pantalla.get_rect().centery
            self.dibujar_texto_centrado("VoColoroid", self.fuente_titulo, (0, 0, 0), (centro_x, centro_y - 100))
            self.dibujar_boton(self.rect_iniciar, "Haz clic para iniciar", (255, 255, 255), (50, 50, 50))
            
        elif self.estado_actual == "SELECCION":
            centro_x = self.pantalla.get_rect().centerx
            centro_y = self.pantalla.get_rect().centery
            self.dibujar_texto_centrado("ELEGIR PERSONAJE", self.fuente_titulo, (0, 0, 0), (centro_x, centro_y - 100))
            for rect, nombre in (
                (self.rect_miku, "Miku"),
                (self.rect_teto, "Teto"),
                (self.rect_neru, "Neru"),
                (self.rect_gumi, "Gumi"),
            ):
                self.dibujar_boton(rect, nombre)
            if self.gestor_puntuacion.total > 0:
                limite_inferior_botones = max(
                    rect.bottom for rect in (self.rect_miku, self.rect_teto, self.rect_neru, self.rect_gumi)
                )
                self.dibujar_texto_centrado(
                    f"Último Puntaje: {self.gestor_puntuacion.total}",
                    self.fuente_normal,
                    (0, 0, 0),
                    (centro_x, limite_inferior_botones + 60),
                )

        elif self.estado_actual in ["MOSTRANDO_SECUENCIA", "JUGANDO"]:
            self.dibujar_texto_lateral(
                f"Puntaje: {self.gestor_puntuacion.total}",
                self.fuente_normal,
                (0, 0, 0),
                30,
                "izquierda",
            )
            self.dibujar_texto_lateral(
                f"Tiempo: {max(0, self.t_restante):.1f}s",
                self.fuente_normal,
                (0, 0, 0),
                65,
                "izquierda",
            )
            self.dibujar_texto_lateral(self.mensaje, self.fuente_normal, (0, 100, 0), 30, "derecha")
            
            for numero, rect in self.rects_botones.items():
                esta_presionado = (
                    self.color_iluminado == numero
                    or self.boton_presionado == numero
                )
                tipo_imagen = "presionado" if esta_presionado else "normal"
                self.pantalla.blit(self.imagenes_botones[numero][tipo_imagen], rect)

            pygame.draw.rect(self.pantalla, (0,0,0), self.rect_reinicio)
            self.dibujar_texto_centrado("REINICIAR", self.fuente_normal, (255, 255, 255), self.rect_reinicio.center)
            pygame.draw.rect(self.pantalla, (0,0,0), self.rect_volver)
            self.dibujar_texto_centrado("VOLVER", self.fuente_normal, (255, 255, 255), self.rect_volver.center)

        elif self.estado_actual == "TRANSICION_NIVEL":
            for numero, rect in self.rects_botones.items():
                tipo_imagen = "presionado" if self.color_iluminado == numero else "normal"
                self.pantalla.blit(self.imagenes_botones[numero][tipo_imagen], rect)
            self.dibujar_transicion_nivel()

        elif self.estado_actual == "ESPERANDO_TRANSICION":
            for numero, rect in self.rects_botones.items():
                tipo_imagen = "presionado" if self.boton_presionado == numero else "normal"
                self.pantalla.blit(self.imagenes_botones[numero][tipo_imagen], rect)

        elif self.estado_actual == "GAME_OVER":
            centro_x = self.pantalla.get_rect().centerx
            self.dibujar_texto_centrado("GAME OVER", self.fuente_titulo, (200, 0, 0), (centro_x, 200))
            self.dibujar_texto_lateral(
                f"Puntaje Final: {self.gestor_puntuacion.total}",
                self.fuente_normal,
                (0, 0, 0),
                300,
                "derecha",
            )
            pygame.draw.rect(self.pantalla, (0,0,0), self.rect_reinicio)
            self.dibujar_texto_centrado("REINICIAR", self.fuente_normal, (255, 255, 255), self.rect_reinicio.center)
            pygame.draw.rect(self.pantalla, (0,0,0), self.rect_volver)
            self.dibujar_texto_centrado("VOLVER", self.fuente_normal, (255, 255, 255), self.rect_volver.center)
