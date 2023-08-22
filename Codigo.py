import pygame
import time
from boton import Boton
import random
import ast
import os
import heapq
import json 
from monstruo import monstruo 

# Inicializa Pygame
pygame.init()
pygame.display.set_caption('La jungla congelada')

# Tamaño de la pantalla
pantallaLargo = 1100
pantallaAncho = 600
pantalla = pygame.display.set_mode((pantallaLargo, pantallaAncho))

#Colores
blanco = (255, 255, 255)
negro = (0, 0, 0)
celeste = (98, 180, 255)
amarillo = (255, 255, 0)
rojo = (255, 0, 0)
violeta = (38, 42, 86)
verde = (34, 139, 34)
cafe = (139, 69, 19)
azul = (30, 144, 255)
#Colores de laberinto 
tropicalPared = (31, 76, 77)
tropicalCamino = (119, 171, 161)
congeladoPared = (69, 120, 190)
congeladoCamino = (144, 211, 238)

# Fuentes
fuente = pygame.font.Font("Fuentes/NexaHeavy.ttf", 20)
fuente2 = pygame.font.Font("Fuentes/NexaHeavy.ttf", 40)

#Imagen de fondo del juego
fondoCongelado = pygame.image.load("Imagenes/congelado.png")
fondoTropical = pygame.image.load("Imagenes/tropical.png")
fondoImagen = fondoCongelado
#Colores de los jugadores incial
pacmanColor = (71,61,111)
Jug2Color = (118,132,220)
congelaColor = (30,144,255)
mataColor = (114, 47, 55)
#Color de botones y el laberinto del juego
colorBotones = azul
colorPared = congeladoPared
colorCamino = congeladoCamino

#Imagenes de los ambientes
imagenTropical = fondoTropical
imagenCongelado = fondoCongelado
anchoImagenAmbiente = 198
largoImagenAmbiente = 140

# Botón de interfaz "Salir"
botonImagenTropical = Boton(225, 210, anchoImagenAmbiente, largoImagenAmbiente, azul)
botonImagenCongelado = Boton(525, 210, anchoImagenAmbiente, largoImagenAmbiente, azul)

# Botones de interfaz
botonEntrar = Boton(370, 350, 100, 50, colorBotones)
botonConfiguracion = Boton(477, 350, 150, 50, colorBotones)
botonSalir = Boton(635, 350, 100, 50, colorBotones)
botonRegresar = Boton(800, 500, 125, 50, colorBotones)
botonRegresarConfiguracion = Boton((pantallaLargo / 2 - (pantallaLargo/1.2) / 2 + 770),(pantallaAncho / 2 - (pantallaAncho/1.2) / 2 + 435), 125, 50, colorBotones)
botonCargar = Boton(500, 250, 125, 50, colorBotones)
botonGenerar = Boton(500, 325, 125, 50, colorBotones)
botonAventura = Boton(500, 400, 125, 50, colorBotones)
botonCompetitivo = Boton(500, 475, 125, 50, colorBotones)
botonOk = Boton(485,450,120,50, colorBotones)
botonJugar = Boton(385,450,120,50, colorBotones)
botonResolver = Boton(585,450,120,50, colorBotones)
botonRegresarNiveles = Boton(pantalla.get_width()-160, pantalla.get_height()/2, 125, 50, colorBotones)

#cambia colores de los botones
def cambiarColorBotones(nuevoColor):
    global colorBotones
    colorBotones = nuevoColor
    botonEntrar.color = nuevoColor
    botonConfiguracion.color = nuevoColor
    botonSalir.color = nuevoColor
    botonRegresar.color = nuevoColor
    botonRegresarConfiguracion.color = nuevoColor
    botonRegresarNiveles.color = nuevoColor
    botonCargar.color = nuevoColor
    botonGenerar.color = nuevoColor
    botonAventura.color = nuevoColor
    botonCompetitivo.color = nuevoColor
    botonOk.color = nuevoColor
    botonJugar.color = nuevoColor
    botonResolver.color = nuevoColor

# Cargar las imágenes
pacman = pygame.image.load("Imagenes/pacman.png")
monstruoJungla = pygame.image.load("Imagenes/monstruo.png")
monstruoHielo = pygame.image.load("Imagenes/monstruo2.png")

# Escalar las imágenes
scaled_image = pygame.transform.scale(monstruoHielo, (100, 100))
scaled_monstruo_image = pygame.transform.scale(monstruoJungla, (100, 100))
scaled_monstruo2_image = pygame.transform.scale(pacman, (100, 100))
configuracionImg = pygame.transform.scale(pygame.image.load("Imagenes/configuracion.png").convert_alpha(),(30,30))

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

#Incializacion de records
records = {
    'nivelMax':0,
    'puntosMax':0
}

try:
    records = json.load(open('records.txt'))
except:
    json.dump(records,open('records.txt','w'))

