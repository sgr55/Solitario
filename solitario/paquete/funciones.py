import pygame
import random
import time
from .graficos import *

# Diccionario global estado:
estado = {
    "carta_seleccionada": None,
    "sonido_activado": True,
    "grupo_seleccionado": [],
    "tiempo_inicio": time.time(),
    "puntaje": 1000  # sistema base de puntos
}

# Inicia la fuente para mostrar texto y la pantalla
pygame.font.init()
fuente = pygame.font.SysFont(None, 32)
pantalla = pygame.display.set_mode((ANCHO, ALTO))

# Palos usados en la baraja del juego
PALOS = ("basto", "copa", "espada", "oro")

# Diccionario que guarda el estado global del juego
estado = {
    "carta_seleccionada": None, # Carta que está seleccionada (si hay)
    "sonido_activado": True,    # Indica si el sonido está activado
    "grupo_seleccionado": []    # Grupo de cartas seleccionadas (por ejemplo, pila que se quiere mover)
}

# Muestra el menú principal del juego y devuelve la selección del usuario.
def mostrar_menu(pantalla, fuente):

    seleccion = None
    while seleccion is None:

        pantalla.fill(VERDE)
        textos = dibujar_textos_menu(pantalla, fuente)
        pygame.display.update()

        seleccion = manejar_eventos_menu(textos)
        
        if seleccion in ["jugar", "ranking"]:
            return seleccion, estado["sonido_activado"]

