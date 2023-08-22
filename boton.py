import pygame 

pygame.init()
pantalla = pygame.display.set_mode((1000,600))
pygame.display.set_caption('MusicBox')
fuente1 = pygame.font.Font("Fuentes/NexaHeavy.ttf",20)
fuente2 = pygame.font.Font("Fuentes/NexaHeavy.ttf",15)

class Boton:
    def __init__(self,x,y,ancho,largo,color): 
        self.color = color
        self.x = x
        self.y = y
        self.ancho = ancho
        self.largo = largo
        self.rect = pygame.Rect(x, y, ancho, largo)
        self.click = False
        self.pressed = False
        
    def imprimirBoton(self): 
        botonCreado = pygame.draw.rect(pantalla,self.color,self.rect)
        posicion = pygame.mouse.get_pos()
        if botonCreado.collidepoint(posicion):
            if pygame.mouse.get_pressed()[0] == True and self.pressed == False:
                self.pressed = True
            if pygame.mouse.get_pressed()[0] == False and self.pressed == True:
                self.click = True
                self.pressed = False
        else:
            if pygame.mouse.get_pressed()[0] == False:
                self.pressed = False
            self.click = False
                
    def imprimirBotonInteractivo(self,color2): 
        accion = False 
        posicion = pygame.mouse.get_pos()
        if self.rect.collidepoint(posicion):
            pygame.draw.rect(pantalla,color2,self.rect)
            if pygame.mouse.get_pressed()[0] == True and self.pressed == False:
                self.pressed = True
            if pygame.mouse.get_pressed()[0] == False and self.pressed == True:
                self.click = True
                accion = True
                self.pressed = False
        else:
            pygame.draw.rect(pantalla,self.color,self.rect)
            if pygame.mouse.get_pressed()[0] == False:
                self.pressed = False
            self.click = False
        return accion

    def textoEnBoton(self,fuente,texto,color):
        textoRender = fuente.render(texto,True,color)
        textoEnBoton = textoRender.get_width()
        pantalla.blit(textoRender, (self.x + int(self.ancho/2) - int(textoEnBoton / 2), self.y + 14)) 

class BotonConfiguracion(Boton):
    def __init__(self, color):
        super().__init__((pantalla.get_width() * 0.04),(pantalla.get_height() * 0.01),40,40,color) #Define el botonConfiguracion a partir de la clase Boton
