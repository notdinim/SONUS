# NAMES: DINIM ONIGYE & EDAFE ETUKE
# END SCREEN PROGRAM

# IMPORTS
import pygame
import sys

# SETUP
pygame.init()
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# AUDIO
pygame.mixer.music.load("../audio/sonus_music.wav")
pygame.mixer.music.set_volume(0.7)
pygame.mixer.music.play(-1)

# VARIABLES
running = True
end_screen = pygame.image.load("../graphics/end_screen.png")

# GAME LOOP
while running:
    for event in pygame.event.get():
        screen.blit(end_screen, (0, 0))
        pygame.display.update()
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                with open("SONUS.py") as f:
                    exec(f.read())

pygame.quit()
sys.exit()