# Renderiza y dibuja los textos del menú principal.
def dibujar_textos_menu(pantalla, fuente):

    titulo = fuente.render("SOLITARIO", True, BLANCO)
    opcion_jugar = fuente.render("JUGAR", True, BLANCO)
    opcion_ranking = fuente.render("VER RANKING", True, BLANCO)

    texto_sonido = "DESACTIVAR SONIDO" if estado["sonido_activado"] else "ACTIVAR SONIDO"
    opcion_sonido = fuente.render(texto_sonido, True, BLANCO)

    pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, Y_TITULO))
    pantalla.blit(opcion_jugar, (ANCHO // 2 - opcion_jugar.get_width() // 2, Y_JUGAR))
    pantalla.blit(opcion_ranking, (ANCHO // 2 - opcion_ranking.get_width() // 2, Y_RANKING))
    pantalla.blit(opcion_sonido, (ANCHO // 2 - opcion_sonido.get_width() // 2, Y_SONIDO))

    return {
        "jugar": (opcion_jugar, (ANCHO // 2 - opcion_jugar.get_width() // 2, Y_JUGAR)),
        "ranking": (opcion_ranking, (ANCHO // 2 - opcion_ranking.get_width() // 2, Y_RANKING)),
        "sonido": (opcion_sonido, (ANCHO // 2 - opcion_sonido.get_width() // 2, Y_SONIDO))
    }

# Maneja los eventos del menú principal.
def manejar_eventos_menu(textos):

    for evento in pygame.event.get():
         
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()

        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            x, y = evento.pos
            
            for opcion, (superficie, topleft) in textos.items():

                rect = superficie.get_rect(topleft=topleft)

                if rect.collidepoint(x, y):
                    reproducir_sonido("click")

                    if opcion == "sonido":
                        alternar_sonido()
                        return None  # vuelve a dibujar con el nuevo estado

                    return opcion

    return None

# Crea una carta a partir del nombre del archivo y su posición
def crear_carta(ruta_imagen: str, x: int, y: int) -> dict:

    carta = {}

    # Carga la imagen desde la carpeta de recursos
    ruta = "recursos/cartas/" + ruta_imagen
    img = pygame.image.load(ruta)
    img = pygame.transform.scale(img, (ANCHO_CARTA, ALTO_CARTA))

    # Guarda la imagen en el diccionario y su posición en pantalla
    carta["superficie"] = img
    carta["rect"] = pygame.Rect(x, y, ANCHO_CARTA, ALTO_CARTA)

    # Si no es el reverso, se le extraen el número y el palo desde el nombre del archivo
    if ruta_imagen != "reverso.png":
        partes = ruta_imagen.replace(".jpg", "").replace(".png", "").split("_")
        carta["numero"] = int(partes[0])
        carta["palo"] = partes[1]
    else:
        carta["numero"] = None
        carta["palo"] = None

    # Por defecto, las cartas se crean boca abajo
    carta["visible"] = False

    return carta

# Crea una nueva carta igual a otra, con rect en nueva posición
def duplicar_carta(carta_origen, x, y):

    """Crea una nueva carta igual a otra, con rect en nueva posición"""
    # Usa el número y palo de la carta original para volver a crearla
    ruta_imagen = f"{carta_origen['numero']}_{carta_origen['palo']}.jpg"
    nueva_carta = crear_carta(ruta_imagen, x, y)
    nueva_carta["visible"] = True  # Las duplicadas siempre se muestran
    return nueva_carta

# Carga la imagen del reverso de las cartas
def cargar_imagen_reverso():

    ruta = "recursos/cartas/reverso.png"
    img = pygame.image.load(ruta)
    img = pygame.transform.scale(img, (ANCHO_CARTA, ALTO_CARTA))

    return img

# Crea y baraja un mazo de 40 cartas (1 al 10 por palo)
def crear_mazo() -> list:

    mazo = []
    for palo in PALOS:
        for n in range(1, 11):
            archivo = f"{n}_{palo}.jpg"
            carta = crear_carta(archivo, 0, 0)  # Se crean en (0,0), luego se ubican al repartir
            mazo.append(carta)

    random.shuffle(mazo)  # Mezcla las cartas al azar

    return mazo

# Distribuye las cartas del mazo en 7 columnas, dejando la última carta de cada columna visible
def repartir_columnas(mazo):

    columnas = [[] for _ in range(7)]  # Se crean 7 columnas vacías

    # Coordenadas iniciales para ubicar las columnas en pantalla
    x_inicial = X_COLUMNAS
    y_inicial = Y_COLUMNAS
    espacio_horizontal = ESPACIO_COLUMNAS
    espacio_vertical = ESPACIO_VERTICAL_CARTAS

    index = 0  # Índice para recorrer las cartas del mazo

    for i in range(7):  # Para cada columna
        for j in range(i + 1):  # Se colocan i+1 cartas en la columna i
            carta = mazo[index]
            carta["rect"] = pygame.Rect(
                x_inicial + i * espacio_horizontal,
                y_inicial + j * espacio_vertical,
                ANCHO_CARTA, ALTO_CARTA
            )
            carta["visible"] = (j == i)  # Solo la última carta se muestra
            columnas[i].append(carta)
            index += 1

    # Lo que sobra del mazo se devuelve como mazo restante
    mazo_restante = mazo[index:]

    return columnas, mazo_restante

#Elimina una carta desde su lugar original (mazo o columna), y si corresponde, da vuelta la carta que queda expuesta.
def eliminar_carta_de_origen(carta, pila_descubierta, columnas):

    # Si estaba en la pila descubierta del mazo
    if carta in pila_descubierta:
        pila_descubierta.remove(carta)
        return

    # Si estaba en una de las columnas
    for columna in columnas:
        if carta in columna:
            idx = columna.index(carta)
            del columna[idx:]  # Se elimina la carta y todas las que están encima de ella

            # Si queda alguna carta oculta, se da vuelta
            if len(columna) > 0 and not columna[-1]["visible"]:
                columna[-1]["visible"] = True
            break

    # Reorganiza las posiciones verticales de las cartas
    reordenar_columnas(columnas)

# Ajusta visualmente las posiciones y separación en las columnas
def reordenar_columnas(columnas):

    y_base = Y_COLUMNAS
    for columna in columnas:
        y = y_base
        for carta in columna:
            carta["rect"].y = y
            y += ESPACIO_VERTICAL_CARTAS

# Maneja todos los eventos del juego (clics del mouse, cerrar ventana, botones, etc.)
def manejar_eventos(columnas, pila_descubierta, mazo_restante, huecos, boton_reiniciar, boton_menu, pantalla, fuente):

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()

        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            x, y = evento.pos  # Coordenadas del clic del mouse

            # Verifica si se hizo clic en alguno de los dos botones (reinicio o menú)
            if procesar_botones(x, y, columnas, pila_descubierta, mazo_restante, huecos, boton_reiniciar, boton_menu, pantalla, fuente):
                return  # Si se usó algún botón, se sale del ciclo

            # Verifica si se hizo clic sobre el mazo
            if procesar_mazo(x, y, mazo_restante, pila_descubierta, columnas, huecos, pantalla, boton_reiniciar, boton_menu, fuente):
                return

            # Si había una carta seleccionada, intenta soltarla en algún lugar
            if procesar_soltar(x, y, columnas, pila_descubierta, huecos, pantalla, mazo_restante, boton_reiniciar, boton_menu, fuente):
                return

            # Si no había ninguna carta seleccionada, intenta seleccionar una
            if procesar_seleccion(x, y, columnas, pila_descubierta):
                return

            # Si no hizo clic sobre nada, se deselecciona todo
            deseleccionar()

# Procesa los clics sobre los botones de "reiniciar" o "menu"
def procesar_botones(x, y, columnas, pila_descubierta, mazo_restante, huecos, boton_reiniciar, boton_menu, pantalla, fuente):

    if boton_reiniciar.collidepoint(x, y):
        reiniciar_juego(columnas, pila_descubierta, mazo_restante, huecos)
        reproducir_sonido("click")

        return True
    
    elif boton_menu.collidepoint(x, y):
        reproducir_sonido("click")
        while True:
                seleccion, _ = mostrar_menu(pantalla, fuente)

                if seleccion == "ranking":
                    reproducir_sonido("click")
                    mostrar_ranking(pantalla, fuente)
                    pygame.event.clear()  # arregla el bug de los 2 clicss
                    # Luego de ver el ranking, vuelve al menú otra vez
                    continue

                elif seleccion == "jugar":
                    # Volvió a elegir jugar, entonces reiniciamos y salimos del ciclo
                    reiniciar_juego(columnas, pila_descubierta, mazo_restante, huecos)
                    return True
    
    return False

# Procesa los clics sobre el mazo (donde están las cartas boca abajo)
def procesar_mazo(x, y, mazo_restante, pila_descubierta, columnas, huecos, pantalla, boton_reiniciar, boton_menu, fuente):
    mazo_rect = pygame.Rect(X_MAZO, Y_MAZO, ANCHO_CARTA, ALTO_CARTA)
    if mazo_rect.collidepoint(x, y):
        estado["carta_seleccionada"] = None
        estado["grupo_seleccionado"] = []

        if mazo_restante:
            carta = mazo_restante.pop()
            # ¡Ajuste clave! Posición inicial: el mazo
            carta["rect"].x = X_MAZO
            carta["rect"].y = Y_MAZO
            destino_x = X_MAZO + ANCHO_CARTA + DESPLAZAMIENTO_PILA_DESCUBIERTA
            destino_y = Y_MAZO
            carta["boca_abajo"] = False
            carta["visible"] = True
            animar_movimiento(carta, destino_x, destino_y, pantalla, columnas, mazo_restante, pila_descubierta, huecos, fuente, boton_reiniciar, boton_menu)
            nueva_carta = duplicar_carta(carta, destino_x, destino_y)
            nueva_carta["boca_abajo"] = False
            nueva_carta["visible"] = True
            pila_descubierta.append(nueva_carta)
            reproducir_sonido("mover")
        elif pila_descubierta:
            # Reinicia el mazo con las cartas de la pila descubierta (en orden inverso)
            while pila_descubierta:
                carta = pila_descubierta.pop()
                carta["rect"].x = X_MAZO
                carta["rect"].y = Y_MAZO
                carta["boca_abajo"] = True
                mazo_restante.append(carta)
            reproducir_sonido("barajar")
        return True
    return False

# Si hay una carta seleccionada, intenta soltarla en algún lugar válido
def procesar_soltar(x, y, columnas, pila_descubierta, huecos, pantalla, mazo_restante, boton_reiniciar, boton_menu, fuente):
    carta = estado.get("carta_seleccionada")
    if carta is None:
        return False

    grupo = estado.get("grupo_seleccionado", [carta])

    if soltar_en_huecos(carta, grupo, x, y, huecos, pila_descubierta, columnas, pantalla, mazo_restante, boton_reiniciar, boton_menu, fuente):
        return True

    if soltar_en_columnas(carta, grupo, x, y, columnas, pila_descubierta, pantalla, mazo_restante, huecos, boton_reiniciar, boton_menu, fuente):
        return True

    if carta["rect"].collidepoint(x, y):
        deseleccionar()
        return True

    return False

# Intenta colocar una carta en los huecos superiores (donde se apilan por palo)
def soltar_en_huecos(carta, grupo, x, y, huecos, pila_descubierta, columnas, pantalla, mazo_restante, boton_reiniciar, boton_menu, fuente):
    if len(grupo) > 1:
        return False

    for i, hueco in enumerate(huecos):
        hx = X_HUECOS + i * ESPACIO_HUECOS
        rect = pygame.Rect(hx, Y_HUECOS, ANCHO_CARTA, ALTO_CARTA)

        if rect.collidepoint(x, y):
            if hueco["palo"] is None and carta["numero"] == 1:
                animar_movimiento(carta, hx, Y_HUECOS, pantalla, columnas, mazo_restante, pila_descubierta, huecos, fuente, boton_reiniciar, boton_menu)
                hueco["palo"] = carta["palo"]
                hueco["cartas"].append(duplicar_carta(carta, hx, Y_HUECOS))
                reproducir_sonido("hueco")
                eliminar_carta_de_origen(carta, pila_descubierta, columnas)
                deseleccionar()
                return True

            elif hueco["palo"] == carta["palo"] and carta["numero"] == hueco["cartas"][-1]["numero"] + 1:
                animar_movimiento(carta, hx, Y_HUECOS, pantalla, columnas, mazo_restante, pila_descubierta, huecos, fuente, boton_reiniciar, boton_menu)
                hueco["cartas"].append(duplicar_carta(carta, hx, Y_HUECOS))
                reproducir_sonido("hueco")
                eliminar_carta_de_origen(carta, pila_descubierta, columnas)
                deseleccionar()
                return True

    return False

# Intenta colocar una carta sobre otra en una columna (o en una columna vacía)
def soltar_en_columnas(carta, grupo, x, y, columnas, pila_descubierta, pantalla, mazo_restante, huecos, boton_reiniciar, boton_menu, fuente):
    for i, columna in enumerate(columnas):
        x_col = X_COLUMNAS + i * ESPACIO_COLUMNAS
        y_col = Y_COLUMNAS
        rect = pygame.Rect(x_col, y_col, ANCHO_CARTA, ALTO_CARTA)

        if columna:
            destino = columna[-1]
            if destino["rect"].collidepoint(x, y) and carta["numero"] == destino["numero"] - 1 and carta["palo"] != destino["palo"]:
                nueva_y = destino["rect"].y + ESPACIO_VERTICAL_CARTAS

                # Mueve el grupo como bloque
                animar_movimiento_grupo(grupo, destino["rect"].x, nueva_y, pantalla, columnas, mazo_restante, pila_descubierta, huecos, fuente, boton_reiniciar, boton_menu)
                for carta_mover in grupo:
                    columna.append(duplicar_carta(carta_mover, destino["rect"].x, nueva_y))
                    nueva_y += ESPACIO_VERTICAL_CARTAS

                reproducir_sonido("mover")
                eliminar_carta_de_origen(grupo[0], pila_descubierta, columnas)
                deseleccionar()
                return True

        elif rect.collidepoint(x, y) and carta["numero"] == 10:
            nueva_y = y_col

            # Mueve el grupo como bloque
            animar_movimiento_grupo(grupo, x_col, nueva_y, pantalla, columnas, mazo_restante, pila_descubierta, huecos, fuente, boton_reiniciar, boton_menu)
            for carta_mover in grupo:
                columna.append(duplicar_carta(carta_mover, x_col, nueva_y))
                nueva_y += ESPACIO_VERTICAL_CARTAS

            reproducir_sonido("mover")
            eliminar_carta_de_origen(grupo[0], pila_descubierta, columnas)
            deseleccionar()
            return True

    return False
# Si no hay ninguna carta seleccionada, intenta seleccionar una
def procesar_seleccion(x, y, columnas, pila_descubierta):

    if pila_descubierta:
        carta = pila_descubierta[-1]
        if carta["rect"].collidepoint(x, y):
            estado["carta_seleccionada"] = carta
            estado["grupo_seleccionado"] = [carta]

            return True

    for columna in columnas:
        for i in range(len(columna) - 1, -1, -1):
            carta = columna[i]

            if carta["visible"] and carta["rect"].collidepoint(x, y):
                estado["carta_seleccionada"] = carta
                estado["grupo_seleccionado"] = columna[i:]

                return True
            
    return False

# Deselecciona cualquier carta que esté seleccionada
def deseleccionar():

    estado["carta_seleccionada"] = None
    estado["grupo_seleccionado"] = []

# Reinicia todo el juego (se usa en el botón de reinicio o al volver del menú)
def reiniciar_juego(columnas, pila_descubierta, mazo_restante, huecos):

    mazo = crear_mazo()
    nuevas_columnas, nuevas_reserva = repartir_columnas(mazo)
    columnas[:] = nuevas_columnas
    mazo_restante[:] = nuevas_reserva
    pila_descubierta.clear()

    for hueco in huecos:
        hueco["palo"] = None
        hueco["cartas"].clear()
    deseleccionar()
    reiniciar_tiempo_y_puntaje()

# Dibuja una carta en pantalla (visible o no)
def dibujar_carta(pantalla, carta, reverso_img, seleccionada):

    if carta["visible"]:
        pantalla.blit(carta["superficie"], carta["rect"])

        if carta is seleccionada:
            pygame.draw.rect(pantalla, AMARILLO, carta["rect"], 4)
    else:
        pantalla.blit(reverso_img, carta["rect"])

# Dibuja una columna (cartas y su hueco si está vacía)
def dibujar_columna(pantalla, columna, indice, reverso_img):

    x = X_COLUMNAS + indice * ESPACIO_COLUMNAS
    y = Y_COLUMNAS
    
    if len(columna) == 0:
        pygame.draw.rect(pantalla, GRIS, (x, y, ANCHO_CARTA, ALTO_CARTA), 2)
    else:
        for carta in columna:
            dibujar_carta(pantalla, carta, reverso_img, estado["carta_seleccionada"])

# Dibuja el mazo (cerrado o vacío)
def dibujar_mazo(pantalla, mazo_restante, reverso_img):

    rect = pygame.Rect(X_MAZO, Y_MAZO, ANCHO_CARTA, ALTO_CARTA)

    if len(mazo_restante) > 0:
        pantalla.blit(reverso_img, rect)
    else:
        pygame.draw.rect(pantalla, GRIS, rect, 2)

# Dibuja la pila descubierta (última carta visible del mazo)
def dibujar_pila_descubierta(pantalla, pila_descubierta, reverso_img, seleccionada):
    
    if len(pila_descubierta) > 0:
        carta = pila_descubierta[-1]
        pantalla.blit(carta["superficie"], carta["rect"])

        if carta is seleccionada:
            pygame.draw.rect(pantalla, AMARILLO, carta["rect"], 4)

# Dibuja los huecos superiores (para los palos ordenados)
def dibujar_huecos(pantalla, huecos):

    for i, hueco in enumerate(huecos):
        x = X_HUECOS + i * ESPACIO_HUECOS
        rect = pygame.Rect(x, Y_HUECOS, ANCHO_CARTA, ALTO_CARTA)

        if len(hueco["cartas"]) == 0:
            pygame.draw.rect(pantalla, GRIS, rect, 2)
        else:
            carta = hueco["cartas"][-1]
            pantalla.blit(carta["superficie"], rect)

# Dibuja todo el tablero en pantalla
def dibujar_tablero(pantalla, columnas, pila_descubierta, mazo_restante, huecos, seleccionada, reverso_img):

    for i, columna in enumerate(columnas):
        dibujar_columna(pantalla, columna, i, reverso_img)

    dibujar_mazo(pantalla, mazo_restante, reverso_img)
    dibujar_pila_descubierta(pantalla, pila_descubierta, reverso_img, seleccionada)
    dibujar_huecos(pantalla, huecos)

# Dibuja los botones superiores
def dibujar_botones(pantalla, fuente, boton_reiniciar, boton_menu):

    # Dibujar los botones como rectángulos azules
    pygame.draw.rect(pantalla, AZUL, boton_reiniciar)
    pygame.draw.rect(pantalla, AZUL, boton_menu)

    # Crear el texto a mostrar
    texto_reiniciar = fuente.render("Reiniciar", True, BLANCO)
    texto_menu = fuente.render("Menú", True, BLANCO)

    # Posicionar los textos usando márgenes definidos en constantes
    pantalla.blit(texto_reiniciar, (boton_reiniciar.x + MARGEN_TEXTO_X, boton_reiniciar.y + MARGEN_TEXTO_Y))
    pantalla.blit(texto_menu, (boton_menu.x + MARGEN_TEXTO_X, boton_menu.y + MARGEN_TEXTO_Y))

# Reproduce un sonido específico si el sonido está activado
def reproducir_sonido(nombre):

    if estado.get("sonido_activado", True):
        if nombre in SONIDOS:
            SONIDOS[nombre].play()

# Alterna el sonido entre activado y desactivado
def alternar_sonido():

    estado["sonido_activado"] = not estado["sonido_activado"]

    if estado["sonido_activado"]:
        SONIDOS["musica_fondo"].play(-1)  # Loop infinito
    else:
        SONIDOS["musica_fondo"].stop()

# Verifica los 4 huecos estén completos con 10 cartas.
def verificar_victoria(huecos):

    for hueco in huecos:
        if len(hueco["cartas"]) < 10:
            return False
    return True

# Muestra una pantalla de victoria cuando el jugador gana.
def mostrar_victoria(pantalla, fuente):

    pantalla.fill(VERDE)
    
    texto = fuente.render("¡Ganaste!", True, AMARILLO)
    instruccion = fuente.render("Presioná click para volver al menú", True, BLANCO)
    
    pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - 40))
    pantalla.blit(instruccion, (ANCHO // 2 - instruccion.get_width() // 2, ALTO // 2 + 10))
    pygame.display.update()
    
    # Esperar a que se presione una tecla
    esperando = True
    while esperando:

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN or evento.type == pygame.MOUSEBUTTONDOWN:
                esperando = False

# Pausa el juego hasta que el jugador haga clic para continuar.
def esperar_click_continuar():

    esperando = True
    while esperando:

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                esperando = False

# Verifica si se ganó el juego y, si es así, pide nombre, guarda ranking y reinicia todo.
def manejar_victoria(pantalla, fuente, columnas, mazo_restante, pila_descubierta, huecos):

    if verificar_victoria(huecos):
        reproducir_sonido("victoria")
         # Mostrar input de nombre
        nombre = pedir_nombre_ganador(pantalla, fuente)

        # Guardar en ranking
        tiempo_total = int(time.time() - estado["tiempo_inicio"])
        puntaje_final = calcular_puntaje()
        guardar_ranking(nombre, tiempo_total, puntaje_final)

        # Reiniciar todo el juego
        nuevo_mazo = crear_mazo()
        nuevas_columnas, nuevo_mazo_restante = repartir_columnas(nuevo_mazo)

        columnas[:] = nuevas_columnas
        mazo_restante[:] = nuevo_mazo_restante
        pila_descubierta.clear()

        for hueco in huecos:
            hueco["palo"] = None
            hueco["cartas"].clear()

        deseleccionar()
        reiniciar_tiempo_y_puntaje()

# Dibuja el tiempo transcurrido desde que comenzó la partida
def mostrar_tiempo(pantalla, fuente):

    segundos = int(time.time() - estado["tiempo_inicio"])
    texto = fuente.render(f"Tiempo: {segundos}s", True, BLANCO)
    pantalla.blit(texto, (20, ALTO - 40))  # esquina inferior izquierda

# Reiniciar el tiempo y el puntaje
def reiniciar_tiempo_y_puntaje():

    estado["tiempo_inicio"] = time.time()
    estado["puntaje"] = 500

# Resta puntos según el tiempo (cada 5 seg baja 1 punto). Mínimo 100
def calcular_puntaje():

    tiempo = int(time.time() - estado["tiempo_inicio"])
    descuento = tiempo // 1
    return max(10, estado["puntaje"] - descuento)

# Muestra un cuadro de entrada para que el jugador ingrese su nombre tras ganar
def pedir_nombre_ganador(pantalla, fuente):

    nombre = ""
    activo = True

    input_rect = pygame.Rect(ANCHO // 2 - 150, ALTO // 2, 300, 40)
    color_activo = BLANCO
    color_borde = BLANCO

    while activo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    if nombre.strip() != "":
                        activo = False
                elif evento.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                else:
                    if len(nombre) < 20:
                        nombre += evento.unicode

        pantalla.fill(VERDE)

        # Mensaje
        titulo = fuente.render("Ganaste", True, BLANCO)
        subtitulo = fuente.render("Ingresá tu nombre:", True, BLANCO)
        pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, ALTO // 2 - 100))
        pantalla.blit(subtitulo, (ANCHO // 2 - subtitulo.get_width() // 2, ALTO // 2 - 50))

        # Dibujar rectángulo de input
        pygame.draw.rect(pantalla, color_borde, input_rect, 2)
        texto_nombre = fuente.render(nombre, True, color_activo)
        pantalla.blit(texto_nombre, (input_rect.x + 10, input_rect.y + 5))

        pygame.display.update()

    return nombre.strip()

# Guarda los datos del ranking
def guardar_ranking(nombre, tiempo, puntaje):
    archivo = open("recursos/ranking.txt", "a", encoding="utf-8")
    texto = (f"{nombre},{tiempo},{puntaje}\n")
    archivo.write(texto)
    archivo.close()

# Lee el ranking
def leer_ranking():

    ranking = []
    archivo = open("recursos/ranking.txt", "r", encoding="utf-8")
    lineas = archivo.readlines()

    for linea in lineas:

        partes = linea.strip().split(",")

        if len(partes) == 3:
            nombre = partes[0]
            tiempo = int(partes[1])
            puntaje = int(partes[2])
            ranking.append((nombre, tiempo, puntaje))

    archivo.close()

    # Ordenar por puntaje (mayor primero)
    ranking.sort(key=lambda tupla: tupla[2], reverse=True)
    return ranking

# Muestra el ranking en pantalla
def mostrar_ranking(pantalla, fuente):
    pantalla.fill(VERDE)
    datos = leer_ranking()
    titulo = fuente.render("Ranking", True, AMARILLO)
    pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, Y_RANKING_TITULO))

    if len(datos) == 0:
        texto = fuente.render("No hay datos todavía", True, BLANCO)
        pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, Y_RANKING_PRIMERA_LINEA))
    else:
        y = Y_RANKING_PRIMERA_LINEA
        i = 0
        while i < len(datos) and i < 10:
            nombre = datos[i][0]
            tiempo = datos[i][1]
            puntaje = datos[i][2]
            linea = fuente.render(f"{i+1}. {nombre} - Tiempo: {tiempo}s - Puntaje: {puntaje}", True, BLANCO)
            pantalla.blit(linea, (100, y))
            y = y + ESPACIO_LINEA_RANKING
            i = i + 1

    pygame.display.update()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                esperando = False

# Crea las animaciones
def animar_movimiento(carta, x_destino, y_destino, pantalla, columnas, mazo_restante, pila_descubierta, huecos, fuente, boton_reiniciar, boton_menu):
    x_origen, y_origen = carta["rect"].x, carta["rect"].y
    pasos = 15
    dx = (x_destino - x_origen) / pasos
    dy = (y_destino - y_origen) / pasos

    for _ in range(pasos):
        carta["rect"].x += dx
        carta["rect"].y += dy
        pantalla.fill(VERDE)
        dibujar_tablero(pantalla, columnas, pila_descubierta, mazo_restante, huecos, estado["carta_seleccionada"], cargar_imagen_reverso())
        dibujar_botones(pantalla, fuente, boton_reiniciar, boton_menu)
        mostrar_tiempo(pantalla, fuente)
        pantalla.blit(carta["superficie"], carta["rect"])
        pygame.display.update()
        pygame.time.delay(11)
    carta["rect"].x = x_destino
    carta["rect"].y = y_destino

def animar_movimiento_grupo(grupo, x_destino, y_destino, pantalla, columnas, mazo_restante, pila_descubierta, huecos, fuente, boton_reiniciar, boton_menu):
    pasos = 15
    x_origen = grupo[0]["rect"].x
    y_origen = grupo[0]["rect"].y
    dx = (x_destino - x_origen) / pasos
    dy = (y_destino - y_origen) / pasos
    offsets = [carta["rect"].y - y_origen for carta in grupo]

    for _ in range(pasos):
        for i, carta in enumerate(grupo):
            carta["rect"].x += dx
            carta["rect"].y += dy
        pantalla.fill(VERDE)
        dibujar_tablero(pantalla, columnas, pila_descubierta, mazo_restante, huecos, estado["carta_seleccionada"], cargar_imagen_reverso())
        dibujar_botones(pantalla, fuente, boton_reiniciar, boton_menu)
        mostrar_tiempo(pantalla, fuente)
        for i, carta in enumerate(grupo):
            pantalla.blit(carta["superficie"], carta["rect"])
        pygame.display.update()
        pygame.time.delay(11)

    for i, carta in enumerate(grupo):
        carta["rect"].x = x_destino
        carta["rect"].y = y_destino + offsets[i]