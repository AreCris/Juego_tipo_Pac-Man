import pygame
import sys
import random

# Inicializar pygame
pygame.init()

# Configuración de la pantalla
ANCHO, ALTO = 600, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Pac-Man Clone")

# Configuración del jugador y las bolitas
TAMANO_JUGADOR = 35
TAMANO_BOLITA = 8
TAMANO_ENEMIGO = 30
ESCALA_CELDA = 40

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)

# Cargar imágenes
try:
    img_bolita = pygame.image.load('imagenes/bolita.png').convert_alpha()
    img_bolita = pygame.transform.scale(img_bolita, (TAMANO_BOLITA, TAMANO_BOLITA))

    img_player = pygame.image.load('imagenes/player.png').convert_alpha()
    img_player = pygame.transform.scale(img_player, (TAMANO_JUGADOR, TAMANO_JUGADOR))

    img_enemy = pygame.image.load('imagenes/enemy.png').convert_alpha()
    img_enemy = pygame.transform.scale(img_enemy, (TAMANO_ENEMIGO, TAMANO_ENEMIGO))

    img_wall = pygame.image.load('imagenes/wall.png').convert_alpha()
    img_wall = pygame.transform.scale(img_wall, (ESCALA_CELDA, ESCALA_CELDA))

except pygame.error as e:
    print(f"Error al cargar las imágenes: {e}")
    pygame.quit()
    sys.exit()

# Configuración del jugador y bolitas
jugador = pygame.Rect(ESCALA_CELDA, ESCALA_CELDA, TAMANO_JUGADOR, TAMANO_JUGADOR)
bolitas = []
bolitas_especiales = []
enemigos = []
paredes = []

# Mapa del laberinto
laberinto = [
    "############################",
    "#............##............#",
    "#...##.###.#.##.##.#..####.#",
    "#...##.###.#.##.##.#..####.#",
    "#..........................#",
    "#.##.#.##.##..####.##.####.#",
    "#.##.#.##.##..####.##.####.#",
    "#..........................#",
    "#.####.#####....#####. ###.#",
    "#.####.#####.##.#####. ###.#",
    "#............##............#",
    "#.####.#..########.##.#.##.#",
    "#.####.#..########.##.#.##.#",
    "#............##............#",
    "############################",
]

# Configuración de la pantalla y FPS
clock = pygame.time.Clock()
FPS = 60

velocidad_jugador = 3
velocidad_enemigos = 1

# Función para reproducir música
def iniciar_musica():
    try:
        pygame.mixer.music.load('musica/musica.mp3')  # Ruta de la música en la carpeta 'musica'
        pygame.mixer.music.set_volume(0.5)  # Ajusta el volumen de la música (0.0 a 1.0)
        pygame.mixer.music.play(-1, 0.0)  # Reproducir en bucle (-1 indica bucle infinito)
    except pygame.error:
        print("Error al cargar la música. Asegúrate de que el archivo 'musica.mp3' esté en la carpeta correcta.")
        sys.exit()

