import pygame
from paquete.graficos import *
from paquete.funciones import *

# Iniciar pygame
pygame.init()

# Iniciar música de fondo en loop
SONIDOS["musica_fondo"].play(-1)

# Crear pantalla, nombre y reloj
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Solitario")
reloj = pygame.time.Clock()

# Fuente (la usamos tanto en el menú como en el juego)
fuente = pygame.font.SysFont(None, 32)

while True:
    seleccion, _ = mostrar_menu(pantalla, fuente)

    if seleccion == "jugar":
        break  # sale del while y sigue al juego
    elif seleccion == "ranking":
        mostrar_ranking(pantalla, fuente)
    else:
        pygame.quit()
        exit()

# Posición de los botones de control
boton_reiniciar = pygame.Rect(X_BOTON_REINICIAR, Y_BOTON_REINICIAR, ANCHO_BOTON, ALTO_BOTON)
boton_menu = pygame.Rect(X_BOTON_MENU, Y_BOTON_MENU, ANCHO_BOTON, ALTO_BOTON)

# Cargar la imagen del reverso
reverso_img = cargar_imagen_reverso()

# Crear y repartir el mazo
mazo = crear_mazo()
columnas, mazo_restante = repartir_columnas(mazo) 
pila_descubierta = []

# Crear 4 huecos para los Ases
huecos = [
    {"palo": None, "cartas": []},
    {"palo": None, "cartas": []},
    {"palo": None, "cartas": []},
    {"palo": None, "cartas": []}
]

reiniciar_tiempo_y_puntaje()

# While principal
ejecutar = True
while ejecutar:

    reloj.tick(FPS)
    pantalla.fill(VERDE)

    # Manejar eventos del mouse
    manejar_eventos(columnas, pila_descubierta, mazo_restante, huecos, boton_reiniciar, boton_menu, pantalla, fuente)

    # Dibujar todo el tablero
    dibujar_tablero(pantalla, columnas, pila_descubierta, mazo_restante, huecos, estado["carta_seleccionada"], reverso_img)

    # Dibuja los botones reiniciar y menu
    dibujar_botones(pantalla, fuente, boton_reiniciar, boton_menu)

    # Muestra el tiempo
    mostrar_tiempo(pantalla, fuente)

    # Genera la victoria al completarse los 4 huecos
    manejar_victoria(pantalla, fuente, columnas, mazo_restante, pila_descubierta, huecos)

    pygame.display.update()

pygame.quit()