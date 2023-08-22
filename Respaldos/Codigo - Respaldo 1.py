import pygame
import time
from boton import Boton
import random
import ast
import os
import heapq

# Inicializa Pygame
pygame.init()
pygame.display.set_caption('La jungla congelada')

# Tamaño de la pantalla
pantallaLargo = 1100
pantallaAncho = 600
pantalla = pygame.display.set_mode((pantallaLargo, pantallaAncho))

# Colores
blanco = (255, 255, 255)
negro = (0, 0, 0)
celeste = (98, 180, 255)
amarillo = (255, 255, 0)

# Fuentes
fuente = pygame.font.Font("Fuentes/NexaHeavy.ttf", 20)
fuente2 = pygame.font.Font("Fuentes/NexaHeavy.ttf", 40)

# Botones de interfaz
botonEntrar = Boton(400, 400, 125, 50, (38, 42, 86))
botonSalir = Boton(600, 400, 125, 50, (38, 42, 86))
botonRegresar = Boton(800, 500, 125, 50, (38, 42, 86))
botonCargar = Boton(500, 250, 125, 50, (38, 42, 86))
botonGenerar = Boton(500, 325, 125, 50, (38, 42, 86))
botonAventura = Boton(500, 400, 125, 50, (38, 42, 86))
botonCompetitivo = Boton(500, 475, 125, 50, (38, 42, 86))
botonOk = Boton(485,450,120,50, (38, 42, 86))
botonJugar = Boton(385,450,120,50, (38, 42, 86))
botonResolver = Boton(585,450,120,50, (38, 42, 86))

# Cargar las imágenes
pacman = pygame.image.load("Imagenes/pacman.png")
monstruoJungla = pygame.image.load("Imagenes/fantasma.png")
monstruoHielo = pygame.image.load("Imagenes/fantasma2.png")

# Escalar las imágenes
scaled_image = pygame.transform.scale(monstruoHielo, (100, 100))
scaled_fantasma_image = pygame.transform.scale(monstruoJungla, (100, 100))
scaled_fantasma2_image = pygame.transform.scale(pacman, (100, 100))

# Título y sombra
texto = fuente.render("La jungla congelada", True, blanco)
textoSombra = fuente.render("La jungla congelada", True, negro)

# Coordenadas y velocidad inicial
animacion_inicio_x = 0
animacion_inicio_y = 0
velocidad = 5

# Dirección inicial (1 = derecha, 0 = abajo, -1 = izquierda, 2 = arriba)
direction = 1

#Tamano de las celdas
tamanoCelda = 20

#Reloj de pygame
reloj = pygame.time.Clock()

#Funcion para dibujar el laberinto
def renderMaze(laberinto):
    x = 0
    y = 0
    for i in range(len(laberinto)):
        for j in range(len(laberinto[0])):
            if laberinto[i][j] == 0:
                pygame.draw.rect(pantalla, (255, 205, 178), (x, y, tamanoCelda, tamanoCelda))
            elif laberinto[i][j] == 1:
                pygame.draw.rect(pantalla, (229, 152, 155) ,(x, y, tamanoCelda, tamanoCelda))
            elif laberinto[i][j] == 'F':
                pygame.draw.rect(pantalla, (255, 183, 0), (x, y, tamanoCelda, tamanoCelda))
            elif laberinto[i][j] == 'I':
                pygame.draw.rect(pantalla, (120, 150, 100), (x, y, tamanoCelda, tamanoCelda))
            x += tamanoCelda
        y += tamanoCelda
        x = 0