#Funcion de configuracion de ambientes
def configuracion():
    global fondoImagen, colorPared, colorCamino, pacmanColor,Jug2Color,mataColor,congelaColor
    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

        fondoPantalla = pygame.transform.scale(fondoImagen, (pantallaLargo, pantallaAncho))
        pantalla.blit(fondoPantalla, (0, 0))

        #Textos
        textoinstrucciones = fuente.render("Selección de ambiente:", True, negro)
        textoIntro = fuente.render("Le damos la bienvenida a la configuración de la jungla congelada", True, negro)
        textoEscojaAmbiente = fuente.render("Haga click en la imagen del ambiente que desea para el juego:", True, negro)
        textoAmbienteTropical = fuente.render("Ambiente tropical", True, negro)
        textoAmbienteCongelado = fuente.render("Ambiente congelado", True, negro)
        textoCerrar = fuente.render("Si desea cerrar el programa, presione regresar y luego salir.", True, negro) 

        rectanguloX = pantallaLargo / 2 - (pantallaLargo/1.2) / 2
        rectanguloY = pantallaAncho / 2 - (pantallaAncho/1.2) / 2
        pygame.draw.rect(pantalla, (209, 190, 157), (rectanguloX, rectanguloY, (pantallaLargo/1.2), (pantallaAncho/1.2)))
        pygame.draw.rect(pantalla, (100, 81, 59), (rectanguloX, rectanguloY, (pantallaLargo/1.2), (pantallaAncho/1.2)), 2)

        #Símbolo de pregunta en pantalla principal
        pantalla.blit(textoinstrucciones, ((pantalla.get_width() // 9)+3, (pantalla.get_height() // 10)+4))
        pantalla.blit(textoIntro, ((pantalla.get_width() // 9)+4, (pantalla.get_height() // 10)+50))
        pantalla.blit(textoEscojaAmbiente, ((pantalla.get_width() // 9)+4, (pantalla.get_height() // 10)+100))
        pantalla.blit(textoAmbienteTropical, ((pantalla.get_width() // 9)+110, (pantalla.get_height() // 10)+300))
        pantalla.blit(textoAmbienteCongelado, ((pantalla.get_width() // 9)+400, (pantalla.get_height() // 10)+300))
        pantalla.blit(textoCerrar, ((pantalla.get_width() // 9)+4, (pantalla.get_height() // 10)+345))

        if botonRegresarConfiguracion.imprimirBotonInteractivo(negro):
            inicio()
        botonRegresarConfiguracion.textoEnBoton(fuente,'Regresar',blanco)
        #cambiar ambientes
        if botonImagenCongelado.imprimirBotonInteractivo(negro):
            cambiarColorBotones(azul)
            fondoImagen = fondoCongelado
            colorPared = congeladoPared
            colorCamino = congeladoCamino
            pacmanColor = (71,61,111)
            Jug2Color = (118,132,220)
            congelaColor = (30,144,255)
            mataColor = (114, 47, 55)
        botonImagenCongelado.textoEnBoton(fuente, 'Congelado', blanco)

        if botonImagenTropical.imprimirBotonInteractivo(negro):
            cambiarColorBotones(verde)
            fondoImagen = fondoTropical
            colorPared = tropicalPared
            colorCamino = tropicalCamino
            pacmanColor = (154,72,122)
            Jug2Color = (110,114,72)
            congelaColor = (0,76,125)
            mataColor = (255,87,51)
        botonImagenTropical.textoEnBoton(fuente, 'Tropical', blanco)

        #Imagen del botón para cambiar el ambiente a Congelado
        imagenCongeladoEscalada = pygame.transform.scale(imagenCongelado, (botonImagenCongelado.ancho, botonImagenCongelado.largo))
        posicionImagenCongelado = imagenCongeladoEscalada.get_rect(center=botonImagenCongelado.rect.center)
        pantalla.blit(imagenCongeladoEscalada, posicionImagenCongelado)

        #Imagen del botón para cambiar el ambiente a Tropical
        imagenTropicalEscalada = pygame.transform.scale(imagenTropical, (botonImagenTropical.ancho, botonImagenTropical.largo))
        posicionImagenTropical = imagenTropicalEscalada.get_rect(center=botonImagenTropical.rect.center)
        pantalla.blit(imagenTropicalEscalada, posicionImagenTropical)

        pygame.display.update()

    pygame.quit()

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
    laberinto[-2][-1] = 'F'

    return laberinto

#Pantalla de terminado de los niveles (cuando se pierde o se gana)
def terminado(nivelActual,puntajeActual):
    global fondoImagen
    pantallaLargo = 1100
    pantallaAncho = 600
    pantalla = pygame.display.set_mode((pantallaLargo, pantallaAncho))
    botonDevolver = Boton(pantalla.get_width()//2  - 50,500,125,50,colorBotones)
    corriendo = True
    #guarda en el archivo json
    if nivelActual > records['nivelMax']:
        records['nivelMax'] = nivelActual
        json.dump(records,open('records.txt','w'))
    if puntajeActual > records['puntosMax']:
        records['puntosMax'] = puntajeActual
        json.dump(records,open('records.txt','w'))
    textoFinal = fuente2.render('¡Partida terminada!',True,blanco)
    textoFinalrect = textoFinal.get_rect(center=(pantallaLargo/2,(pantallaAncho/2) - 125))
    #textos de records
    textoPuntajeActual = fuente.render('Puntaje obtenido: ' + str(puntajeActual),True,blanco)
    textoPuntajeMaximo = fuente.render('Puntaje máximo: ' + str(records['puntosMax']),True,blanco)
    textoNivelActual = fuente.render('Nivel alcanzado: ' + str(nivelActual),True,blanco)
    textoNivelMaximo = fuente.render('Nivel máximo: ' + str(records['nivelMax']),True,blanco)
    fondoPantalla = pygame.transform.scale(fondoImagen, (pantallaLargo, pantallaAncho))

    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
        pantalla.blit(fondoPantalla, (0, 0))
        pantalla.blit(textoFinal,textoFinalrect)
        pantalla.blit(textoPuntajeActual,(300,300))
        pantalla.blit(textoPuntajeMaximo,(300,375))
        pantalla.blit(textoNivelActual,(650,300))
        pantalla.blit(textoNivelMaximo,(650,375))
        if botonDevolver.imprimirBotonInteractivo(negro):
            menuSeleccion()
        botonDevolver.textoEnBoton(fuente,'Regresar',blanco)
        pygame.display.update()

#Funcion para dibujar el laberinto
def renderMaze(laberinto):
    global colorPared, colorCamino
    x = 0
    y = 0
    for i in range(len(laberinto)):
        for j in range(len(laberinto[0])): #Aquí también se define el color del laberinto, tanto del camino, como de las paredes
            if laberinto[i][j] == 0:
                pygame.draw.rect(pantalla, colorCamino, (x, y, tamanoCelda, tamanoCelda))
            elif laberinto[i][j] == 1:
                pygame.draw.rect(pantalla, colorPared,(x, y, tamanoCelda, tamanoCelda))
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
    pygame.draw.circle(pantalla, pacmanColor, rect.center, tamanoCelda // 2 - 2)

#Defina la funcion para dibujar a jugador 2
def dibujar_jugador2():
    rect = pygame.Rect(j2x * tamanoCelda, j2y * tamanoCelda, tamanoCelda, tamanoCelda)
    pygame.draw.circle(pantalla, Jug2Color, rect.center, tamanoCelda // 2 - 2)

#Funcion de nivel 1 para dos jugadores
def nivel1(laberinto,jug2):
    global pacman_x,pacman_y,j2x,j2y, fin, inicioPos, fondoImagen, botonRegresarNiveles
    pygame.mixer.music.play(-1)
    ancho, alto = (len(laberinto[0])*tamanoCelda) + 200,len(laberinto)*tamanoCelda
    pantalla = pygame.display.set_mode((ancho, alto))
    contadorSeg = 300
    segundos = contadorSeg % 60
    minutos = contadorSeg // 60
    textoNivel = fuente2.render('Nivel 1',True,(255,255,255))
    texto = fuente2.render(str(minutos) + ':' + "{:02d}".format(segundos),True,(255,255,255))
    textoPuntaje = fuente2.render(str(0),True,(255,255,255))
    botonRegresarNiveles = Boton(pantalla.get_width()-160, pantalla.get_height()/2, 125, 50, colorBotones)
    eventoTiempo = pygame.USEREVENT + 1
    pygame.time.set_timer(eventoTiempo,1000)
    fondoPantalla = pygame.transform.scale(fondoImagen, (ancho, alto))
    # Encuentra la posición inicial y final en el laberinto
    inicioPos = None
    fin = None
    for y, fila in enumerate(laberinto):
        for x, celda in enumerate(fila):
            if celda == 'I':
                laberinto[y][x] = 0
                inicioPos = (random.randint(0,(len(laberinto[0])-1)//2), random.randint(0,(len(laberinto)-1)//2))
            elif celda == 'F':
                fin = (x, y)
    # Define la posición inicial de Pacman y del jugador 2
    pacman_x, pacman_y = inicioPos
    j2x,j2y = inicioPos
    laberinto[inicioPos[1]][inicioPos[0]] = 'I'
    siguenteMov1 = pygame.time.get_ticks() + 1000
    siguenteMov2 = pygame.time.get_ticks() + 1000
    while True:
            pantalla.blit(fondoPantalla, (0, 0))
            movActual1 = pygame.time.get_ticks()
            movActual2 = pygame.time.get_ticks()
            renderMaze(laberinto)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == eventoTiempo:
                    contadorSeg -= 1
                    segundos = contadorSeg % 60
                    minutos = (contadorSeg//60) % 60
                    texto = fuente2.render(str(minutos) + ':' + "{:02d}".format(segundos),True,(255,255,255))    
                    if contadorSeg == 0:
                        terminado(0,0)
            #movimientos del jugador
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and pacman_x > 0 and (not laberinto[pacman_y][pacman_x-1] or laberinto[pacman_y][pacman_x-1] == 'F' or laberinto[pacman_y][pacman_x-1] == 'I'):
                if (movActual1 > siguenteMov1): 
                    pacman_x -= 1
                    siguenteMov1 = movActual1 + 80
            elif keys[pygame.K_RIGHT] and pacman_x < len(laberinto[0])-1 and (not laberinto[pacman_y][pacman_x+1] or laberinto[pacman_y][pacman_x+1] == 'F' or laberinto[pacman_y][pacman_x+1] == 'I'):
                if (movActual1 > siguenteMov1):
                    pacman_x += 1
                    siguenteMov1 = movActual1 + 80
            elif keys[pygame.K_UP] and pacman_y > 0 and (not laberinto[pacman_y-1][pacman_x] or laberinto[pacman_y-1][pacman_x] == 'F' or laberinto[pacman_y-1][pacman_x] == 'I'):
                if (movActual1 > siguenteMov1):
                    pacman_y -= 1
                    siguenteMov1 = movActual1 + 80 
            elif keys[pygame.K_DOWN] and pacman_y < len(laberinto)-1 and (not laberinto[pacman_y+1][pacman_x] or laberinto[pacman_y+1][pacman_x] == 'F' or laberinto[pacman_y+1][pacman_x] == 'I'):
                if (movActual1 > siguenteMov1):
                    pacman_y += 1
                    siguenteMov1 = movActual1 + 80
            if keys[pygame.K_a] and j2x > 0 and (not laberinto[j2y][j2x-1] or laberinto[j2y][j2x-1] == 'F' or laberinto[j2y][j2x-1] == 'I'):
                if (movActual2 > siguenteMov2): 
                    j2x -= 1
                    siguenteMov2 = movActual2 + 80
            elif keys[pygame.K_d] and j2x < len(laberinto[0])-1 and (not laberinto[j2y][j2x+1] or laberinto[j2y][j2x+1] == 'F' or laberinto[j2y][j2x+1] == 'I'):
                if (movActual2 > siguenteMov2):
                    j2x += 1
                    siguenteMov2 = movActual2 + 80
            elif keys[pygame.K_w] and j2y > 0 and (not laberinto[j2y-1][j2x] or laberinto[j2y-1][j2x] == 'F' or laberinto[j2y-1][j2x] == 'I'):
                if (movActual2 > siguenteMov2):
                    j2y -= 1
                    siguenteMov2 = movActual1 + 80 
            elif keys[pygame.K_s] and j2y < len(laberinto)-1 and (not laberinto[j2y+1][j2x] or laberinto[j2y+1][j2x] == 'F' or laberinto[j2y+1][j2x] == 'I'):
                if (movActual2 > siguenteMov2):
                    j2y += 1
                    siguenteMov2 = movActual1 + 80  
            if (pacman_x,pacman_y) == (fin[0],fin[1]) or (j2x,j2y) == (fin[0],fin[1]):
                #Funcionalidades de jugador 2
                if jug2 == False:
                    nivel2(crear_laberinto(len(laberinto[0]),len(laberinto)),contadorSeg,False)
                else:
                    nivel2(crear_laberinto(len(laberinto[0]),len(laberinto)),contadorSeg,True)

            if botonRegresarNiveles.imprimirBotonInteractivo(negro):
                menuSeleccion()
            botonRegresarNiveles.textoEnBoton(fuente,'Regresar',blanco)
            
            pantalla.blit(textoPuntaje,(pantalla.get_width() - 150,pantalla.get_height()/3))
            pantalla.blit(texto,(pantalla.get_width() - 150,pantalla.get_height()/5))
            pantalla.blit(textoNivel,(pantalla.get_width() - 150,pantalla.get_height()/8))
            dibujar_pacman()
            if jug2 == True:
                dibujar_jugador2()
            pygame.display.flip()
            reloj.tick(30)

#Congela a pacman
def congelarPacman():
    global pacmanCongelado, pacmanDescongelarTiempo
    pacmanCongelado = True
    pacmanDescongelarTiempo = time.time() + 10  # 10 segundos de congelamiento

#Descongela a pacman
def descongelarPacman():
    global pacmanCongelado, pacmanDescongelarTiempo
    pacmanCongelado = False
    pacmanDescongelarTiempo = None

#Congela al jugador 2
def congelarJug2():
    global jug2Congelado, jug2DescongelarTiempo
    jug2Congelado = True
    jug2DescongelarTiempo = time.time() + 10  # 10 segundos de congelamiento

#Descongela al jugador 2
def descongelarJug2():
    global jug2Congelado, jug2DescongelarTiempo
    jug2Congelado = False
    jug2DescongelarTiempo = None


#Funcion de nivel 2
def nivel2(laberinto,puntajeActual,jug2):
    global pacman_x, pacman_y, j2x, j2y, fin, inicioPos, pacmanCongelado, jug2Congelado, pacmanDescongelarTiempo, jug2DescongelarTiempo, fondoImagen,botonRegresarNiveles
    pygame.mixer.music.play(-1)
    ancho, alto = (len(laberinto[0])*tamanoCelda) + 200,len(laberinto)*tamanoCelda
    pantalla = pygame.display.set_mode((ancho, alto))
    contadorSeg = 300
    segundos = contadorSeg % 60
    minutos = contadorSeg // 60
    textoNivel = fuente2.render('Nivel 2',True,(255,255,255))
    texto = fuente2.render(str(minutos) + ':' + "{:02d}".format(segundos),True,(255,255,255))
    textoPuntaje = fuente2.render(str(puntajeActual),True,(255,255,255))
    botonRegresarNiveles = Boton(pantalla.get_width()-160, pantalla.get_height()/2, 125, 50, colorBotones)
    eventoTiempo = pygame.USEREVENT + 1
    pygame.time.set_timer(eventoTiempo,1000)
    fondoPantalla = pygame.transform.scale(fondoImagen, (ancho, alto))

    # Encuentra la posición inicial y final en el laberinto
    inicioPos = None
    fin = None
    for y, fila in enumerate(laberinto):
        for x, celda in enumerate(fila):
            if celda == 'I':
                laberinto[y][x] = 0
                inicioPos = (random.randint(0,(len(laberinto[0])-1)//2), random.randint(0,(len(laberinto)-1)//2))
            elif celda == 'F':
                fin = (x, y)

    # Define la posición inicial de Pacman y del jugador 2
    pacman_x, pacman_y = inicioPos
    j2x,j2y = inicioPos
    laberinto[inicioPos[1]][inicioPos[0]] = 'I'
    siguenteMov1 = pygame.time.get_ticks() + 1000
    siguenteMov2 = pygame.time.get_ticks() + 1000
    #monstruo de congelar
    congelar = monstruo(len(laberinto),len(laberinto[0]))
    contadorFoto = 0
    retardoFoto = 5
    #velocidad de jugadores
    vel1 = 80
    vel2 = 80
    #variables para estados de congelamiento
    pacmanCongelado = jug2Congelado = False
    pacmanDescongelarTiempo = jug2DescongelarTiempo = None
    reducirMov1 = reducirMov2 = False
    reducirMov1Tiempo = reducirMov2Tiempo = None
    while True:
            pantalla.blit(fondoPantalla, (0, 0))
            movActual1 = pygame.time.get_ticks()
            movActual2 = pygame.time.get_ticks()
            renderMaze(laberinto)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == eventoTiempo:
                    contadorSeg -= 1
                    segundos = contadorSeg % 60
                    minutos = (contadorSeg//60) % 60
                    texto = fuente2.render(str(minutos) + ':' + "{:02d}".format(segundos),True,(255,255,255))    
                    if contadorSeg == 0:
                        terminado(1,puntajeActual)
            #movimiento de jugadores
            keys = pygame.key.get_pressed()
            if not pacmanCongelado:
                if keys[pygame.K_LEFT] and pacman_x > 0 and (not laberinto[pacman_y][pacman_x-1] or laberinto[pacman_y][pacman_x-1] == 'F' or laberinto[pacman_y][pacman_x-1] == 'I'):
                    if (movActual1 > siguenteMov1): 
                        pacman_x -= 1
                        siguenteMov1 = movActual1 + vel1
                elif keys[pygame.K_RIGHT] and pacman_x < len(laberinto[0])-1 and (not laberinto[pacman_y][pacman_x+1] or laberinto[pacman_y][pacman_x+1] == 'F' or laberinto[pacman_y][pacman_x+1] == 'I'):
                    if (movActual1 > siguenteMov1):
                        pacman_x += 1
                        siguenteMov1 = movActual1 +vel1
                elif keys[pygame.K_UP] and pacman_y > 0 and (not laberinto[pacman_y-1][pacman_x] or laberinto[pacman_y-1][pacman_x] == 'F' or laberinto[pacman_y-1][pacman_x] == 'I'):
                    if (movActual1 > siguenteMov1):
                        pacman_y -= 1
                        siguenteMov1 = movActual1 + vel1
                elif keys[pygame.K_DOWN] and pacman_y < len(laberinto)-1 and (not laberinto[pacman_y+1][pacman_x] or laberinto[pacman_y+1][pacman_x] == 'F' or laberinto[pacman_y+1][pacman_x] == 'I'):
                    if (movActual1 > siguenteMov1):
                        pacman_y += 1
                        siguenteMov1 = movActual1 + vel1
            if not jug2Congelado:
                if keys[pygame.K_a] and j2x > 0 and (not laberinto[j2y][j2x-1] or laberinto[j2y][j2x-1] == 'F' or laberinto[j2y][j2x-1] == 'I'):
                    if (movActual2 > siguenteMov2): 
                        j2x -= 1
                        siguenteMov2 = movActual2 + vel2
                elif keys[pygame.K_d] and j2x < len(laberinto[0])-1 and (not laberinto[j2y][j2x+1] or laberinto[j2y][j2x+1] == 'F' or laberinto[j2y][j2x+1] == 'I'):
                    if (movActual2 > siguenteMov2):
                        j2x += 1
                        siguenteMov2 = movActual2 + vel2
                elif keys[pygame.K_w] and j2y > 0 and (not laberinto[j2y-1][j2x] or laberinto[j2y-1][j2x] == 'F' or laberinto[j2y-1][j2x] == 'I'):
                    if (movActual2 > siguenteMov2):
                        j2y -= 1
                        siguenteMov2 = movActual1 + vel2
                elif keys[pygame.K_s] and j2y < len(laberinto)-1 and (not laberinto[j2y+1][j2x] or laberinto[j2y+1][j2x] == 'F' or laberinto[j2y+1][j2x] == 'I'):
                    if (movActual2 > siguenteMov2):
                        j2y += 1
                        siguenteMov2 = movActual1 + vel2  
            if (pacman_x,pacman_y) == (fin[0],fin[1]) or (j2x,j2y) == (fin[0],fin[1]):
                if jug2 == False:
                    nivel3(crear_laberinto(len(laberinto[0]),len(laberinto)),puntajeActual + contadorSeg,False)
                else:
                    nivel3(crear_laberinto(len(laberinto[0]),len(laberinto)),puntajeActual + contadorSeg,True)

            if botonRegresarNiveles.imprimirBotonInteractivo(negro):
                menuSeleccion()
            botonRegresarNiveles.textoEnBoton(fuente,'Regresar',blanco)

            pantalla.blit(textoPuntaje,(pantalla.get_width() - 150,pantalla.get_height()/3))
            pantalla.blit(texto,(pantalla.get_width() - 150,pantalla.get_height()/5))
            pantalla.blit(textoNivel,(pantalla.get_width() - 150,pantalla.get_height()/8))
            #revisar si el monstruo de congelar toca al jugador 1
            if congelar.verificarCol((pacman_y,pacman_x)):
                congelarPacman()
            dibujar_pacman()
            #estados de congelamiento
            if pacmanCongelado and time.time() >= pacmanDescongelarTiempo:
                descongelarPacman()
                reducirMov1 = True
                reducirMov1Tiempo = time.time() + 5
                vel1 = 200
            if reducirMov1 and time.time() >= reducirMov1Tiempo:
                vel1 = 80
                reducirMov1Tiempo = None
                reducirMov1 = False
            #revisar si el monstruo de congelar toca al jugador 2 y lo dibuja 
            if jug2 == True:
                if congelar.verificarCol((j2y,j2x)):
                    congelarJug2()
                dibujar_jugador2()
                if jug2Congelado and time.time() >= jug2DescongelarTiempo:
                    descongelarJug2()
                    reducirMov2 = True
                    reducirMov2Tiempo = time.time() + 5
                    vel2 = 150
                if reducirMov2 and time.time() >= reducirMov2Tiempo:
                    vel2 = 80
                    reducirMov2Tiempo = None
                    reducirMov2 = False
            #Controla velocidad de monstruo
            if contadorFoto % retardoFoto == 0:
                congelar.mover(laberinto)
            contadorFoto += 1
            congelar.dibujar(pantalla,congelaColor,tamanoCelda)
            pygame.display.flip()

            reloj.tick(30)

#Funcion nivel 3
def nivel3(laberinto,puntajeActual,jug2):
    global pacman_x,pacman_y,j2x,j2y, fin, inicioPos, fondoImagen,botonRegresarNiveles
    pygame.mixer.music.play(-1)
    ancho, alto = (len(laberinto[0])*tamanoCelda) + 200,len(laberinto)*tamanoCelda
    pantalla = pygame.display.set_mode((ancho, alto))
    contadorSeg = 300
    segundos = contadorSeg % 60
    minutos = contadorSeg // 60
    textoNivel = fuente2.render('Nivel 3',True,(255,255,255))
    texto = fuente2.render(str(minutos) + ':' + "{:02d}".format(segundos),True,(255,255,255))
    textoPuntaje = fuente2.render(str(puntajeActual),True,(255,255,255))
    botonRegresarNiveles = Boton(pantalla.get_width()-160, pantalla.get_height()/2, 125, 50, colorBotones)
    eventoTiempo = pygame.USEREVENT + 1
    pygame.time.set_timer(eventoTiempo,1000)
    fondoPantalla = pygame.transform.scale(fondoImagen, (ancho, alto))

    # Encuentra la posición inicial y final en el laberinto
    inicioPos = None
    fin = None
    for y, fila in enumerate(laberinto):
        for x, celda in enumerate(fila):
            if celda == 'I':
                laberinto[y][x] = 0
                inicioPos = (random.randint(0,(len(laberinto[0])-1)//2), random.randint(0,(len(laberinto)-1)//2))
            elif celda == 'F':
                fin = (x, y)

    # Define la posición inicial de Pacman y del jugador 2
    pacman_x, pacman_y = inicioPos
    j2x,j2y = inicioPos
    laberinto[inicioPos[1]][inicioPos[0]] = 'I'
    # Define el monstruo 
    mata = monstruo(len(laberinto),len(laberinto[0]))
    contadorFoto = 0
    retardoFoto = 5
    siguenteMov1 = pygame.time.get_ticks() + 1000
    siguenteMov2 = pygame.time.get_ticks() + 1000
    while True:
            pantalla.blit(fondoPantalla, (0, 0))
            movActual1 = pygame.time.get_ticks()
            movActual2 = pygame.time.get_ticks()
            renderMaze(laberinto)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == eventoTiempo:
                    contadorSeg -= 1
                    segundos = contadorSeg % 60
                    minutos = (contadorSeg//60) % 60
                    texto = fuente2.render(str(minutos) + ':' + "{:02d}".format(segundos),True,(255,255,255))    
                    if contadorSeg == 0:
                        terminado(2,puntajeActual)
            #movimiento de los jugadores 
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and pacman_x > 0 and (not laberinto[pacman_y][pacman_x-1] or laberinto[pacman_y][pacman_x-1] == 'F' or laberinto[pacman_y][pacman_x-1] == 'I'):
                if (movActual1 > siguenteMov1): 
                    pacman_x -= 1
                    siguenteMov1 = movActual1 + 80
            elif keys[pygame.K_RIGHT] and pacman_x < len(laberinto[0])-1 and (not laberinto[pacman_y][pacman_x+1] or laberinto[pacman_y][pacman_x+1] == 'F' or laberinto[pacman_y][pacman_x+1] == 'I'):
                if (movActual1 > siguenteMov1):
                    pacman_x += 1
                    siguenteMov1 = movActual1 + 80
            elif keys[pygame.K_UP] and pacman_y > 0 and (not laberinto[pacman_y-1][pacman_x] or laberinto[pacman_y-1][pacman_x] == 'F' or laberinto[pacman_y-1][pacman_x] == 'I'):
                if (movActual1 > siguenteMov1):
                    pacman_y -= 1
                    siguenteMov1 = movActual1 + 80 
            elif keys[pygame.K_DOWN] and pacman_y < len(laberinto)-1 and (not laberinto[pacman_y+1][pacman_x] or laberinto[pacman_y+1][pacman_x] == 'F' or laberinto[pacman_y+1][pacman_x] == 'I'):
                if (movActual1 > siguenteMov1):
                    pacman_y += 1
                    siguenteMov1 = movActual1 + 80
            if keys[pygame.K_a] and j2x > 0 and (not laberinto[j2y][j2x-1] or laberinto[j2y][j2x-1] == 'F' or laberinto[j2y][j2x-1] == 'I'):
                if (movActual2 > siguenteMov2): 
                    j2x -= 1
                    siguenteMov2 = movActual2 + 80
            elif keys[pygame.K_d] and j2x < len(laberinto[0])-1 and (not laberinto[j2y][j2x+1] or laberinto[j2y][j2x+1] == 'F' or laberinto[j2y][j2x+1] == 'I'):
                if (movActual2 > siguenteMov2):
                    j2x += 1
                    siguenteMov2 = movActual2 + 80
            elif keys[pygame.K_w] and j2y > 0 and (not laberinto[j2y-1][j2x] or laberinto[j2y-1][j2x] == 'F' or laberinto[j2y-1][j2x] == 'I'):
                if (movActual2 > siguenteMov2):
                    j2y -= 1
                    siguenteMov2 = movActual1 + 80 
            elif keys[pygame.K_s] and j2y < len(laberinto)-1 and (not laberinto[j2y+1][j2x] or laberinto[j2y+1][j2x] == 'F' or laberinto[j2y+1][j2x] == 'I'):
                if (movActual2 > siguenteMov2):
                    j2y += 1
                    siguenteMov2 = movActual1 + 80  
            if (pacman_x,pacman_y) == (fin[0],fin[1]) or (j2x,j2y) == (fin[0],fin[1]):
                if jug2 == False:
                    nivel4(crear_laberinto(len(laberinto[0]),len(laberinto)),puntajeActual + contadorSeg,False)
                else:
                    nivel4(crear_laberinto(len(laberinto[0]),len(laberinto)),puntajeActual + contadorSeg,True)

            if botonRegresarNiveles.imprimirBotonInteractivo(negro):
                menuSeleccion()
            botonRegresarNiveles.textoEnBoton(fuente,'Regresar',blanco)

            pantalla.blit(textoPuntaje,(pantalla.get_width() - 150,pantalla.get_height()/3))
            pantalla.blit(texto,(pantalla.get_width() - 150,pantalla.get_height()/5))
            pantalla.blit(textoNivel,(pantalla.get_width() - 150,pantalla.get_height()/8))
            if mata.verificarCol((pacman_y,pacman_x)):
                terminado(2,puntajeActual)
            dibujar_pacman()
            #Define funciones del jugador 2
            if jug2 == True:
                if mata.verificarCol((j2y,j2x)):
                    terminado(2,puntajeActual)
                dibujar_jugador2()
            #movimiento del monstruo
            if contadorFoto % retardoFoto == 0:
                mata.mover(laberinto)
            contadorFoto += 1
            mata.dibujar(pantalla,mataColor,tamanoCelda)
            pygame.display.flip()
            reloj.tick(30)

#Funcion nivel 4
def nivel4(laberinto,puntajeActual,jug2):
    global pacman_x, pacman_y, j2x, j2y, fin, inicioPos, pacmanCongelado, jug2Congelado, pacmanDescongelarTiempo, jug2DescongelarTiempo, fondoImagen,botonRegresarNiveles
    pygame.mixer.music.play(-1)
    ancho, alto = (len(laberinto[0])*tamanoCelda) + 200,len(laberinto)*tamanoCelda
    pantalla = pygame.display.set_mode((ancho, alto))
    contadorSeg = 300
    segundos = contadorSeg % 60
    minutos = contadorSeg // 60
    textoNivel = fuente2.render('Nivel 4',True,(255,255,255)) 
    texto = fuente2.render(str(minutos) + ':' + "{:02d}".format(segundos),True,(255,255,255))
    textoPuntaje = fuente2.render(str(puntajeActual),True,(255,255,255))
    botonRegresarNiveles = Boton(pantalla.get_width()-160, pantalla.get_height()/2, 125, 50, colorBotones)
    eventoTiempo = pygame.USEREVENT + 1
    pygame.time.set_timer(eventoTiempo,1000)
    fondoPantalla = pygame.transform.scale(fondoImagen, (ancho, alto))
    # Encuentra la posición inicial y final en el laberinto
    inicioPos = None
    fin = None
    for y, fila in enumerate(laberinto):
        for x, celda in enumerate(fila):
            if celda == 'I':
                laberinto[y][x] = 0
                inicioPos = (random.randint(0,(len(laberinto[0])-1)//2), random.randint(0,(len(laberinto)-1)//2))
            elif celda == 'F':
                fin = (x, y)

    # Define la posición inicial de Pacman y del jugador 2
    pacman_x, pacman_y = inicioPos
    j2x,j2y = inicioPos
    laberinto[inicioPos[1]][inicioPos[0]] = 'I'
    # Define los mosntruos
    mata = monstruo(len(laberinto),len(laberinto[0]))
    contadorFoto1 = 0
    retardoFoto1 = 3
    congelar = monstruo(len(laberinto),len(laberinto[0]))
    contadorFoto2 = 0
    retardoFoto2 = 3
    #velocidad de jugadores
    vel1 = 80
    vel2 = 80
    #variables para estados de congelamiento
    pacmanCongelado = jug2Congelado = False
    pacmanDescongelarTiempo = jug2DescongelarTiempo = None
    reducirMov1 = reducirMov2 = False
    reducirMov1Tiempo = reducirMov2Tiempo = None
    pacmanCongelado = jug2Congelado = False
    pacmanDescongelarTiempo = jug2DescongelarTiempo = None
    siguenteMov1 = pygame.time.get_ticks() + 1000
    siguenteMov2 = pygame.time.get_ticks() + 1000
    while True:
            pantalla.blit(fondoPantalla, (0, 0))
            movActual1 = pygame.time.get_ticks()
            movActual2 = pygame.time.get_ticks()
            renderMaze(laberinto)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == eventoTiempo:
                    contadorSeg -= 1
                    segundos = contadorSeg % 60
                    minutos = (contadorSeg//60) % 60
                    texto = fuente2.render(str(minutos) + ':' + "{:02d}".format(segundos),True,(255,255,255))    
                    if contadorSeg == 0:
                        terminado(3,puntajeActual)
            #movimiento del jugador
            keys = pygame.key.get_pressed()
            if not pacmanCongelado:
                if keys[pygame.K_LEFT] and pacman_x > 0 and (not laberinto[pacman_y][pacman_x-1] or laberinto[pacman_y][pacman_x-1] == 'F' or laberinto[pacman_y][pacman_x-1] == 'I'):
                    if (movActual1 > siguenteMov1): 
                        pacman_x -= 1
                        siguenteMov1 = movActual1 + vel1
                elif keys[pygame.K_RIGHT] and pacman_x < len(laberinto[0])-1 and (not laberinto[pacman_y][pacman_x+1] or laberinto[pacman_y][pacman_x+1] == 'F' or laberinto[pacman_y][pacman_x+1] == 'I'):
                    if (movActual1 > siguenteMov1):
                        pacman_x += 1
                        siguenteMov1 = movActual1 +vel1
                elif keys[pygame.K_UP] and pacman_y > 0 and (not laberinto[pacman_y-1][pacman_x] or laberinto[pacman_y-1][pacman_x] == 'F' or laberinto[pacman_y-1][pacman_x] == 'I'):
                    if (movActual1 > siguenteMov1):
                        pacman_y -= 1
                        siguenteMov1 = movActual1 + vel1
                elif keys[pygame.K_DOWN] and pacman_y < len(laberinto)-1 and (not laberinto[pacman_y+1][pacman_x] or laberinto[pacman_y+1][pacman_x] == 'F' or laberinto[pacman_y+1][pacman_x] == 'I'):
                    if (movActual1 > siguenteMov1):
                        pacman_y += 1
                        siguenteMov1 = movActual1 + vel1
            if not jug2Congelado:
                if keys[pygame.K_a] and j2x > 0 and (not laberinto[j2y][j2x-1] or laberinto[j2y][j2x-1] == 'F' or laberinto[j2y][j2x-1] == 'I'):
                    if (movActual2 > siguenteMov2): 
                        j2x -= 1
                        siguenteMov2 = movActual2 + vel2
                elif keys[pygame.K_d] and j2x < len(laberinto[0])-1 and (not laberinto[j2y][j2x+1] or laberinto[j2y][j2x+1] == 'F' or laberinto[j2y][j2x+1] == 'I'):
                    if (movActual2 > siguenteMov2):
                        j2x += 1
                        siguenteMov2 = movActual2 + vel2
                elif keys[pygame.K_w] and j2y > 0 and (not laberinto[j2y-1][j2x] or laberinto[j2y-1][j2x] == 'F' or laberinto[j2y-1][j2x] == 'I'):
                    if (movActual2 > siguenteMov2):
                        j2y -= 1
                        siguenteMov2 = movActual1 + vel2
                elif keys[pygame.K_s] and j2y < len(laberinto)-1 and (not laberinto[j2y+1][j2x] or laberinto[j2y+1][j2x] == 'F' or laberinto[j2y+1][j2x] == 'I'):
                    if (movActual2 > siguenteMov2):
                        j2y += 1
                        siguenteMov2 = movActual1 + vel2  
            if (pacman_x,pacman_y) == (fin[0],fin[1]) or (j2x,j2y) == (fin[0],fin[1]):
                terminado(4,puntajeActual + contadorSeg)

            if botonRegresarNiveles.imprimirBotonInteractivo(negro):
                menuSeleccion()
            botonRegresarNiveles.textoEnBoton(fuente,'Regresar',blanco)

            pantalla.blit(textoPuntaje,(pantalla.get_width() - 150,pantalla.get_height()/3))
            pantalla.blit(texto,(pantalla.get_width() - 150,pantalla.get_height()/5))
            pantalla.blit(textoNivel,(pantalla.get_width() - 150,pantalla.get_height()/8))
            if mata.verificarCol((pacman_y,pacman_x)):
                terminado(3,puntajeActual)
            #revisar si el monstruo de congelar toca al jugador 1
            if congelar.verificarCol((pacman_y,pacman_x)):
                congelarPacman()
            #estados de congelamiento
            if pacmanCongelado and time.time() >= pacmanDescongelarTiempo:
                descongelarPacman()
                reducirMov1 = True
                reducirMov1Tiempo = time.time() + 5
                vel1 = 200
            if reducirMov1 and time.time() >= reducirMov1Tiempo:
                vel1 = 80
                reducirMov1Tiempo = None
                reducirMov1 = False
            dibujar_pacman()
            #interaccion con monstruos con 2 jugadores
            if jug2 == True:
                if mata.verificarCol((j2y,j2x)):
                    terminado(3,puntajeActual)
                if congelar.verificarCol((j2y,j2x)):
                    congelarJug2()
                if jug2Congelado and time.time() >= jug2DescongelarTiempo:
                    descongelarJug2()
                    reducirMov2 = True
                    reducirMov2Tiempo = time.time() + 5
                    vel2 = 150
                if reducirMov2 and time.time() >= reducirMov2Tiempo:
                    vel2 = 80
                    reducirMov2Tiempo = None
                    reducirMov2 = False
                dibujar_jugador2()
            
            #define monstruos y sus velocidades
            if contadorFoto1 % retardoFoto1 == 0:
                mata.mover(laberinto)
            contadorFoto1 += 1
            mata.dibujar(pantalla,mataColor,tamanoCelda)
            if contadorFoto2 % retardoFoto2 == 0:
                congelar.mover(laberinto)
            contadorFoto2 += 1
            congelar.dibujar(pantalla,congelaColor,tamanoCelda)
            pygame.display.flip()
            reloj.tick(30)

#texto final para el modo simple
def final(texto):
    textoFinal = fuente2.render(texto,True,blanco)
    textoFinalrect = textoFinal.get_rect(center=(pantalla.get_width()/2,pantalla.get_height()/3))
    pantalla.blit(textoFinal,textoFinalrect)
    botonFinal = Boton(pantalla.get_width()/1.2,pantalla.get_height()/1.1, 125, 50, colorBotones)
    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
        if botonFinal.imprimirBotonInteractivo(negro):
            menuSeleccion()
        botonFinal.textoEnBoton(fuente,'regresar',blanco)
        pygame.display.update()


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
            elif celda == 'F':
                fin = (x, y)

    # Define la posición inicial de Pacman
    pacman_x, pacman_y = inicioPos
    siguenteMov = pygame.time.get_ticks() + 1000
    #pausa
    paused = False
    botonFinal = Boton(pantalla.get_width()/1.2,pantalla.get_height()/1.1, 125, 50, colorBotones)
    while True:
            movActual = pygame.time.get_ticks()
            renderMaze(laberinto)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                #revisa si esta pausado o no
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and paused == False:
                        paused = True
                    elif event.key == pygame.K_ESCAPE and paused == True:
                        paused = False
            #movimiento de los jugadores
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and pacman_x > 0 and (not laberinto[pacman_y][pacman_x-1] or laberinto[pacman_y][pacman_x-1] == 'F' or laberinto[pacman_y][pacman_x-1] == 'I'):
                if (movActual > siguenteMov): 
                    pacman_x -= 1
                    siguenteMov = movActual + 80
            elif keys[pygame.K_RIGHT] and pacman_x < len(laberinto[0])-1 and (not laberinto[pacman_y][pacman_x+1] or laberinto[pacman_y][pacman_x+1] == 'F' or laberinto[pacman_y][pacman_x+1] == 'I'):
                if (movActual > siguenteMov):
                    pacman_x += 1
                    siguenteMov = movActual + 80
            elif keys[pygame.K_UP] and pacman_y > 0 and (not laberinto[pacman_y-1][pacman_x] or laberinto[pacman_y-1][pacman_x] == 'F' or laberinto[pacman_y-1][pacman_x] == 'I'):
                if (movActual > siguenteMov):
                    pacman_y -= 1
                    siguenteMov = movActual + 80 
            elif keys[pygame.K_DOWN] and pacman_y < len(laberinto)-1 and (not laberinto[pacman_y+1][pacman_x] or laberinto[pacman_y+1][pacman_x] == 'F' or laberinto[pacman_y+1][pacman_x] == 'I'):
                if (movActual > siguenteMov):
                    pacman_y += 1
                    siguenteMov = movActual + 80  
            if (pacman_x,pacman_y) == (fin[0],fin[1]):
                final('¡Has ganado!')
            #muestra el boton de regresar
            if paused == True:
                if botonFinal.imprimirBotonInteractivo(negro):
                        menuSeleccion()
                botonFinal.textoEnBoton(fuente,'regresar',blanco)
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

#resuelve el laberinto 
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
            final('LABERINTO SIN SOLUCIÓN')
        final('Número de movimientos requeridos: ' + str(len(sol) - 1))

#Menu de seleccion de modo para jugar
def selecMododeSol(laberinto):
    global fondoImagen
    corriendo = True
    textoSol = fuente2.render('Seleccione el metodo de solucion:',True,blanco)
    textoSolrect = textoSol.get_rect(center=(pantallaLargo/2,(pantallaAncho/2) - 125))
    fondoPantalla = pygame.transform.scale(fondoImagen, (pantallaLargo, pantallaAncho))

    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
        pantalla.blit(fondoPantalla, (0, 0))
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
    global fondoImagen
    corriendo = True
    textoBox = pygame.Rect(350,400,400,40)
    entrada = ''
    activo = False
    textoIngreso = fuente2.render('Ingrese el nombre de su laberinto',True,blanco)
    textoIngresorect = textoIngreso.get_rect(center=(pantallaLargo/2,(pantallaAncho/2) - 125))
    fondoPantalla = pygame.transform.scale(fondoImagen, (pantallaLargo, pantallaAncho))
    
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
        pantalla.blit(fondoPantalla, (0, 0))
        pantalla.blit(textoIngreso,textoIngresorect) 
        pygame.draw.rect(pantalla,colorBotones,textoBox)
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
        botonOk.textoEnBoton(fuente,'Aceptar',blanco)
        if botonRegresar.imprimirBotonInteractivo(negro):
            menuSeleccion()
        botonRegresar.textoEnBoton(fuente,'Regresar',blanco)
        pygame.display.update()



#Funcion para que el usuario genere el laberinto
def dimensionesGenerar():
    global fondoImagen
    corriendo = True
    textoAncho = fuente.render('Ancho',True,blanco)
    textoAlto = fuente.render('Alto',True,blanco)
    textoBox1 = pygame.Rect(350,400,100,40)
    textoBox2 = pygame.Rect(650,400,100,40)
    entrada1 = ''
    entrada2 = ''
    activo1 = False
    activo2 = False
    textoIngreso = fuente2.render('Ingrese las dimensiones de su laberinto:',True,blanco)
    textoIngresorect = textoIngreso.get_rect(center=(pantallaLargo/2,(pantallaAncho/2) - 125))
    fondoPantalla = pygame.transform.scale(fondoImagen, (pantallaLargo, pantallaAncho))
    
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
        pantalla.blit(fondoPantalla, (0, 0))
        pantalla.blit(textoIngreso,textoIngresorect) 
        pygame.draw.rect(pantalla,colorBotones,textoBox1)
        pygame.draw.rect(pantalla,colorBotones,textoBox2)
        textoEntrada1 = fuente.render(entrada1,True,blanco)
        textoEntrada2 = fuente.render(entrada2,True,blanco)
        pantalla.blit(textoAncho,(365,360))
        pantalla.blit(textoAlto,(675,360))
        pantalla.blit(textoEntrada1,(textoBox1.x + 5, textoBox1.y + 5))
        pantalla.blit(textoEntrada2,(textoBox2.x + 5, textoBox2.y + 5))
        if botonOk.imprimirBotonInteractivo(negro):
            try:
                ancho = int(entrada1) 
                alto = int(entrada2)
                if 50<=ancho<=100 and 50<=alto<=100:
                    return crear_laberinto(ancho,alto)
            except:
                continue
            
        botonOk.textoEnBoton(fuente,'Aceptar',blanco)
        if botonRegresar.imprimirBotonInteractivo(negro):
            menuSeleccion()
        botonRegresar.textoEnBoton(fuente,'Regresar',blanco)
        pygame.display.update()


#Menu de seleccion 
def menuSeleccion():
    pygame.mixer.music.stop()
    global fondoImagen
    if fondoImagen == fondoCongelado:
        pygame.mixer.music.load('Canciones/laberintoCongelado.mp3')
    elif fondoImagen == fondoTropical:
        pygame.mixer.music.load('Canciones/laberintoJungla.mp3')
    pantallaLargo = 1100
    pantallaAncho = 600
    pantalla = pygame.display.set_mode((pantallaLargo, pantallaAncho))
    corriendo = True
    textoMenu = fuente2.render('Seleccione el modo de juego:', True, blanco)
    textoMunurect = textoMenu.get_rect(center=(pantallaLargo/2,(pantallaAncho/2) - 125))
    fondoPantalla = pygame.transform.scale(fondoImagen, (pantallaLargo, pantallaAncho))

    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
        pantalla.blit(fondoPantalla, (0, 0))
        if botonCargar.imprimirBotonInteractivo(negro):
            laberintoSelec = cargarLaberinto()
            selecMododeSol(laberintoSelec)
        botonCargar.textoEnBoton(fuente,'Cargar',blanco)
        if botonGenerar.imprimirBotonInteractivo(negro):
            laberintoSelec = dimensionesGenerar()
            selecMododeSol(laberintoSelec)
        botonGenerar.textoEnBoton(fuente,'Generar',blanco)
        if botonAventura.imprimirBotonInteractivo(negro):
            laberintoSelec = dimensionesGenerar()
            nivel1(laberintoSelec,False)
        botonAventura.textoEnBoton(fuente,'Aventura',blanco)
        if botonCompetitivo.imprimirBotonInteractivo(negro):
            laberintoSelec = dimensionesGenerar()
            nivel1(laberintoSelec,True)
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

    if botonConfiguracion.imprimirBotonInteractivo(negro):
        configuracion()
    botonConfiguracion.textoEnBoton(fuente, 'Configuración', blanco)

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

    monstruo_x = animacion_inicio_x
    monstruo_y = animacion_inicio_y
    monstruo2_x = animacion_inicio_x
    monstruo2_y = animacion_inicio_y

    if direction == 1:
        monstruo_x -= scaled_monstruo_image.get_width()
        monstruo2_x += scaled_image.get_width()
    elif direction == -1:
        monstruo_x += scaled_image.get_width()
        monstruo2_x -= scaled_monstruo2_image.get_width()
    elif direction == 0:
        monstruo_y -= scaled_monstruo_image.get_height()
        monstruo2_y += scaled_image.get_height()
    elif direction == 2:
        monstruo_y += scaled_image.get_height()
        monstruo2_y -= scaled_monstruo2_image.get_height()

    monstruo_x = max(0, monstruo_x)
    monstruo_x = min(pantallaLargo - scaled_monstruo_image.get_width(), monstruo_x)
    monstruo_y = max(0, monstruo_y)
    monstruo_y = min(pantallaAncho - scaled_monstruo_image.get_height(), monstruo_y)

    monstruo2_x = max(0, monstruo2_x)
    monstruo2_x = min(pantallaLargo - scaled_monstruo2_image.get_width(), monstruo2_x)
    monstruo2_y = max(0, monstruo2_y)
    monstruo2_y = min(pantallaAncho - scaled_monstruo2_image.get_height(), monstruo2_y)

    pantalla.blit(scaled_image, (animacion_inicio_x, animacion_inicio_y))
    pantalla.blit(scaled_monstruo_image, (monstruo_x, monstruo_y))
    pantalla.blit(scaled_monstruo2_image, (monstruo2_x, monstruo2_y))

#Funcion inicial 
def inicio():
    global fondoImagen

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
    fondoPantalla = pygame.transform.scale(fondoImagen, (pantallaLargo, pantallaAncho))

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

        pantalla.blit(fondoPantalla, (0, 0))

        pantalla.blit(textoEscalaSombra, textoEscalaRectSombra)
        pantalla.blit(textoEscala, textoEscalaRect)

        dibujar_botones_inicio()

        actualizar_posicion_imagenes()

        pygame.display.update()
        clock.tick(60)
        
    pygame.quit()

inicio()