import pygame
from pygame.locals import *
import random

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
volador = False
juego_terminado = False
brecha_tuberia = 150
frecuencia_tuberia = 1500 # Milisegundos
ultima_tuberia = pygame.time.get_ticks() - frecuencia_tuberia


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
        
        self.vel = 0
        self.clicked = False

    def update(self):

        if volador == True:
            # Gravedad
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)

        if juego_terminado == False:
            # Salto
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            # Manejar la animación
            self.contador += 1
            enfriamiento_aleteo = 5

            if self.contador > enfriamiento_aleteo:
                self.contador = 0
                self.indice += 1
                if self.indice >= len(self.imagenes):
                    self.indice = 0
            self.image = self.imagenes[self.indice]

            # Girar el pájaro
            self.image = pygame.transform.rotate(self.imagenes[self.indice], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.imagenes[self.indice], -90)



class Tuberias(pygame.sprite.Sprite):
    def __init__(self, x, y, posicion):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/pipe.png')
        self.rect = self.image.get_rect()
        # La posición 1 es desde arriba, -1 es desde abajo
        if posicion == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(brecha_tuberia / 2)]
        if posicion == -1:
            self.rect.topleft = [x, y + int(brecha_tuberia / 2)]

    def update(self):
        self.rect.x -= velocidad_desplazamiento
        if self.rect.right < 0:
            self.kill()



grupo_aves = pygame.sprite.Group()
grupo_tuberias = pygame.sprite.Group()

flappy = Pajaro(100, int(pantalla_altura / 2))

grupo_aves.add(flappy)



run = True
while run:

    clock.tick(fps)

    # Dibujar el fondo
    pantalla.blit(imagen_fondo, (0,0))

    grupo_aves.draw(pantalla)
    grupo_aves.update()
    grupo_tuberias.draw(pantalla)

    # Dibujar el suelo
    pantalla.blit(imagen_suelo, (desplazamiento_suelo, 768))

    # Buscar colisión
    if pygame.sprite.groupcollide(grupo_aves, grupo_tuberias, False, False) or flappy.rect.top < 0:
        juego_terminado = True

    # Comprobar si el pajaro ha tocado el suelo
    if flappy.rect.bottom >= 768:
        juego_terminado = True
        volador = False


    if juego_terminado == False and volador == True:

        # Generar nuevas tuberías
        time_now = pygame.time.get_ticks()
        if time_now - ultima_tuberia > frecuencia_tuberia:
            altura_tuberia = random.randint(-100, 100)
            btm_tubo = Tuberias(pantalla_ancho, int(pantalla_altura / 2) + altura_tuberia, -1)
            tubo_superior = Tuberias(pantalla_ancho, int(pantalla_altura / 2) + altura_tuberia, 1)
            grupo_tuberias.add(btm_tubo)
            grupo_tuberias.add(tubo_superior)
            ultima_tuberia = time_now


        # Dibujar y desplazar el suelo
        desplazamiento_suelo -= velocidad_desplazamiento
        if abs(desplazamiento_suelo) > 35:
            desplazamiento_suelo = 0

        grupo_tuberias.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and volador == False and juego_terminado == False:
            volador = True

    pygame.display.update()

pygame.quit()