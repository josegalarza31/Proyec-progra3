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
velocida_desplazamineto = 4

# Cargar imagenes
imagen_fondo = pygame.image.load('img/bg.png')
imagen_suelo = pygame.image.load('img/ground.png')

run = True
while run:

    clock.tick(fps)

    # Dibujar fondo
    pantalla.blit(imagen_fondo, (0,0))

    # Dibujar y desplazar el suelo
    pantalla.blit(imagen_suelo, (desplazamiento_suelo, 768))
    desplazamiento_suelo -= velocida_desplazamineto
    if abs(desplazamiento_suelo) > 35:
        desplazamiento_suelo = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update()

pygame.quit()