# NAMES: DINIM ONIGYE & EDAFE ETUKE
# RESPAWN CONTROLS 3

# IMPORTS
import pygame
import sys
from pygame import gfxdraw

# SETUP
pygame.init()
WIDTH, HEIGHT = 1200, 704
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# VARIABLES
ticks = 3
running = True

# CUSTOM EVENTS
COUNTDOWN = pygame.USEREVENT + 1
pygame.time.set_timer(COUNTDOWN, 1000)

# FONTS
fibberish = pygame.font.Font("../fonts/fibberish.ttf", 20)
fibberish_medium = pygame.font.Font("../fonts/fibberish.ttf", 30)
fibberish_large = pygame.font.Font("../fonts/fibberish.ttf", 40)

def draw():
    """This function draws the respawn screen, restarting level 3."""
    global screen
    global WIDTH
    global HEIGHT

    global fibberish
    global fibberish_medium
    global fibberish_large

    global ticks

    background = pygame.transform.scale(pygame.image.load("../graphics/landscape3.jpg"), (1200, 704))
    screen.blit(background, (0, 0))
    gfxdraw.box(screen, pygame.Rect(0, 0, WIDTH, HEIGHT), (181, 16, 16, 170))

    correct_message = fibberish_large.render("Game Over.", True, (255, 255, 255))
    confirmation = fibberish_medium.render(f"Respawning in {ticks}", True, (255, 255, 255))
    prompt = fibberish.render("Press X to return to overworld.", True, (255, 255, 255))

    screen.blit(correct_message, (WIDTH // 2 - (correct_message.get_width() / 2), (HEIGHT // 2) - 50))
    screen.blit(confirmation, (WIDTH // 2 - (confirmation.get_width() / 2), HEIGHT // 2))
    screen.blit(prompt, (WIDTH // 2 - (prompt.get_width() / 2), (HEIGHT // 2) + 50))

# GAME LOOP
while running:
    draw()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                with open("overworld3.py") as f:
                    exec(f.read())
        elif event.type == COUNTDOWN:
            ticks -= 1
            if ticks == 0:
                with open("main3.py") as f:
                    exec(f.read())

pygame.quit()
sys.exit()