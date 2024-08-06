# NAMES: DINIM ONIGYE & EDAFE ETUKE
# LEVEL 1 RUNNING CODE + TIMER

# IMPORTS
import pygame, sys
from pygame import gfxdraw
from settings import *
from level import Level
from game_data import level_0

# SETUP
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
level1 = Level(level_0, screen)
COUNTDOWN = pygame.USEREVENT + 1
pygame.time.set_timer(COUNTDOWN, 1000)

# COLORS
MALACHITE = pygame.Color("#08c427")
CANDLIELIGHT = pygame.Color("#ffd500")
LAVA = pygame.Color("#cf0808")
color = MALACHITE

# VARIABLES
ticks = 60
fibberish_large = pygame.font.Font("../fonts/fibberish.ttf", 50)

# AUDIO
pygame.mixer.music.load("../audio/level1.wav")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

# GAME LOOP
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == COUNTDOWN:
            ticks -= 1
            if ticks <= 15 and ticks >= 11:
                color = MALACHITE
            elif ticks <= 10 and ticks >= 6:
                color = CANDLIELIGHT
            elif ticks <= 5:
                color = LAVA
                if ticks == 0:
                    level1.collected_words = {}
                    level1.speaker_on = False
                    with open("respawn.py") as f:
                        exec(f.read())

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                with open("SONUS.py") as f:
                    exec(f.read())

    background = pygame.transform.scale2x(pygame.image.load("../graphics/landscape.jpg"))
    screen.blit(background, (0, 0))
    gfxdraw.box(screen, pygame.Rect(0, 0, screen_width, screen_height), (0, 0, 0, 100))
    level1.run()
    border = pygame.Rect(820, 23, 60, 60)
    pygame.draw.rect(screen, color, border, width=4, border_radius=3)
    time_left = fibberish_large.render(str(ticks), True, "white")
    x = ((border.width / 2) - (time_left.get_width() / 2)) + 820
    y = ((border.height / 2) - (time_left.get_height() / 2)) + 27
    screen.blit(time_left, (x, y))

    pygame.display.update()
    clock.tick(60)