# Pantalla de inicio
def pantalla_inicio():
    fuente_titulo = pygame.font.Font(None, 74)
    fuente_boton = pygame.font.Font(None, 50)

    while True:
        pantalla.fill((0, 0, 0))

        # Mostrar texto centrado
        titulo_texto = fuente_titulo.render("Pac-Man Clone", True, (255, 255, 0))
        rect_titulo = titulo_texto.get_rect(center=(ANCHO // 2, ALTO // 4))
        pantalla.blit(titulo_texto, rect_titulo)

        boton_rect = pygame.Rect(ANCHO // 2 - 100, ALTO // 2, 200, 50)
        pygame.draw.rect(pantalla, (0, 0, 255), boton_rect)
        iniciar_texto = fuente_boton.render("Iniciar", True, (255, 255, 255))
        rect_iniciar = iniciar_texto.get_rect(center=(ANCHO // 2, ALTO // 2 + 25))
        pantalla.blit(iniciar_texto, rect_iniciar)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_rect.collidepoint(evento.pos):
                    return

        pygame.display.flip()
        clock.tick(FPS)

# Función para mostrar texto
def mostrar_texto(texto, fuente, color, x, y):
    superficie_texto = fuente.render(texto, True, color)
    rect_texto = superficie_texto.get_rect(center=(x, y))
    pantalla.blit(superficie_texto, rect_texto)

# Pantalla de fin de juego
def pantalla_fin(mensaje):
    fuente_titulo = pygame.font.Font(None, 50)
    fuente_boton = pygame.font.Font(None, 50)

    while True:
        pantalla.fill(NEGRO)
        mostrar_texto(mensaje, fuente_titulo, ROJO, ANCHO // 2, ALTO // 4)
        boton_rect = pygame.Rect(ANCHO // 2 - 100, ALTO // 2, 200, 50)
        pygame.draw.rect(pantalla, AZUL, boton_rect)
        mostrar_texto("Reiniciar", fuente_boton, BLANCO, ANCHO // 2, ALTO // 2 + 25)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_rect.collidepoint(evento.pos):
                    inicializar_juego()
                    juego()  # Reiniciar el ciclo del juego
                    return

        pygame.display.flip()

# Pantalla de ganaste
def pantalla_ganaste():
    fuente_titulo = pygame.font.Font(None, 74)
    fuente_boton = pygame.font.Font(None, 50)

    while True:
        pantalla.fill(NEGRO)
        mostrar_texto("¡Ganaste!", fuente_titulo, BLANCO, ANCHO // 2, ALTO // 4)
        boton_rect = pygame.Rect(ANCHO // 2 - 100, ALTO // 2, 200, 50)
        pygame.draw.rect(pantalla, AZUL, boton_rect)
        mostrar_texto("Reiniciar", fuente_boton, BLANCO, ANCHO // 2, ALTO // 2 + 25)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_rect.collidepoint(evento.pos):
                    inicializar_juego()
                    juego()  # Reiniciar el ciclo del juego
                    return

        pygame.display.flip()

# Inicializar enemigos y bolitas basadas en el laberinto
def inicializar_juego():
    global bolitas, bolitas_especiales, enemigos, paredes, jugador, vidas, puntaje, modo_especial, tiempo_especial

    bolitas = []
    bolitas_especiales = []
    enemigos = []
    paredes = []
    vidas = 3
    puntaje = 0
    modo_especial = False
    tiempo_especial = 0

    for fila_idx, fila in enumerate(laberinto):
        for col_idx, celda in enumerate(fila):
            if celda == ".":
                bolita = pygame.Rect(
                    col_idx * ESCALA_CELDA + ESCALA_CELDA // 3,
                    fila_idx * ESCALA_CELDA + ESCALA_CELDA // 3,
                    TAMANO_BOLITA,
                    TAMANO_BOLITA,
                )
                bolitas.append(bolita)
            elif celda == "#":
                pared = pygame.Rect(
                    col_idx * ESCALA_CELDA,
                    fila_idx * ESCALA_CELDA,
                    ESCALA_CELDA,
                    ESCALA_CELDA
                )
                paredes.append(pared)

    # Agregar 4 enemigos en posiciones iniciales
    enemigos = [
        pygame.Rect(150, 200, TAMANO_ENEMIGO, TAMANO_ENEMIGO),
        pygame.Rect(230, 220, TAMANO_ENEMIGO, TAMANO_ENEMIGO),
        pygame.Rect(200, 300, TAMANO_ENEMIGO, TAMANO_ENEMIGO),
        pygame.Rect(260, 100, TAMANO_ENEMIGO, TAMANO_ENEMIGO)
    ]

    # Agregar 4 bolitas especiales en posiciones aleatorias
    while len(bolitas_especiales) < 4:
        fila_idx = random.randint(0, len(laberinto) - 1)
        col_idx = random.randint(0, len(laberinto[0]) - 1)
        if laberinto[fila_idx][col_idx] == ".":
            bolita_especial = pygame.Rect(
                col_idx * ESCALA_CELDA + ESCALA_CELDA // 3,
                fila_idx * ESCALA_CELDA + ESCALA_CELDA // 3,
                TAMANO_BOLITA,
                TAMANO_BOLITA,
            )
            bolitas_especiales.append(bolita_especial)
            laberinto[fila_idx] = laberinto[fila_idx][:col_idx] + " " + laberinto[fila_idx][col_idx + 1:]

# Validar movimiento dentro del laberinto
def movimiento_valido(rect, dx, dy):
    nueva_x = rect.x + dx
    nueva_y = rect.y + dy
    fila = (nueva_y + TAMANO_JUGADOR // 2) // ESCALA_CELDA
    columna = (nueva_x + TAMANO_JUGADOR // 2) // ESCALA_CELDA

    if laberinto[fila][columna] != "#":
        return True
    return False

# Bucle principal del juego
def juego():
    global bolitas, bolitas_especiales, enemigos, laberinto, paredes, vidas, puntaje, modo_especial, tiempo_especial

    direccion_jugador = (0, 0)
    vidas = 3
    puntaje = 0
    modo_especial = False
    tiempo_especial = 0

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    direccion_jugador = (0, -velocidad_jugador)
                elif evento.key == pygame.K_DOWN:
                    direccion_jugador = (0, velocidad_jugador)
                elif evento.key == pygame.K_LEFT:
                    direccion_jugador = (-velocidad_jugador, 0)
                elif evento.key == pygame.K_RIGHT:
                    direccion_jugador = (velocidad_jugador, 0)

        if movimiento_valido(jugador, *direccion_jugador):
            jugador.x += direccion_jugador[0]
            jugador.y += direccion_jugador[1]

        for bolita in bolitas[:]:
            if jugador.colliderect(bolita):
                bolitas.remove(bolita)
                puntaje += 10

        for bolita_especial in bolitas_especiales[:]:
            if jugador.colliderect(bolita_especial):
                bolitas_especiales.remove(bolita_especial)
                puntaje += 10
                modo_especial = True
                tiempo_especial = pygame.time.get_ticks()

        if modo_especial and pygame.time.get_ticks() - tiempo_especial > 5000:
            modo_especial = False

        for enemigo in enemigos[:]:
            dx = -velocidad_enemigos if jugador.x < enemigo.x else velocidad_enemigos
            dy = -velocidad_enemigos if jugador.y < enemigo.y else velocidad_enemigos

            if movimiento_valido(enemigo, dx, 0):
                enemigo.x += dx
            if movimiento_valido(enemigo, 0, dy):
                enemigo.y += dy

            if jugador.colliderect(enemigo):
                if modo_especial:
                    enemigos.remove(enemigo)
                else:
                    vidas -= 1
                    jugador.x, jugador.y = ESCALA_CELDA, ESCALA_CELDA
                    if vidas == 0:
                        pantalla_fin(f"Fin del juego. Puntaje: {puntaje}")
                        return

        if puntaje >= 1060:
            pantalla_ganaste()
            return

        pantalla.fill((0, 0, 0))

        for pared in paredes:
            pantalla.blit(img_wall, (pared.x, pared.y))

        pantalla.blit(img_player, (jugador.x, jugador.y))

        for bolita in bolitas:
            pantalla.blit(img_bolita, (bolita.x, bolita.y))

        for bolita_especial in bolitas_especiales:
            pygame.draw.ellipse(pantalla, AMARILLO, bolita_especial)

        for enemigo in enemigos:
            pantalla.blit(img_enemy, (enemigo.x, enemigo.y))

        mostrar_texto(f"Vidas: {vidas}  Puntaje: {puntaje}", pygame.font.Font(None, 36), BLANCO, ANCHO // 2, 20)

        pygame.display.flip()
        clock.tick(FPS)

# Iniciar juego
if __name__ == "__main__":
    iniciar_musica()  # Reproducir música al inicio
    pantalla_inicio()  # Pantalla de inicio
    inicializar_juego()  # Inicializar juego
    juego()  # Empezar juego
