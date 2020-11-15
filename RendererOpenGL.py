import pygame
from pygame.locals import *

from gl import Renderer
import shaders



deltaTime = 0.0

# Inicializacion de pygame
pygame.init()
clock = pygame.time.Clock()
screenSize = (960, 540)
screen = pygame.display.set_mode(screenSize, DOUBLEBUF | OPENGL)

# Inicializacion de nuestro Renderer en OpenGL
r = Renderer(screen)
r.setShaders(shaders.vertex_shader, shaders.fragment_shader)
r.createObjects()


camX = 0
camZ = 0
camRotZ = 0

isPlaying = True
while isPlaying:

    # Para revisar si una tecla esta presionada
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        camX -= 2 * deltaTime
    if keys[pygame.K_d]:
        camX += 2 * deltaTime
    if keys[pygame.K_w]:
        camZ -= 2 * deltaTime
    if keys[pygame.K_s]:
        camZ += 2 * deltaTime
    # ROTACION CAM
    if keys[pygame.K_q]:
        camZ += 0.5 * deltaTime
    if keys[pygame.K_e]:
        camZ -= 0.5 * deltaTime

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            isPlaying = False
        elif ev.type == pygame.KEYDOWN:
            # para revisar en el momento que se presiona una tecla
            if ev.key == pygame.K_1:
                r.filledMode()
            elif ev.key == pygame.K_2:
                r.wireframeMode
            elif ev.key == pygame.K_ESCAPE:
                isPlaying = False


    r.translateCam(camX, 0, camZ)
    r.rotateCam(0, 0, camRotZ)

    # Main Renderer Loop
    r.render()

    pygame.display.flip()
    clock.tick(60)
    deltaTime = clock.get_time() / 1000


pygame.quit()
