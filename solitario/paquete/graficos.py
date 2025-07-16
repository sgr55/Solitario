# Colores
VERDE = (0, 90, 0)
GRIS = (100, 100, 100)
AMARILLO = (255, 255, 0)
BLANCO = (255, 255, 255)
AZUL = (0, 60, 100)

# Dimensiones generales
ANCHO = 1080
ALTO = 720

# FPS
FPS = 30

# Cartas
ANCHO_CARTA = 70
ALTO_CARTA = 120

# Posiciones base
X_HUECOS = 500
Y_HUECOS = 50
ESPACIO_HUECOS = 90

X_MAZO = 50
Y_MAZO = 50

X_COLUMNAS = 235
Y_COLUMNAS = 220
ESPACIO_COLUMNAS = 90
ESPACIO_VERTICAL_CARTAS = 35

DESPLAZAMIENTO_PILA_DESCUBIERTA = 20  # Para que la carta salga a la derecha del mazo

# Posiciones botones menú y reiniciar
MARGEN_TEXTO_X = 10
MARGEN_TEXTO_Y = 10

X_BOTON_REINICIAR = ANCHO - 180
Y_BOTON_REINICIAR = 20

X_BOTON_MENU = ANCHO - 180
Y_BOTON_MENU = 70

ANCHO_BOTON = 140
ALTO_BOTON = 40

# Posiciones menú
Y_TITULO = 100
Y_JUGAR = 250
Y_RANKING = 300
Y_SONIDO = 350

# Ranking
Y_RANKING_TITULO = 50
Y_RANKING_PRIMERA_LINEA = 120
ESPACIO_LINEA_RANKING = 35

# Sonidos
import pygame.mixer

pygame.mixer.init()

SONIDOS = {
    "musica_fondo": pygame.mixer.Sound("recursos/sonidos/musica_fondo.ogg"),
    "click": pygame.mixer.Sound("recursos/sonidos/click.wav"),
    "mover": pygame.mixer.Sound("recursos/sonidos/carta.wav"),
    "barajar": pygame.mixer.Sound("recursos/sonidos/barajar_mazo.wav"),
    "hueco": pygame.mixer.Sound("recursos/sonidos/hueco.wav"),
    "victoria": pygame.mixer.Sound("recursos/sonidos/victoria.wav")
}

# Ajustar volúmenes
SONIDOS["musica_fondo"].set_volume(0.03)
SONIDOS["click"].set_volume(0.1)
SONIDOS["mover"].set_volume(0.6)
SONIDOS["barajar"].set_volume(1.5)
SONIDOS["hueco"].set_volume(0.1)
SONIDOS["victoria"].set_volume(0.1)