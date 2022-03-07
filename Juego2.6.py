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

# Definir fuente
font = pygame.font.SysFont('Bauhaus 93', 60)

# Definir colores
white = (255, 255, 255)

# Definir las variables del juego
desplazamiento_suelo = 0
velocidad_desplazamiento = 4
volador = False
juego_terminado = False
brecha_tuberia = 150
frecuencia_tuberia = 1500 # Milisegundos
ultima_tuberia = pygame.time.get_ticks() - frecuencia_tuberia
puntaje = 0
paso_tubo = False


# Cargar imagemes
imagen_fondo = pygame.image.load('img/bg.png')
imagen_suelo = pygame.image.load('img/ground.png')
button_img = pygame.image.load('img/restart.png')


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    pantalla.blit(img, (x, y))


def reset_game():
    grupo_tuberias.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(pantalla_altura / 2)
    puntaje = 0
    return puntaje



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


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):

        action = False

        # Obtener la posición del ratón
        pos = pygame.mouse.get_pos()

        # Compruebe si el mouse está sobre el botón
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        # Dibujar botón
        pantalla.blit(self.image, (self.rect.x, self.rect.y))

        return action

grupo_aves = pygame.sprite.Group()
grupo_tuberias = pygame.sprite.Group()

flappy = Pajaro(100, int(pantalla_altura / 2))

grupo_aves.add(flappy)

# Crear instancia de botón de reinicio
button = Button(pantalla_ancho // 2 - 50, pantalla_altura // 2 - 100, button_img)

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

    # Comprobar la puntuación
    if len(grupo_tuberias) > 0:
        if grupo_aves.sprites()[0].rect.left > grupo_tuberias.sprites()[0].rect.left\
            and grupo_aves.sprites()[0].rect.right < grupo_tuberias.sprites()[0].rect.right\
            and paso_tubo == False:
            paso_tubo = True
        if paso_tubo == True:
            if grupo_aves.sprites()[0].rect.left > grupo_tuberias.sprites()[0].rect.right:
                puntaje += 1
                paso_tubo = False


    draw_text(str(puntaje), font, white, int(pantalla_ancho / 2), 20)

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


    # Comprueba si el juego ha terminado y reinicia
    if juego_terminado == True:
        if button.draw() == True:
            juego_terminado = False
            puntaje = reset_game()



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and volador == False and juego_terminado == False:
            volador = True

    pygame.display.update()

pygame.quit()