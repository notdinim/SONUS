# NAMES: DINIM ONIGYE & EDAFE ETUKE
# OVERWORLD 3 / LEVEL 3 PICK SCREEN

# IMPORTS
import pygame
import sys

# SETUP
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# VARIABLES
button1 = pygame.image.load("../graphics/button1.png")
button2 = pygame.image.load("../graphics/button2.png")
button3 = pygame.image.load("../graphics/button3.png")
running = True

# GAME LOOP
while running:
    screen.fill("black")
    screen.blit(pygame.transform.scale2x(pygame.image.load("../graphics/scroll.png")), (-50, -50))
    screen.blit(button1, (50, 250))
    screen.blit(button2, (250, 250))
    screen.blit(button3, (450, 250))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button1.get_rect(topleft=(50, 250)).collidepoint(pygame.mouse.get_pos()):
                with open("main.py") as f:
                    exec(f.read())
            if button2.get_rect(topleft=(250, 250)).collidepoint(pygame.mouse.get_pos()):
                with open("main2.py") as f:
                    exec(f.read())
            if button3.get_rect(topleft=(450, 250)).collidepoint(pygame.mouse.get_pos()):
                with open("main3.py") as f:
                    exec(f.read())