import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60

pantalla_ancho = 864
pantalla_altura = 936

pantalla = pygame.display.set_mode((pantalla_ancho, pantalla_altura))
pygame.display.set_caption('Flappy Bird')


# Definir las variables del juego
desplazamiento_suelo = 0
velocidad_desplazamiento = 4

# Cargar imagenes
imagen_fondo = pygame.image.load('img/bg.png')
imagen_suelo = pygame.image.load('img/ground.png')


class Pajaro(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.imagenes = []
        self.indice = 0
        self.contador = 0
        for num in range(1, 4):
            img = pygame.image.load(f'img/bird{num}.png')
            self.imagenes.append(img)
        self.image = self.imagenes[self.indice]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):

        # Manejar las animación
        self.contador += 1
        enfriamiento_aleteo = 5

        if self.contador > enfriamiento_aleteo:
            self.contador = 0
            self.indice += 1
            if self.indice >= len(self.imagenes):
                self.indice = 0
        self.image = self.imagenes[self.indice]


grupo_aves = pygame.sprite.Group()

flappy = Pajaro(100, int(pantalla_altura / 2))

grupo_aves.add(flappy)


run = True
while run:

    clock.tick(fps)

    # Dibujar fondo
    pantalla.blit(imagen_fondo, (0,0))

    grupo_aves.draw(pantalla)
    grupo_aves.update()

    # Dibujar y desplazar el suelo
    pantalla.blit(imagen_suelo, (desplazamiento_suelo, 768))
    desplazamiento_suelo -= velocidad_desplazamiento
    if abs(desplazamiento_suelo) > 35:
        desplazamiento_suelo = 0


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()