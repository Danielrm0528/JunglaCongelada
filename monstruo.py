import pygame
import random

class monstruo:
    def __init__(self,filas,columnas):
        self.posicion = (filas - 2, columnas - 2)
        self.direccion = random.choice(['arriba', 'abajo', 'izquierda', 'derecha'])
        self.velocidad = 1
        self.contador_fotogramas = 0
        self.retardo_fotogramas = 30
        self.filas = filas
        self.columnas = columnas

    def mover(self,laberinto):
        opciones = []
        if self.direccion != 'abajo' and self.posicion[0] > 0: 
            if laberinto[self.posicion[0] - 1][self.posicion[1]] == 0 or laberinto[self.posicion[0] - 1][self.posicion[1]] == 'F' or laberinto[self.posicion[0] - 1][self.posicion[1]] == 'I':
                opciones.append('arriba')
        if self.direccion != 'arriba' and self.posicion[0] < self.filas - 1:
            if laberinto[self.posicion[0] + 1][self.posicion[1]] == 0 or laberinto[self.posicion[0] + 1][self.posicion[1]] == 'F' or laberinto[self.posicion[0] + 1][self.posicion[1]] == 'I':
                opciones.append('abajo')
        if self.direccion != 'derecha' and self.posicion[1] > 0:
            if laberinto[self.posicion[0]][self.posicion[1] - 1] == 0 or laberinto[self.posicion[0]][self.posicion[1] - 1] == 'F' or laberinto[self.posicion[0]][self.posicion[1] - 1] == 'I':
                opciones.append('izquierda')
        if self.direccion != 'izquierda' and self.posicion[1] < self.columnas - 1:
            if laberinto[self.posicion[0]][self.posicion[1] + 1] == 0 or laberinto[self.posicion[0]][self.posicion[1] + 1] == 'F' or laberinto[self.posicion[0]][self.posicion[1] + 1] == 'I':
                opciones.append('derecha')

        if len(opciones) > 0:
            self.direccion = random.choice(opciones)
        else:
            self.direccion = self.invertir_direccion(self.direccion)

        if self.direccion == 'arriba' and self.posicion[0] > 0:
            self.posicion = (self.posicion[0] - 1, self.posicion[1])
        elif self.direccion == 'abajo' and self.posicion[0] < self.filas - 1:
            self.posicion = (self.posicion[0] + 1, self.posicion[1])
        elif self.direccion == 'izquierda' and self.posicion[1] > 0:
            self.posicion = (self.posicion[0], self.posicion[1] - 1)
        elif self.direccion == 'derecha' and self.posicion[1] < self.columnas - 1:
            self.posicion = (self.posicion[0], self.posicion[1] + 1)

    def invertir_direccion(self, direccion):
        if direccion == 'arriba':
            return 'abajo'
        elif direccion == 'abajo':
            return 'arriba'
        elif direccion == 'izquierda':
            return 'derecha'
        elif direccion == 'derecha':
            return 'izquierda'

    def dibujar(self, pantalla,color,tamanoCelda):
        pygame.draw.circle(pantalla, color, (self.posicion[1] * tamanoCelda + tamanoCelda // 2, self.posicion[0] * tamanoCelda + tamanoCelda // 2), tamanoCelda // 2)
    
    def verificarCol(self,objeto):
        if self.posicion == (objeto[0],objeto[1]):
            return True
        else:
            return False
