import pygame
import sys
from math import cos, sin, pi

from gl import *

from pygame.constants import KEYDOWN, K_ESCAPE, MOUSEBUTTONDOWN, MOUSEBUTTONUP, QUIT


pygame.init()
screen = pygame.display.set_mode((500,500), pygame.DOUBLEBUF | pygame.HWACCEL) #, pygame.FULLSCREEN)
screen.set_alpha(None)
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

pygame.mixer.music.load("music/C418 - Sweden - Minecraft Volume Alpha.mp3")

def updateFPS():
    fps = str(int(clock.get_fps()))
    fps = font.render(fps, 1, pygame.Color("white"))
    return fps

map_file = 'maps/map2.txt'
r = Raycaster(screen, map_file)

bg = pygame.image.load('bg.png')

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def main_menu ():
    click = False
    isPlaying = False

    while True:
        screen.blit(bg, (0,0))
        draw_text('MENÚ PRINCIPAL', font, (255, 255, 255), screen, r.width/3+25, 50)

        mx, my = pygame.mouse.get_pos()


        button_2 = pygame.Rect(r.width/3, 200, 200, 50)
        button_1 = pygame.Rect(r.width/3, 100, 200, 50)


        if button_1.collidepoint(mx, my): # Jugar
            if click:
                pygame.mixer.music.unpause()
                game()
                isPlaying = True

        if button_2.collidepoint(mx, my): # Salir
            if click:
                pygame.quit()
                sys.exit()

        pygame.draw.rect(screen, (255,0,0), button_1)
        pygame.draw.rect(screen, (255,0,0), button_2)

        play_btn_txt = "Continuar" if isPlaying else "Jugar"
        #Play button text
        play_text = font.render(play_btn_txt, False, (0, 0, 0))
        play_rect = play_text.get_rect(center=button_1.center)
        screen.blit(play_text, play_rect)

        #Quit button text
        play_text = font.render("Salir", False, (0, 0, 0))
        play_rect = play_text.get_rect(center=button_2.center)
        screen.blit(play_text, play_rect)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(60)

def game():
    isRunning = True
    while isRunning:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                isRunning = False

            newX = r.player['x']
            newY = r.player['y']

            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    pygame.mixer.music.pause()
                    isRunning = False
                elif ev.key == pygame.K_w:
                    newX += cos(r.player['angle'] * pi / 180) * r.stepSize
                    newY += sin(r.player['angle'] * pi / 180) * r.stepSize
                elif ev.key == pygame.K_s:
                    newX -= cos(r.player['angle'] * pi / 180) * r.stepSize
                    newY -= sin(r.player['angle'] * pi / 180) * r.stepSize
                elif ev.key == pygame.K_a:
                    newX -= cos((r.player['angle'] + 90) * pi / 180) * r.stepSize
                    newY -= sin((r.player['angle'] + 90) * pi / 180) * r.stepSize
                elif ev.key == pygame.K_d:
                    newX += cos((r.player['angle'] + 90) * pi / 180) * r.stepSize
                    newY += sin((r.player['angle'] + 90) * pi / 180) * r.stepSize
                elif ev.key == pygame.K_q:
                    r.player['angle'] -= 5
                elif ev.key == pygame.K_e:
                    r.player['angle'] += 5


                i = int(newX / r.blocksize)
                j = int(newY / r.blocksize)

                if r.map[j][i] == ' ':
                    r.player['x'] = newX
                    r.player['y'] = newY

        screen.fill(pygame.Color("gray")) # Background

        screen.fill(pygame.Color("skyblue"), (0, 0, int(r.width),int(r.height / 2))) # Sky
        
        screen.fill(pygame.Color("green"), (0, int(r.height/2), int(r.width),int(r.height / 2))) # Floor

        r.render()
        
        # FPS
        screen.fill(pygame.Color("black"), (0,0,30,30))
        screen.blit(updateFPS(), (0,0))
        clock.tick(30)
        
        pygame.display.update()

pygame.mixer.music.play(-1)
main_menu()