# Define la función para dibujar a Pacman
def dibujar_pacman():
    rect = pygame.Rect(pacman_x * tamanoCelda, pacman_y * tamanoCelda, tamanoCelda, tamanoCelda)
    pygame.draw.circle(pantalla, amarillo, rect.center, tamanoCelda // 2 - 2)

#Funcion para jugar el laberinto con las flechas
def partidaSimple(laberinto):
    global pacman_x,pacman_y, fin, inicioPos,pantalla
    ancho, alto = len(laberinto[0])*tamanoCelda,len(laberinto)*tamanoCelda
    pantalla = pygame.display.set_mode((ancho, alto))
    # Encuentra la posición inicial y final en el laberinto
    inicioPos = None
    fin = None
    for y, fila in enumerate(laberinto):
        for x, celda in enumerate(fila):
            if celda == 'I':
                inicioPos = (x, y)
                laberinto[y][x] = 0
            elif celda == 'F':
                fin = (x, y)
                laberinto[y][x] = 0

    # Define la posición inicial de Pacman
    pacman_x, pacman_y = inicioPos
    laberinto[fin[1]][fin[0]] = 'F'
    siguenteMov = pygame.time.get_ticks() + 1000
    while True:
            movActual = pygame.time.get_ticks()
            renderMaze(laberinto)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and pacman_x > 0 and (not laberinto[pacman_y][pacman_x-1] or laberinto[pacman_y][pacman_x-1] == 'F'):
                if (movActual > siguenteMov): 
                    pacman_x -= 1
                    siguenteMov = movActual + 80
            elif keys[pygame.K_RIGHT] and pacman_x < len(laberinto[0])-1 and (not laberinto[pacman_y][pacman_x+1] or laberinto[pacman_y][pacman_x+1] == 'F'):
                if (movActual > siguenteMov):
                    pacman_x += 1
                    siguenteMov = movActual + 80
            elif keys[pygame.K_UP] and pacman_y > 0 and (not laberinto[pacman_y-1][pacman_x] or laberinto[pacman_y-1][pacman_x] == 'F'):
                if (movActual > siguenteMov):
                    pacman_y -= 1
                    siguenteMov = movActual + 80 
            elif keys[pygame.K_DOWN] and pacman_y < len(laberinto)-1 and (not laberinto[pacman_y+1][pacman_x] or laberinto[pacman_y+1][pacman_x] == 'F'):
                if (movActual > siguenteMov):
                    pacman_y += 1
                    siguenteMov = movActual + 80  
            if (pacman_x,pacman_y) == (fin[0],fin[1]):
                print('ganado')
            
            dibujar_pacman()
            pygame.display.flip()
            reloj.tick(30)

#Funciones del algoritmo para resolver (A*)
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(laberinto, inicio, fin):
    vecinos = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    open_list = []
    heapq.heappush(open_list, (0, inicio))
    g_costs = {inicio: 0}
    came_from = {inicio: None}

    while open_list:
        _, actual = heapq.heappop(open_list)

        if actual == fin:
            path = []
            while actual is not None:
                path.append(actual)
                actual = came_from[actual]
            path.reverse()
            return path

        for dx, dy in vecinos:
            vecino = actual[0] + dx, actual[1] + dy
            if 0 <= vecino[0] < len(laberinto[0]) and 0 <= vecino[1] < len(laberinto) and laberinto[vecino[1]][vecino[0]] == 0:
                tentative_g_cost = g_costs[actual] + 1
                if vecino not in g_costs or tentative_g_cost < g_costs[vecino]:
                    g_costs[vecino] = tentative_g_cost
                    f_cost = tentative_g_cost + heuristic(fin, vecino)
                    heapq.heappush(open_list, (f_cost, vecino))
                    came_from[vecino] = actual

    return []

#mueve a pacman
def mover_pacman(laberinto):
    global pacman_x, pacman_y

    path = a_star(laberinto, (pacman_x, pacman_y), fin)

    if len(path) > 1:
        pacman_x, pacman_y = path[1]
        laberinto[path[1][1]][path[1][0]] = 'I'
        return False  # Pacman no ha llegado al destino
    else:
        return True  # Pacman ha llegado al destino

def resolver(laberinto):
    global pacman_x,pacman_y, fin, inicioPos,pantalla
    #actualiza el tamano de la pantalla
    ancho, alto = len(laberinto[0])*tamanoCelda,len(laberinto)*tamanoCelda
    pantalla = pygame.display.set_mode((ancho, alto))
    # Encuentra la posición inicial y final en el laberinto
    inicioPos = None
    fin = None
    for y, fila in enumerate(laberinto):
        for x, celda in enumerate(fila):
            if celda == 'I':
                inicioPos = (x, y)
                laberinto[y][x] = 0
            elif celda == 'F':
                fin = (x, y)
                laberinto[y][x] = 0

    # Define la posición inicial de Pacman
    pacman_x, pacman_y = inicioPos
    sol = a_star(laberinto, (pacman_x, pacman_y), fin)
    while True:
        encontrado = False

        # Verifica si el usuario ha cerrado la ventana
        while not encontrado:
            # Verifica si el usuario ha cerrado la ventana
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            # Dibuja el laberinto y a Pacman
            renderMaze(laberinto)
            dibujar_pacman()

            # Mueve a Pacman y verifica si ha llegado al destino
            encontrado = mover_pacman(laberinto)

            # Actualiza la pantalla
            pygame.display.update()

            # Espera antes de actualizar la pantalla de nuevo
            reloj.tick(20)  # Velocidad en la que se mueve
        if (pacman_x,pacman_y) == inicioPos:
            print('no sol')
        print('ganado' + str(len(sol) - 1))

#Menu de seleccion de modo para jugar
def selecMododeSol(laberinto):
    corriendo = True
    textoSol = fuente2.render('Seleccione el metodo de solucion:',True,blanco)
    textoSolrect = textoSol.get_rect(center=(pantallaLargo/2,(pantallaAncho/2) - 125))
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
        pantalla.fill(celeste)
        pantalla.blit(textoSol,textoSolrect)
        if botonJugar.imprimirBotonInteractivo(negro):
            partidaSimple(laberinto)
        botonJugar.textoEnBoton(fuente,'Jugar',blanco)
        if botonResolver.imprimirBotonInteractivo(negro):
            resolver(laberinto)
        botonResolver.textoEnBoton(fuente,'Resolver',blanco) 
        pygame.display.update()


#valida que el laberinto subido sea valido
def validarLaberinto(matriz):
    if type(matriz) == list and len(matriz)>1:
        inicioEncontrado = False
        FinalEncontrado = False
        filaRef = matriz[0]
        for i in matriz:
            if type(i) != list or len(i)<=1 or len(i) != len(filaRef):
                    return False
            for j in i:
                if j != 1 and j != 0 and j != 'I' and j != 'F':
                     return False
                if j == 'F' and FinalEncontrado == False:
                     FinalEncontrado = True
                elif j == 'F' and FinalEncontrado:
                     return False
                if j == 'I' and inicioEncontrado == False:
                     inicioEncontrado = True
                elif j == 'I' and inicioEncontrado:
                     return False
        return True
    else:
         return False

#Funcion para que el usuario cargue el laberinto
def cargarLaberinto():
    corriendo = True
    textoBox = pygame.Rect(350,400,400,40)
    entrada = ''
    activo = False
    textoIngreso = fuente2.render('Ingrese el nombre de su laberinto',True,blanco)
    textoIngresorect = textoIngreso.get_rect(center=(pantallaLargo/2,(pantallaAncho/2) - 125))
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                #si se clickea sobre el cuadro
                if textoBox.collidepoint(evento.pos):
                    activo = True
                else:
                    activo = False
            if evento.type == pygame.KEYDOWN:
                #si se presiona backspace se borra
                if activo:
                    if evento.key == pygame.K_BACKSPACE:
                        entrada = entrada[:-1]
                #sino solo se anade el texto
                    else:
                        entrada += evento.unicode 
        #colorea el fondo 
        pantalla.fill(celeste)
        pantalla.blit(textoIngreso,textoIngresorect) 
        pygame.draw.rect(pantalla,(38, 42, 86),textoBox)
        textoEntrada = fuente.render(entrada,True,blanco)
        pantalla.blit(textoEntrada,(textoBox.x + 5, textoBox.y + 5))
        textoBox.w = max(400, textoEntrada.get_width()+10)
        if botonOk.imprimirBotonInteractivo(negro):
            for file in os.scandir("Laberintos"):
               if os.path.splitext(file.name)[1] == ".txt" and os.path.splitext(file.name)[0] == entrada:
                   laberintostr = open(file.path, "r").read()
                   try:
                       laberinto = ast.literal_eval(laberintostr)
                       if type(laberinto) == list and validarLaberinto(laberinto):
                           return laberinto
                   except:
                       continue
        botonOk.textoEnBoton(fuente,'Ok',blanco)
        if botonRegresar.imprimirBotonInteractivo(negro):
            menuSeleccion()
        botonRegresar.textoEnBoton(fuente,'Regresar',blanco)
        pygame.display.update()

#Funcion para crear laberinto
def crear_laberinto(ancho, alto):
    # Inicializar laberinto con todas las celdas como paredes
    laberinto = [[1 for _ in range(ancho)] for _ in range(alto)]

    # Función auxiliar para verificar si una celda es válida y sin visitar
    def es_valido(x, y, visitado):
        return 0 <= x < alto and 0 <= y < ancho and not visitado[x][y] and laberinto[x][y] == 1

    #Función del algoritmo Depth-First Search (algoritmoDFS) para crear el laberinto
    def algoritmoDFS(x, y, visitado): 
        visitado[x][y] = True
        laberinto[x][y] = 0

        direcciones = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(direcciones)

        for dx, dy in direcciones:
            nx, ny = x + 2 * dx, y + 2 * dy

            if es_valido(nx, ny, visitado):
                laberinto[x + dx][y + dy] = 0
                algoritmoDFS(nx, ny, visitado)

    # Iniciar la búsqueda en profundidad desde una celda aleatoria
    visitado = [[False for _ in range(ancho)] for _ in range(alto)]
    x_inicial, y_inicial = random.randint(0, alto // 2) * 2, random.randint(0, ancho // 2) * 2
    algoritmoDFS(x_inicial, y_inicial, visitado)

    # Agregar entrada y salida al laberinto
    laberinto[0][0] = 'I'
    laberinto[-2][-2] = 'F'

    return laberinto

#Funcion para que el usuario genere el laberinto
def dimensionesGenerar():
    corriendo = True
    textoBox1 = pygame.Rect(350,400,100,40)
    textoBox2 = pygame.Rect(650,400,100,40)
    entrada1 = ''
    entrada2 = ''
    activo1 = False
    activo2 = False
    textoIngreso = fuente2.render('Ingrese las dimensiones de su laberinto:',True,blanco)
    textoIngresorect = textoIngreso.get_rect(center=(pantallaLargo/2,(pantallaAncho/2) - 125))
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                #si se clickea sobre el cuadro
                if textoBox1.collidepoint(evento.pos):
                    activo1 = True
                else:
                    activo1 = False
                if textoBox2.collidepoint(evento.pos):
                    activo2 = True
                else:
                    activo2 = False
            if evento.type == pygame.KEYDOWN:
                #si se presiona backspace se borra
                if activo1:
                    if evento.key == pygame.K_BACKSPACE:
                        entrada1 = entrada1[:-1]
                #sino solo se anade el texto
                    else:
                        entrada1 += evento.unicode 
                if activo2:
                    if evento.key == pygame.K_BACKSPACE:
                        entrada2 = entrada2[:-1]
                #sino solo se anade el texto
                    else:
                        entrada2 += evento.unicode
        #colorea el fondo 
        pantalla.fill(celeste)
        pantalla.blit(textoIngreso,textoIngresorect) 
        pygame.draw.rect(pantalla,(38, 42, 86),textoBox1)
        pygame.draw.rect(pantalla,(38, 42, 86),textoBox2)
        textoEntrada1 = fuente.render(entrada1,True,blanco)
        textoEntrada2 = fuente.render(entrada2,True,blanco)
        pantalla.blit(textoEntrada1,(textoBox1.x + 5, textoBox1.y + 5))
        pantalla.blit(textoEntrada2,(textoBox2.x + 5, textoBox2.y + 5))
        if botonOk.imprimirBotonInteractivo(negro):
            try:
                ancho = int(entrada1) 
                alto = int(entrada2)
                if 2<=ancho<=100 and 2<=alto<=100:
                    return crear_laberinto(ancho,alto)
            except:
                continue
            
        botonOk.textoEnBoton(fuente,'Ok',blanco)
        if botonRegresar.imprimirBotonInteractivo(negro):
            menuSeleccion()
        botonRegresar.textoEnBoton(fuente,'Regresar',blanco)
        pygame.display.update()
#Menu de seleccion 
def menuSeleccion():
    pantallaLargo = 1100
    pantallaAncho = 600
    pantalla = pygame.display.set_mode((pantallaLargo, pantallaAncho))
    corriendo = True
    textoMenu = fuente2.render('Seleccione modo de juego:', True, blanco)
    textoMunurect = textoMenu.get_rect(center=(pantallaLargo/2,(pantallaAncho/2) - 125))
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
        pantalla.fill(celeste)
        if botonCargar.imprimirBotonInteractivo(negro):
            laberintoSelec = cargarLaberinto()
            selecMododeSol(laberintoSelec)
        botonCargar.textoEnBoton(fuente,'Cargar',blanco)
        if botonGenerar.imprimirBotonInteractivo(negro):
            laberintoSelec = dimensionesGenerar()
            selecMododeSol(laberintoSelec)
        botonGenerar.textoEnBoton(fuente,'Generar',blanco)
        if botonAventura.imprimirBotonInteractivo(negro):
            pass
        botonAventura.textoEnBoton(fuente,'Aventura',blanco)
        if botonCompetitivo.imprimirBotonInteractivo(negro):
            pass
        botonCompetitivo.textoEnBoton(fuente,'Competitivo',blanco)
        if botonRegresar.imprimirBotonInteractivo(negro):
            inicio()
        botonRegresar.textoEnBoton(fuente,'Regresar',blanco)
        pantalla.blit(textoMenu,textoMunurect)
        pygame.display.update()

# Función para dibujar los botones
def dibujar_botones_inicio():
    if botonSalir.imprimirBotonInteractivo(negro):
        pygame.quit()
    botonSalir.textoEnBoton(fuente, 'Salir', blanco)

    if botonEntrar.imprimirBotonInteractivo(negro):
        pygame.mixer.music.stop()
        menuSeleccion()
    botonEntrar.textoEnBoton(fuente, 'Entrar', blanco)

# Función para actualizar la posición de las imágenes
def actualizar_posicion_imagenes():
    global animacion_inicio_x, animacion_inicio_y, direction

    if direction == 1:
        animacion_inicio_x += velocidad
        if animacion_inicio_x + scaled_image.get_width() >= pantallaLargo:
            direction = 0
    elif direction == 0:
        animacion_inicio_y += velocidad
        if animacion_inicio_y + scaled_image.get_height() >= pantallaAncho:
            direction = -1
    elif direction == -1:
        animacion_inicio_x -= velocidad
        if animacion_inicio_x <= 0:
            direction = 2
    elif direction == 2:
        animacion_inicio_y -= velocidad
        if animacion_inicio_y <= 0:
            direction = 1

    # Limitar la posición de las imágenes dentro de los límites de la pantalla
    animacion_inicio_x = max(0, animacion_inicio_x)
    animacion_inicio_x = min(pantallaLargo - scaled_image.get_width(), animacion_inicio_x)
    animacion_inicio_y = max(0, animacion_inicio_y)
    animacion_inicio_y = min(pantallaAncho - scaled_image.get_height(), animacion_inicio_y)

    fantasma_x = animacion_inicio_x
    fantasma_y = animacion_inicio_y
    fantasma2_x = animacion_inicio_x
    fantasma2_y = animacion_inicio_y

    if direction == 1:
        fantasma_x -= scaled_fantasma_image.get_width()
        fantasma2_x += scaled_image.get_width()
    elif direction == -1:
        fantasma_x += scaled_image.get_width()
        fantasma2_x -= scaled_fantasma2_image.get_width()
    elif direction == 0:
        fantasma_y -= scaled_fantasma_image.get_height()
        fantasma2_y += scaled_image.get_height()
    elif direction == 2:
        fantasma_y += scaled_image.get_height()
        fantasma2_y -= scaled_fantasma2_image.get_height()

    fantasma_x = max(0, fantasma_x)
    fantasma_x = min(pantallaLargo - scaled_fantasma_image.get_width(), fantasma_x)
    fantasma_y = max(0, fantasma_y)
    fantasma_y = min(pantallaAncho - scaled_fantasma_image.get_height(), fantasma_y)

    fantasma2_x = max(0, fantasma2_x)
    fantasma2_x = min(pantallaLargo - scaled_fantasma2_image.get_width(), fantasma2_x)
    fantasma2_y = max(0, fantasma2_y)
    fantasma2_y = min(pantallaAncho - scaled_fantasma2_image.get_height(), fantasma2_y)

    pantalla.blit(scaled_image, (animacion_inicio_x, animacion_inicio_y))
    pantalla.blit(scaled_fantasma_image, (fantasma_x, fantasma_y))
    pantalla.blit(scaled_fantasma2_image, (fantasma2_x, fantasma2_y))

def inicio():
    
    # Reproducir música de inicio
    pygame.mixer.music.load('Canciones/inicio.mp3')
    pygame.mixer.music.play(-1)

    pantallaLargo = 1100
    pantallaAncho = 600
    pantalla = pygame.display.set_mode((pantallaLargo, pantallaAncho))
    corriendo = True
    textoAumenta = True
    textoEscalaAumento = 0
    clock = pygame.time.Clock()

    while corriendo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False

        # Aumentar y disminuir el tamaño del texto
        if textoAumenta:
            textoEscalaAumento += 0.1
            if textoEscalaAumento >= 1.1:
                textoAumenta = False
        else:
            textoEscalaAumento -= 0.001
            if textoEscalaAumento <= 1.9:
                textoAumenta = True

        textoEscala = pygame.transform.rotozoom(texto, 0, textoEscalaAumento)
        textoEscalaRect = textoEscala.get_rect()
        textoEscalaRect.center = (pantalla.get_width() // 2, pantalla.get_height() // 2)

        textoEscalaSombra = pygame.transform.rotozoom(textoSombra, 0, textoEscalaAumento)
        textoEscalaRectSombra = textoEscalaSombra.get_rect()
        textoEscalaRectSombra.center = ((pantalla.get_width() // 2) + 4, (pantalla.get_height() // 2) + 4)

        pantalla.fill(celeste)

        pantalla.blit(textoEscalaSombra, textoEscalaRectSombra)
        pantalla.blit(textoEscala, textoEscalaRect)

        dibujar_botones_inicio()

        actualizar_posicion_imagenes()

        pygame.display.update()
        clock.tick(60)
        
    pygame.quit()

inicio()




