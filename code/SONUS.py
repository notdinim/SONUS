# NAMES: DINIM ONIGYE & EDAFE ETUKE
# SONUS TTS INFO, QUIZ AND PROLOGUE

# IMPORTS
import pygame
from pygame import gfxdraw
from os import listdir
from os.path import join, isfile

# from gtts import gTTS
"""We originally used the gTTS module, but since the system on your computer doesn't support it, we converted all the gTTS outputs to .wav and .ogg files instead."""

# SETUP
pygame.init()
WIDTH, HEIGHT = 1000, 800
FPS = 30
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SONUS PLATFORMER")
running = True

# COLORS
BALTIC_SEA = pygame.Color("#2b2b2b")
VIOLENT_VIOLET = pygame.Color("#290557")
STEEL = pygame.Color("#788a9c")
BLIZZARD_BLUE = pygame.Color("#89e8e3")
MALIBU = pygame.Color("#86cef0")
BLACK_ROCK = pygame.Color("#17093b")
SOFT_AMBER = pygame.Color("#cfc4ab")
PINK_LACE = pygame.Color("#fbd9ff")


# FONTS
fibberish = pygame.font.Font("../fonts/fibberish.ttf", 20)
fibberish_medium = pygame.font.Font("../fonts/fibberish.ttf", 30)
fibberish_large = pygame.font.Font("../fonts/fibberish.ttf", 40)

# VARIABLES
your_answer = ""
certificate = False
button_func = "play"
clicks = 0

# FUNCTIONS
# https://www.youtube.com/watch?v=6gLeplbqtqg
def load_sprite_icons(width, height):
    """This function loads a sprite sheet from the icon directory."""
    path = "../graphics/icons"
    images = [file for file in listdir(path) if isfile(join(path, file))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image))

        sprites = []

        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(surface)

        all_sprites[image.replace(".png", "")] = sprites


    return sprites

def load_sprite_sheets():
    """This is a general use function used for loading sprite sheets."""
    path = "../graphics/scene_animation"
    images = [file for file in listdir(path)]

    sprites = []

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image))
        sprites.append(sprite_sheet)

    return sprites

def load_sprite_keys(letter, width, height):
    """This function is used to load sprite sheet specifically from the SimpleKeys directory."""
    path = "../graphics/SimpleKeys/Jumbo/Light/Spritesheets/" + f"{letter.upper()}.png"
    sprite_sheet = pygame.image.load(path)

    sprite = []

    for i in range(sprite_sheet.get_width() // width):
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        rect = pygame.Rect(i * width, 0, width, height)
        surface.blit(sprite_sheet, (0, 0), rect)
        sprite.append(surface)

    return sprite

def load_sprite_keys2(letter, width, height):
    """This function is also used to load sprite sheets from the SimpleKeys directory, although larger in size."""
    path = "../graphics/SimpleKeys/Jumbo/Light/Spritesheets/" + f"{letter.upper()}.png"
    sprite_sheet = pygame.image.load(path)

    sprite = []

    for i in range(sprite_sheet.get_width() // width):
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        rect = pygame.Rect(i * width, 0, width, height)
        surface.blit(sprite_sheet, (0, 0), rect)
        sprite.append(pygame.transform.scale(surface, (38, 42)))

    return sprite

def load_progress_bar(width, height):
    """This function is used to load sprite sheets of the progress bar seen at the top of the game."""
    sprite_sheet = pygame.image.load("../graphics/progress_bar.png")

    sprites = []

    for i in range(sprite_sheet.get_width() // width):
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        rect = pygame.Rect(i * width, 0, width, height)
        surface.blit(sprite_sheet, (0, 0), rect)
        sprites.insert(0, pygame.transform.scale2x(surface))

    return sprites

def draw(screen, progress_bar):
    """This function draws the progress bar."""
    screen.fill(BALTIC_SEA)
    start = 320
    y_pos = 360
    loading_coordinates = {
        (start, y_pos): loading[0],
        (start + 50, y_pos): loading[1],
        (start + 100, y_pos): loading[2],
        (start + 150, y_pos): loading[3],
        (start + 200, y_pos): loading[4],
        (start + 250, y_pos): loading[5],
        (start + 300, y_pos): loading[6]
    }
    for key, item in loading_coordinates.items():
        item.draw(key)
    progress_bar.draw((395, 430))


# CLASSES
class Key:
    """This class creates a key from a letter of choice."""
    ANIMATION_DELAY = 30

    def __init__(self, letter):
        """The magic keyword / dunder function __init__ initializes the class."""
        self.animation_count = 0
        self.sprites = load_sprite_keys(letter, 19, 21)

    def draw(self, placement):
        """This function draws a key on the desired screen at a specific place."""
        sprite_index = (self.animation_count // self.ANIMATION_DELAY % len(self.sprites))
        self.sprite = self.sprites[sprite_index]
        self.animation_count += 1
        screen.blit(self.sprite, placement)

class Key2:
    """This class also creates keys, although larger."""
    ANIMATION_DELAY = 100

    def __init__(self, letter):
        """The magic keyword / dunder function __init__ initializes the class."""
        self.animation_count = 0
        self.sprites = load_sprite_keys2(letter, 19, 21)
        self.sprite = self.sprites[0]

    def draw(self, placement):
        """This funcion draws the key on the screen at a specific place."""
        sprite_index = (self.animation_count // self.ANIMATION_DELAY % len(self.sprites))
        self.sprite = self.sprites[sprite_index]
        self.animation_count += 1
        screen.blit(self.sprite, placement)

class Subtitle:
    """This class creates subtitles for the loading screen."""

    def __init__(self):
        """The magic keyword / dunder function __init__ initializes the class."""
        self.my_font = pygame.font.Font("fonts/broken-console-broken-console-bold-700.ttf", 20)
        self.sentences = ["", "", "", "", "", "Game Complete"]
        self.index = 0
        if self.index < len(self.sentences):
            self.index = 0

    def draw(self, placement):
        """This function draws the words at a specific place on the screen."""
        text = self.my_font.render(self.sentences[self.index], True, (255, 255, 255))
        text.get_rect().center = placement
        screen.blit(text, placement)

class ProgressBar:
    """This class creates a multi-purpose progress bar object."""

    def __init__(self):
        """The magic keyword / dunder function __init__ initializes the class."""
        self.sprites = load_progress_bar(48, 14)
        self.index = 0
        if self.index > len(self.sprites):
            self.index = 0

    def draw(self, placement):
        """This function draws the progress bar at a specific spot on the screen."""
        self.sprite = pygame.transform.scale2x(self.sprites[self.index])
        screen.blit(self.sprite, placement)

class TTSProgressBar:
    """This class creates a progress bar object, specifically for use in the TTS slides."""

    def __init__(self):
        """The magic keyword / dunder function __init__ initializes the class."""
        self.sprites = load_progress_bar(48, 14)
        self.index = 0
        if self.index > len(self.sprites):
            self.index = 0

    def draw(self, placement):
        """This function draws the progress bar at a specific place on the screen."""
        self.sprite = self.sprites[self.index]
        screen.blit(self.sprite, placement)

class Splashscreen:
    """This class creates the splashscreen."""

    def __init__(self):
        """The magic keyword / dunder function __init__ initializes the class."""
        self.bg = pygame.transform.scale(pygame.image.load("../graphics/background.png"), (1000, 800))

    def create_shadow(self):
        """This function creates the things needed to make on overlay over the background image for increased visibility."""
        rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        return rect

    def box(self):
        """This function creates the things needed to make a translucent box for increased visibility."""
        rect = pygame.Rect(0, 500, WIDTH, HEIGHT / 4)
        return rect

    def title(self):
        """This function creates the things needed to draw the title."""
        title = pygame.image.load("../graphics/title.png")
        return title

    def draw(self):
        """This function draws the components of the splashscreen."""
        start = 775
        play_coordinates = {
            (start, 525): play[0],
            (start + 25, 525): play[1],
            (start + 50, 525): play[2],
            (start + 75, 525): play[3]
        }
        tts_coordinates = {
            (start, 560): tts[0],
            (start + 25, 560): tts[1],
            (start + 50, 560): tts[2]
        }

        screen.blit(self.bg, (0, 0))
        gfxdraw.box(screen, self.create_shadow(), (0, 0, 0, 0))
        gfxdraw.box(screen, self.box(), (50, 50, 50, 200))
        screen.blit(self.title(), (470, 535))
        for key, item in play_coordinates.items():
            item.draw(key)
        for key, item in tts_coordinates.items():
            item.draw(key)

class TTS1:
    """This class creates on object of the first TTS screen. All following TTS scene classes follow the same format and the same docstrings apply."""
    def __init__(self):
        """The magic keyword / dunder function __init__ initializes the class."""
        pass

    def header(self):
        """This function creates the rect object used to create the header."""
        rect = pygame.Rect(0, 0, WIDTH, HEIGHT // 11)
        return rect

    def subtitle(self):
        """This creates the subtitle."""
        tts_list = [Key("T"), Key("T"), Key("S")]
        start = 465
        tts_coordinates = {
            (470, 15): tts_list[0],
            (495, 15): tts_list[1],
            (520, 15): tts_list[2]
        }
        return tts_list, tts_coordinates

    def arrows(self):
        """This creates the back and forward buttons used for navigation."""
        back = Key2("Arrowleft")
        forward = Key2("Arrowright")
        return back, forward

    def dialogue(self):
        """This function returns the sound icon used to initiate TTS."""
        sprite_sheet = pygame.image.load("../graphics/icons/sound.png")
        surface = pygame.Surface((30, 31), pygame.SRCALPHA)
        rect = pygame.Rect(0, 0, 30, 31)
        surface.blit(sprite_sheet, (0, 0), rect)

        return pygame.transform.scale(surface, (150, 155)), pygame.Rect(100, 580, 800, 200)

    def draw(self):
        """This function draws the TTS scene."""
        screen.fill(VIOLENT_VIOLET)
        rect = self.header()
        tts_list, tts_coordinates = self.subtitle()
        back, forward = self.arrows()
        megaphone_img, box = self.dialogue()
        sentences = ["TTS translates to Text-to-Speech. It is a technology that allows", "synthesized human speech to be read aloud. It comes with many", "customizables features such as a voice settings, and reading speed. Some", "TTS softwares include OCR, optical chcracter recognition, which can turn", "text from images into audio."]
        tts_image = pygame.transform.scale(pygame.image.load("../graphics/tts.jpg"), (798, 444))
        gfxdraw.box(screen, rect, (0, 0, 0, 100))
        for key, item in tts_coordinates.items():
            item.draw(key)
        tts_progress_bar = TTSProgressBar()
        tts_progress_bar.index = 1
        tts_progress_bar.draw((456, 41))
        back.draw((406, 13))
        forward.draw((565, 13))
        gfxdraw.box(screen, box, (0, 0, 0, 100))
        screen.blit(megaphone_img, (120, 597))
        fibberish = pygame.font.Font("../fonts/fibberish.ttf", 20)
        text = fibberish.render(sentences[0], True, (255, 255, 255))
        text2 = fibberish.render(sentences[1], True, (255, 255, 255))
        text3 = fibberish.render(sentences[2], True, (255, 255, 255))
        text4 = fibberish.render(sentences[3], True, (255, 255, 255))
        text5 = fibberish.render(sentences[4], True, (255, 255, 255))
        screen.blit(text, (285, 620))
        screen.blit(text2, (285, 650))
        screen.blit(text3, (285, 680))
        screen.blit(text4, (285, 710))
        screen.blit(text5, (285, 740))
        screen.blit(tts_image, (101, 120))

class TTS2:
    def __init__(self):
        pass

    def header(self):
        rect = pygame.Rect(0, 0, WIDTH, HEIGHT // 11)
        return rect

    def subtitle(self):
        tts_list = [Key("T"), Key("T"), Key("S")]
        start = 465
        tts_coordinates = {
            (470, 15): tts_list[0],
            (495, 15): tts_list[1],
            (520, 15): tts_list[2]
        }
        return tts_list, tts_coordinates

    def arrows(self):
        back = Key2("Arrowleft")
        forward = Key2("Arrowright")
        return back, forward

    def dialogue(self):
        sprite_sheet = pygame.image.load("../graphics/icons/sound.png")
        surface = pygame.Surface((30, 31), pygame.SRCALPHA)
        rect = pygame.Rect(0, 0, 30, 31)
        surface.blit(sprite_sheet, (0, 0), rect)

        return pygame.transform.scale(surface, (150, 155)), pygame.Rect(100, 580, 800, 200)

    def draw(self):
        screen.fill(STEEL)
        rect = self.header()
        tts_list, tts_coordinates = self.subtitle()
        back, forward = self.arrows()
        megaphone_img, box = self.dialogue()
        sentences = ["TTS systems have been in constant development since its birth in 1968.", "It was developed by Noriko Umeda and his team at the Electrotechnical", "Laboratory in Japan. This makes the tech about half a century old (55).", "TTS is evolving quickly with voice cloning and more language options", "available."]
        tts_image = pygame.transform.scale(pygame.image.load("../graphics/ljackson.png"), (798, 444))
        gfxdraw.box(screen, rect, (0, 0, 0, 100))
        for key, item in tts_coordinates.items():
            item.draw(key)
        tts_progress_bar = TTSProgressBar()
        tts_progress_bar.index = 2
        tts_progress_bar.draw((456, 41))
        back.draw((406, 13))
        forward.draw((565, 13))
        gfxdraw.box(screen, box, (0, 0, 0, 100))
        screen.blit(megaphone_img, (120, 597))
        fibberish = pygame.font.Font("../fonts/fibberish.ttf", 20)
        text = fibberish.render(sentences[0], True, (255, 255, 255))
        text2 = fibberish.render(sentences[1], True, (255, 255, 255))
        text3 = fibberish.render(sentences[2], True, (255, 255, 255))
        text4 = fibberish.render(sentences[3], True, (255, 255, 255))
        text5 = fibberish.render(sentences[4], True, (255, 255, 255))
        screen.blit(text, (285, 620))
        screen.blit(text2, (285, 650))
        screen.blit(text3, (285, 680))
        screen.blit(text4, (285, 710))
        screen.blit(text5, (285, 740))
        screen.blit(tts_image, (101, 120))

class TTS3:
    def __init__(self):
        pass

    def header(self):
        rect = pygame.Rect(0, 0, WIDTH, HEIGHT // 11)
        return rect

    def subtitle(self):
        tts_list = [Key("T"), Key("T"), Key("S")]
        start = 465
        tts_coordinates = {
            (470, 15): tts_list[0],
            (495, 15): tts_list[1],
            (520, 15): tts_list[2]
        }
        return tts_list, tts_coordinates

    def arrows(self):
        back = Key2("Arrowleft")
        forward = Key2("Arrowright")
        return back, forward

    def dialogue(self):
        sprite_sheet = pygame.image.load("../graphics/icons/sound.png")
        surface = pygame.Surface((30, 31), pygame.SRCALPHA)
        rect = pygame.Rect(0, 0, 30, 31)
        surface.blit(sprite_sheet, (0, 0), rect)

        return pygame.transform.scale(surface, (150, 155)), pygame.Rect(100, 580, 800, 200)

    def draw(self):
        screen.fill(BLIZZARD_BLUE)
        rect = self.header()
        tts_list, tts_coordinates = self.subtitle()
        back, forward = self.arrows()
        megaphone_img, box = self.dialogue()
        sentences = ["TTS is aimed at helping the physically challenged. Those with impaired", "vision can use TTS to read out text on screens and alternate text for", "images. It is also used to help people who have difficulty reading.", "TTS also allows people to reduce their screen time amounts.", "Go to the next slide for a quiz to test what you've learned!"]
        tts_image = pygame.transform.scale(pygame.image.load("../graphics/tts_users.jpg"), (798, 444))
        gfxdraw.box(screen, rect, (0, 0, 0, 100))
        for key, item in tts_coordinates.items():
            item.draw(key)
        tts_progress_bar = TTSProgressBar()
        tts_progress_bar.index = 3
        tts_progress_bar.draw((456, 41))
        back.draw((406, 13))
        forward.draw((565, 13))
        gfxdraw.box(screen, box, (0, 0, 0, 100))
        screen.blit(megaphone_img, (120, 597))
        fibberish = pygame.font.Font("../fonts/fibberish.ttf", 20)
        text = fibberish.render(sentences[0], True, (255, 255, 255))
        text2 = fibberish.render(sentences[1], True, (255, 255, 255))
        text3 = fibberish.render(sentences[2], True, (255, 255, 255))
        text4 = fibberish.render(sentences[3], True, (255, 255, 255))
        text5 = fibberish.render(sentences[4], True, (255, 255, 255))
        screen.blit(text, (285, 620))
        screen.blit(text2, (285, 650))
        screen.blit(text3, (285, 680))
        screen.blit(text4, (285, 710))
        screen.blit(text5, (285, 740))
        screen.blit(tts_image, (101, 120))

class TTSTest1:
    def __init__(self):
        pass

    def header(self):
        rect = pygame.Rect(0, 0, WIDTH, HEIGHT // 11)
        return rect

    def subtitle(self):
        tts_list = [Key("T"), Key("T"), Key("S")]
        start = 465
        tts_coordinates = {
            (470, 15): tts_list[0],
            (495, 15): tts_list[1],
            (520, 15): tts_list[2]
        }
        return tts_list, tts_coordinates

    def arrows(self):
        back = Key2("Arrowleft")
        forward = Key2("Arrowright")
        return back, forward

    def dialogue(self):
        sprite_sheet = pygame.image.load("../graphics/icons/sound.png")
        surface = pygame.Surface((30, 31), pygame.SRCALPHA)
        rect = pygame.Rect(0, 0, 30, 31)
        surface.blit(sprite_sheet, (0, 0), rect)

        return pygame.transform.scale(surface, (150, 155)), pygame.Rect(100, 580, 800, 200)

    def draw(self):
        screen.fill(MALIBU)
        rect = self.header()
        tts_list, tts_coordinates = self.subtitle()
        megaphone_img, box = self.dialogue()
        sentences = ["Quiz Time - Question 1", "What does TTS stand for?"]
        tts_image = pygame.transform.scale(pygame.image.load("../graphics/tts_icon.png"), (500, 444))
        gfxdraw.box(screen, rect, (0, 0, 0, 100))
        for key, item in tts_coordinates.items():
            item.draw(key)
        tts_progress_bar = TTSProgressBar()
        tts_progress_bar.index = 4
        tts_progress_bar.draw((456, 41))
        gfxdraw.box(screen, box, (0, 0, 0, 100))
        screen.blit(megaphone_img, (120, 597))
        text = fibberish.render(sentences[0], True, (255, 255, 255))
        text2 = fibberish_large.render(sentences[1], True, (255, 255, 255))
        screen.blit(text, (285, 620))
        screen.blit(text2, (285, 650))
        screen.blit(tts_image, (101, 120))

        answer1_rect = pygame.Rect(620, 120, 280, 80)
        gfxdraw.box(screen, answer1_rect, (0, 0, 0, 100))
        answer1 = fibberish_large.render("Text to Speech", True, (255, 255, 255))
        screen.blit(answer1, (635, 145))

        answer2_rect = pygame.Rect(620, 241, 280, 80)
        gfxdraw.box(screen, answer2_rect, (0, 0, 0, 100))
        answer2 = fibberish_large.render("Speech to Text", True, (255, 255, 255))
        screen.blit(answer2, (635, 270))

        answer3_rect = pygame.Rect(620, 362, 280, 80)
        gfxdraw.box(screen, answer3_rect, (0, 0, 0, 100))
        answer3 = fibberish_medium.render("Touch Type Software", True, (255, 255, 255))
        screen.blit(answer3, (635, 390))

        answer4_rect = pygame.Rect(620, 483, 280, 80)
        gfxdraw.box(screen, answer4_rect, (0, 0, 0, 100))
        answer4 = fibberish_medium.render("Type Text System", True, (255, 255, 255))
        screen.blit(answer4, (635, 510))

class Correct:
    """This class displays the correct scene. All following correct and incorrect scenes follow the same format and the same docstrings apply."""

    def __init__(self):
        """The magic keyword / dunder function __init__ initializes the class."""
        pass

    def header(self):
        """This creates the Rect object used for the header."""
        rect = pygame.Rect(0, 0, WIDTH, HEIGHT // 11)
        return rect

    def subtitle(self):
        """This creates the subtitle."""
        tts_list = [Key("T"), Key("T"), Key("S")]
        start = 465
        tts_coordinates = {
            (470, 15): tts_list[0],
            (495, 15): tts_list[1],
            (520, 15): tts_list[2]
        }
        return tts_list, tts_coordinates

    def arrows(self):
        """This creates the back and forward arrows used for navigation."""
        back = Key2("Arrowleft")
        forward = Key2("Arrowright")
        return back, forward

    def dialogue(self):
        """This creates the sound icon image used to initiate TTS."""
        sprite_sheet = pygame.image.load("../graphics/icons/sound.png")
        surface = pygame.Surface((30, 31), pygame.SRCALPHA)
        rect = pygame.Rect(0, 0, 30, 31)
        surface.blit(sprite_sheet, (0, 0), rect)

        return pygame.transform.scale(surface, (150, 155)), pygame.Rect(100, 580, 800, 200)

    def draw(self):
        """This draws the scene."""
        screen.fill(BLIZZARD_BLUE)
        rect = self.header()
        tts_list, tts_coordinates = self.subtitle()
        megaphone_img, box = self.dialogue()
        sentences = ["Quiz Time - Question 1", "What does TTS stand for?"]
        tts_image = pygame.transform.scale(pygame.image.load("../graphics/tts_icon.png"), (500, 444))
        gfxdraw.box(screen, rect, (0, 0, 0, 100))
        for key, item in tts_coordinates.items():
            item.draw(key)
        tts_progress_bar = TTSProgressBar()
        tts_progress_bar.index = 4
        tts_progress_bar.draw((456, 41))
        gfxdraw.box(screen, box, (0, 0, 0, 100))
        screen.blit(megaphone_img, (120, 597))
        fibberish = pygame.font.Font("../fonts/fibberish.ttf", 20)
        fibberish_medium = pygame.font.Font("../fonts/fibberish.ttf", 30)
        fibberish_large = pygame.font.Font("../fonts/fibberish.ttf", 40)
        text = fibberish.render(sentences[0], True, (255, 255, 255))
        text2 = fibberish_large.render(sentences[1], True, (255, 255, 255))
        screen.blit(text, (285, 620))
        screen.blit(text2, (285, 650))
        screen.blit(tts_image, (101, 120))

        answer1_rect = pygame.Rect(620, 120, 280, 80)
        gfxdraw.box(screen, answer1_rect, (0, 0, 0, 100))
        answer1 = fibberish_large.render("Text to Speech", True, (255, 255, 255))
        screen.blit(answer1, (635, 145))

        answer2_rect = pygame.Rect(620, 241, 280, 80)
        gfxdraw.box(screen, answer2_rect, (0, 0, 0, 100))
        answer2 = fibberish_large.render("Speech to Text", True, (255, 255, 255))
        screen.blit(answer2, (635, 270))

        answer3_rect = pygame.Rect(620, 362, 280, 80)
        gfxdraw.box(screen, answer3_rect, (0, 0, 0, 100))
        answer3 = fibberish_medium.render("Touch Type Software", True, (255, 255, 255))
        screen.blit(answer3, (635, 390))

        answer4_rect = pygame.Rect(620, 483, 280, 80)
        gfxdraw.box(screen, answer4_rect, (0, 0, 0, 100))
        answer4 = fibberish_medium.render("Type Text System", True, (255, 255, 255))
        screen.blit(answer4, (635, 510))

        gfxdraw.box(screen, pygame.Rect(0, 0, WIDTH, HEIGHT), (22, 186, 55, 150))

        correct_message = fibberish_large.render("Correct!", True, (255, 255, 255))
        confirmation = fibberish_medium.render(f"{your_answer} is correct!", True, (255, 255, 255))
        prompt = fibberish.render("Press Space to continue.", True, (255, 255, 255))

        screen.blit(correct_message, (WIDTH // 2 - (correct_message.get_width() / 2), (HEIGHT // 2) - 50))
        screen.blit(confirmation, (WIDTH // 2 - (confirmation.get_width() / 2), HEIGHT // 2))
        screen.blit(prompt, (WIDTH // 2 - (prompt.get_width() / 2), (HEIGHT // 2) + 50))

class Incorrect:
    def __init__(self):
        pass

    def header(self):
        rect = pygame.Rect(0, 0, WIDTH, HEIGHT // 11)
        return rect

    def subtitle(self):
        tts_list = [Key("T"), Key("T"), Key("S")]
        start = 465
        tts_coordinates = {
            (470, 15): tts_list[0],
            (495, 15): tts_list[1],
            (520, 15): tts_list[2]
        }
        return tts_list, tts_coordinates

    def arrows(self):
        back = Key2("Arrowleft")
        forward = Key2("Arrowright")
        return back, forward

    def dialogue(self):
        sprite_sheet = pygame.image.load("../graphics/icons/sound.png")
        surface = pygame.Surface((30, 31), pygame.SRCALPHA)
        rect = pygame.Rect(0, 0, 30, 31)
        surface.blit(sprite_sheet, (0, 0), rect)

        return pygame.transform.scale(surface, (150, 155)), pygame.Rect(100, 580, 800, 200)

    def draw(self):
        screen.fill(BLIZZARD_BLUE)
        rect = self.header()
        tts_list, tts_coordinates = self.subtitle()
        megaphone_img, box = self.dialogue()
        sentences = ["Quiz Time - Question 1", "What does TTS stand for?"]
        tts_image = pygame.transform.scale(pygame.image.load("../graphics/tts_icon.png"), (500, 444))
        gfxdraw.box(screen, rect, (0, 0, 0, 100))
        for key, item in tts_coordinates.items():
            item.draw(key)
        tts_progress_bar = TTSProgressBar()
        tts_progress_bar.index = 4
        tts_progress_bar.draw((456, 41))
        gfxdraw.box(screen, box, (0, 0, 0, 100))
        screen.blit(megaphone_img, (120, 597))
        fibberish = pygame.font.Font("../fonts/fibberish.ttf", 20)
        fibberish_medium = pygame.font.Font("../fonts/fibberish.ttf", 30)
        fibberish_large = pygame.font.Font("../fonts/fibberish.ttf", 40)
        text = fibberish.render(sentences[0], True, (255, 255, 255))
        text2 = fibberish_large.render(sentences[1], True, (255, 255, 255))
        screen.blit(text, (285, 620))
        screen.blit(text2, (285, 650))
        screen.blit(tts_image, (101, 120))

        answer1_rect = pygame.Rect(620, 120, 280, 80)
        gfxdraw.box(screen, answer1_rect, (0, 0, 0, 100))
        answer1 = fibberish_large.render("Text to Speech", True, (255, 255, 255))
        screen.blit(answer1, (635, 145))

        answer2_rect = pygame.Rect(620, 241, 280, 80)
        gfxdraw.box(screen, answer2_rect, (0, 0, 0, 100))
        answer2 = fibberish_large.render("Speech to Text", True, (255, 255, 255))
        screen.blit(answer2, (635, 270))

        answer3_rect = pygame.Rect(620, 362, 280, 80)
        gfxdraw.box(screen, answer3_rect, (0, 0, 0, 100))
        answer3 = fibberish_medium.render("Touch Type Software", True, (255, 255, 255))
        screen.blit(answer3, (635, 390))

        answer4_rect = pygame.Rect(620, 483, 280, 80)
        gfxdraw.box(screen, answer4_rect, (0, 0, 0, 100))
        answer4 = fibberish_medium.render("Type Text System", True, (255, 255, 255))
        screen.blit(answer4, (635, 510))

        gfxdraw.box(screen, pygame.Rect(0, 0, WIDTH, HEIGHT), (191, 15, 15, 150))

        correct_message = fibberish_large.render("Incorrect!", True, (255, 255, 255))
        confirmation = fibberish_medium.render(f"{your_answer} is not correct.", True, (255, 255, 255))
        prompt = fibberish.render("Press esc to try again.", True, (255, 255, 255))

        screen.blit(correct_message, (WIDTH // 2 - (correct_message.get_width() / 2), (HEIGHT // 2) - 50))
        screen.blit(confirmation, (WIDTH // 2 - (confirmation.get_width() / 2), HEIGHT // 2))
        screen.blit(prompt, (WIDTH // 2 - (prompt.get_width() / 2), (HEIGHT // 2) + 50))

class TTSTest2:
    def __init__(self):
        pass

    def header(self):
        rect = pygame.Rect(0, 0, WIDTH, HEIGHT // 11)
        return rect

    def subtitle(self):
        tts_list = [Key("T"), Key("T"), Key("S")]
        start = 465
        tts_coordinates = {
            (470, 15): tts_list[0],
            (495, 15): tts_list[1],
            (520, 15): tts_list[2]
        }
        return tts_list, tts_coordinates

    def arrows(self):
        back = Key2("Arrowleft")
        forward = Key2("Arrowright")
        return back, forward

    def dialogue(self):
        sprite_sheet = pygame.image.load("../graphics/icons/sound.png")
        surface = pygame.Surface((30, 31), pygame.SRCALPHA)
        rect = pygame.Rect(0, 0, 30, 31)
        surface.blit(sprite_sheet, (0, 0), rect)

        return pygame.transform.scale(surface, (150, 155)), pygame.Rect(100, 580, 800, 200)

    def draw(self):
        screen.fill(BLACK_ROCK)
        rect = self.header()
        tts_list, tts_coordinates = self.subtitle()
        megaphone_img, box = self.dialogue()
        sentences = ["Quiz Time - Question 2", "Where was TTS created?"]
        tts_image = pygame.transform.scale(pygame.image.load("../graphics/where.jpg"), (500, 444))
        gfxdraw.box(screen, rect, (0, 0, 0, 100))
        for key, item in tts_coordinates.items():
            item.draw(key)
        tts_progress_bar = TTSProgressBar()
        tts_progress_bar.index = 4
        tts_progress_bar.draw((456, 41))
        gfxdraw.box(screen, box, (0, 0, 0, 100))
        screen.blit(megaphone_img, (120, 597))
        fibberish = pygame.font.Font("../fonts/fibberish.ttf", 20)
        fibberish_medium = pygame.font.Font("../fonts/fibberish.ttf", 30)
        fibberish_large = pygame.font.Font("../fonts/fibberish.ttf", 40)
        text = fibberish.render(sentences[0], True, (255, 255, 255))
        text2 = fibberish_large.render(sentences[1], True, (255, 255, 255))
        screen.blit(text, (285, 620))
        screen.blit(text2, (285, 650))
        screen.blit(tts_image, (101, 120))

        answer1_rect = pygame.Rect(620, 120, 280, 80)
        gfxdraw.box(screen, answer1_rect, (0, 0, 0, 100))
        answer1 = fibberish_large.render("Canada", True, (255, 255, 255))
        screen.blit(answer1, (705, 145))

        answer2_rect = pygame.Rect(620, 241, 280, 80)
        gfxdraw.box(screen, answer2_rect, (0, 0, 0, 100))
        answer2 = fibberish_large.render("China", True, (255, 255, 255))
        screen.blit(answer2, (725, 270))

        answer3_rect = pygame.Rect(620, 362, 280, 80)
        gfxdraw.box(screen, answer3_rect, (0, 0, 0, 100))
        answer3 = fibberish_large.render("Japan", True, (255, 255, 255))
        screen.blit(answer3, (720, 390))

        answer4_rect = pygame.Rect(620, 483, 280, 80)
        gfxdraw.box(screen, answer4_rect, (0, 0, 0, 100))
        answer4 = fibberish_large.render("Netherlands", True, (255, 255, 255))
        screen.blit(answer4, (680, 510))

class Correct2:
    def __init__(self):
        pass

    def header(self):
        rect = pygame.Rect(0, 0, WIDTH, HEIGHT // 11)
        return rect

    def subtitle(self):
        tts_list = [Key("T"), Key("T"), Key("S")]
        start = 465
        tts_coordinates = {
            (470, 15): tts_list[0],
            (495, 15): tts_list[1],
            (520, 15): tts_list[2]
        }
        return tts_list, tts_coordinates

    def arrows(self):
        back = Key2("Arrowleft")
        forward = Key2("Arrowright")
        return back, forward

    def dialogue(self):
        sprite_sheet = pygame.image.load("../graphics/icons/sound.png")
        surface = pygame.Surface((30, 31), pygame.SRCALPHA)
        rect = pygame.Rect(0, 0, 30, 31)
        surface.blit(sprite_sheet, (0, 0), rect)

        return pygame.transform.scale(surface, (150, 155)), pygame.Rect(100, 580, 800, 200)

    def draw(self):
        screen.fill(BLACK_ROCK)
        rect = self.header()
        tts_list, tts_coordinates = self.subtitle()
        megaphone_img, box = self.dialogue()
        sentences = ["Quiz Time - Question 2", "Where was TTS created?"]
        tts_image = pygame.transform.scale(pygame.image.load("../graphics/where.jpg"), (500, 444))
        gfxdraw.box(screen, rect, (0, 0, 0, 100))
        for key, item in tts_coordinates.items():
            item.draw(key)
        tts_progress_bar = TTSProgressBar()
        tts_progress_bar.index = 4
        tts_progress_bar.draw((456, 41))
        gfxdraw.box(screen, box, (0, 0, 0, 100))
        screen.blit(megaphone_img, (120, 597))
        fibberish = pygame.font.Font("../fonts/fibberish.ttf", 20)
        fibberish_medium = pygame.font.Font("../fonts/fibberish.ttf", 30)
        fibberish_large = pygame.font.Font("../fonts/fibberish.ttf", 40)
        text = fibberish.render(sentences[0], True, (255, 255, 255))
        text2 = fibberish_large.render(sentences[1], True, (255, 255, 255))
        screen.blit(text, (285, 620))
        screen.blit(text2, (285, 650))
        screen.blit(tts_image, (101, 120))

        answer1_rect = pygame.Rect(620, 120, 280, 80)
        gfxdraw.box(screen, answer1_rect, (0, 0, 0, 100))
        answer1 = fibberish_large.render("Canada", True, (255, 255, 255))
        screen.blit(answer1, (705, 145))

        answer2_rect = pygame.Rect(620, 241, 280, 80)
        gfxdraw.box(screen, answer2_rect, (0, 0, 0, 100))
        answer2 = fibberish_large.render("China", True, (255, 255, 255))
        screen.blit(answer2, (725, 270))

        answer3_rect = pygame.Rect(620, 362, 280, 80)
        gfxdraw.box(screen, answer3_rect, (0, 0, 0, 100))
        answer3 = fibberish_large.render("Japan", True, (255, 255, 255))
        screen.blit(answer3, (720, 390))

        answer4_rect = pygame.Rect(620, 483, 280, 80)
        gfxdraw.box(screen, answer4_rect, (0, 0, 0, 100))
        answer4 = fibberish_large.render("Netherlands", True, (255, 255, 255))
        screen.blit(answer4, (680, 510))
        gfxdraw.box(screen, pygame.Rect(0, 0, WIDTH, HEIGHT), (22, 186, 55, 150))

        correct_message = fibberish_large.render("Correct!", True, (255, 255, 255))
        confirmation = fibberish_medium.render(f"{your_answer} is correct!", True, (255, 255, 255))
        prompt = fibberish.render("Press Space to continue.", True, (255, 255, 255))

        screen.blit(correct_message, (WIDTH // 2 - (correct_message.get_width() / 2), (HEIGHT // 2) - 50))
        screen.blit(confirmation, (WIDTH // 2 - (confirmation.get_width() / 2), HEIGHT // 2))
        screen.blit(prompt, (WIDTH // 2 - (prompt.get_width() / 2), (HEIGHT // 2) + 50))

class Incorrect2:
    def __init__(self):
        pass

    def header(self):
        rect = pygame.Rect(0, 0, WIDTH, HEIGHT // 11)
        return rect

    def subtitle(self):
        tts_list = [Key("T"), Key("T"), Key("S")]
        start = 465
        tts_coordinates = {
            (470, 15): tts_list[0],
            (495, 15): tts_list[1],
            (520, 15): tts_list[2]
        }
        return tts_list, tts_coordinates

    def arrows(self):
        back = Key2("Arrowleft")
        forward = Key2("Arrowright")
        return back, forward

    def dialogue(self):
        sprite_sheet = pygame.image.load("../graphics/icons/sound.png")
        surface = pygame.Surface((30, 31), pygame.SRCALPHA)
        rect = pygame.Rect(0, 0, 30, 31)
        surface.blit(sprite_sheet, (0, 0), rect)

        return pygame.transform.scale(surface, (150, 155)), pygame.Rect(100, 580, 800, 200)

    def draw(self):
        screen.fill(BLACK_ROCK)
        rect = self.header()
        tts_list, tts_coordinates = self.subtitle()
        megaphone_img, box = self.dialogue()
        sentences = ["Quiz Time - Question 2", "Where was TTS created?"]
        tts_image = pygame.transform.scale(pygame.image.load("../graphics/where.jpg"), (500, 444))
        gfxdraw.box(screen, rect, (0, 0, 0, 100))
        for key, item in tts_coordinates.items():
            item.draw(key)
        tts_progress_bar = TTSProgressBar()
        tts_progress_bar.index = 4
        tts_progress_bar.draw((456, 41))
        gfxdraw.box(screen, box, (0, 0, 0, 100))
        screen.blit(megaphone_img, (120, 597))
        fibberish = pygame.font.Font("../fonts/fibberish.ttf", 20)
        fibberish_medium = pygame.font.Font("../fonts/fibberish.ttf", 30)
        fibberish_large = pygame.font.Font("../fonts/fibberish.ttf", 40)
        text = fibberish.render(sentences[0], True, (255, 255, 255))
        text2 = fibberish_large.render(sentences[1], True, (255, 255, 255))
        screen.blit(text, (285, 620))
        screen.blit(text2, (285, 650))
        screen.blit(tts_image, (101, 120))

        answer1_rect = pygame.Rect(620, 120, 280, 80)
        gfxdraw.box(screen, answer1_rect, (0, 0, 0, 100))
        answer1 = fibberish_large.render("Canada", True, (255, 255, 255))
        screen.blit(answer1, (705, 145))

        answer2_rect = pygame.Rect(620, 241, 280, 80)
        gfxdraw.box(screen, answer2_rect, (0, 0, 0, 100))
        answer2 = fibberish_large.render("China", True, (255, 255, 255))
        screen.blit(answer2, (725, 270))

        answer3_rect = pygame.Rect(620, 362, 280, 80)
        gfxdraw.box(screen, answer3_rect, (0, 0, 0, 100))
        answer3 = fibberish_large.render("Japan", True, (255, 255, 255))
        screen.blit(answer3, (720, 390))

        answer4_rect = pygame.Rect(620, 483, 280, 80)
        gfxdraw.box(screen, answer4_rect, (0, 0, 0, 100))
        answer4 = fibberish_large.render("Netherlands", True, (255, 255, 255))
        screen.blit(answer4, (680, 510))

        gfxdraw.box(screen, pygame.Rect(0, 0, WIDTH, HEIGHT), (191, 15, 15, 150))

        correct_message = fibberish_large.render("Incorrect!", True, (255, 255, 255))
        confirmation = fibberish_medium.render(f"{your_answer} is not correct.", True, (255, 255, 255))
        prompt = fibberish.render("Press esc to try again.", True, (255, 255, 255))

        screen.blit(correct_message, (WIDTH // 2 - (correct_message.get_width() / 2), (HEIGHT // 2) - 50))
        screen.blit(confirmation, (WIDTH // 2 - (confirmation.get_width() / 2), HEIGHT // 2))
        screen.blit(prompt, (WIDTH // 2 - (prompt.get_width() / 2), (HEIGHT // 2) + 50))

class TTSTest3:
    def __init__(self):
        pass

    def header(self):
        rect = pygame.Rect(0, 0, WIDTH, HEIGHT // 11)
        return rect

    def subtitle(self):
        tts_list = [Key("T"), Key("T"), Key("S")]
        start = 465
        tts_coordinates = {
            (470, 15): tts_list[0],
            (495, 15): tts_list[1],
            (520, 15): tts_list[2]
        }
        return tts_list, tts_coordinates

    def arrows(self):
        back = Key2("Arrowleft")
        forward = Key2("Arrowright")
        return back, forward

    def dialogue(self):
        sprite_sheet = pygame.image.load("../graphics/icons/sound.png")
        surface = pygame.Surface((30, 31), pygame.SRCALPHA)
        rect = pygame.Rect(0, 0, 30, 31)
        surface.blit(sprite_sheet, (0, 0), rect)

        return pygame.transform.scale(surface, (150, 155)), pygame.Rect(100, 580, 800, 200)

    def draw(self):
        screen.fill(SOFT_AMBER)
        rect = self.header()
        tts_list, tts_coordinates = self.subtitle()
        megaphone_img, box = self.dialogue()
        sentences = ["Quiz Time - Question 3", "How old is TTS Technology?"]
        tts_image = pygame.transform.scale(pygame.image.load("../graphics/clock.jpg"), (500, 444))
        gfxdraw.box(screen, rect, (0, 0, 0, 100))
        for key, item in tts_coordinates.items():
            item.draw(key)
        tts_progress_bar = TTSProgressBar()
        tts_progress_bar.index = 4
        tts_progress_bar.draw((456, 41))
        gfxdraw.box(screen, box, (0, 0, 0, 100))
        screen.blit(megaphone_img, (120, 597))
        fibberish = pygame.font.Font("../fonts/fibberish.ttf", 20)
        fibberish_medium = pygame.font.Font("../fonts/fibberish.ttf", 30)
        fibberish_large = pygame.font.Font("../fonts/fibberish.ttf", 40)
        text = fibberish.render(sentences[0], True, (255, 255, 255))
        text2 = fibberish_large.render(sentences[1], True, (255, 255, 255))
        screen.blit(text, (285, 620))
        screen.blit(text2, (285, 650))
        screen.blit(tts_image, (101, 120))

        answer1_rect = pygame.Rect(620, 120, 280, 80)
        gfxdraw.box(screen, answer1_rect, (0, 0, 0, 100))
        answer1 = fibberish_large.render("100 years", True, (255, 255, 255))
        screen.blit(answer1, (690, 145))

        answer2_rect = pygame.Rect(620, 241, 280, 80)
        gfxdraw.box(screen, answer2_rect, (0, 0, 0, 100))
        answer2 = fibberish_large.render("A decade", True, (255, 255, 255))
        screen.blit(answer2, (690, 270))

        answer3_rect = pygame.Rect(620, 362, 280, 80)
        gfxdraw.box(screen, answer3_rect, (0, 0, 0, 100))
        answer3 = fibberish_large.render("27 years", True, (255, 255, 255))
        screen.blit(answer3, (690, 390))

        answer4_rect = pygame.Rect(620, 483, 280, 80)
        gfxdraw.box(screen, answer4_rect, (0, 0, 0, 100))
        answer4 = fibberish_large.render("55 years", True, (255, 255, 255))
        screen.blit(answer4, (690, 510))

class Correct3:
    def __init__(self):
        pass

    def header(self):
        rect = pygame.Rect(0, 0, WIDTH, HEIGHT // 11)
        return rect

    def subtitle(self):
        tts_list = [Key("T"), Key("T"), Key("S")]
        start = 465
        tts_coordinates = {
            (470, 15): tts_list[0],
            (495, 15): tts_list[1],
            (520, 15): tts_list[2]
        }
        return tts_list, tts_coordinates

    def arrows(self):
        back = Key2("Arrowleft")
        forward = Key2("Arrowright")
        return back, forward

    def dialogue(self):
        sprite_sheet = pygame.image.load("../graphics/icons/sound.png")
        surface = pygame.Surface((30, 31), pygame.SRCALPHA)
        rect = pygame.Rect(0, 0, 30, 31)
        surface.blit(sprite_sheet, (0, 0), rect)

        return pygame.transform.scale(surface, (150, 155)), pygame.Rect(100, 580, 800, 200)

    def draw(self):
        screen.fill(SOFT_AMBER)
        rect = self.header()
        tts_list, tts_coordinates = self.subtitle()
        megaphone_img, box = self.dialogue()
        sentences = ["Quiz Time - Question 3", "How old is TTS Technology?"]
        tts_image = pygame.transform.scale(pygame.image.load("../graphics/clock.jpg"), (500, 444))
        gfxdraw.box(screen, rect, (0, 0, 0, 100))
        for key, item in tts_coordinates.items():
            item.draw(key)
        tts_progress_bar = TTSProgressBar()
        tts_progress_bar.index = 4
        tts_progress_bar.draw((456, 41))
        gfxdraw.box(screen, box, (0, 0, 0, 100))
        screen.blit(megaphone_img, (120, 597))
        fibberish = pygame.font.Font("../fonts/fibberish.ttf", 20)
        fibberish_medium = pygame.font.Font("../fonts/fibberish.ttf", 30)
        fibberish_large = pygame.font.Font("../fonts/fibberish.ttf", 40)
        text = fibberish.render(sentences[0], True, (255, 255, 255))
        text2 = fibberish_large.render(sentences[1], True, (255, 255, 255))
        screen.blit(text, (285, 620))
        screen.blit(text2, (285, 650))
        screen.blit(tts_image, (101, 120))

        answer1_rect = pygame.Rect(620, 120, 280, 80)
        gfxdraw.box(screen, answer1_rect, (0, 0, 0, 100))
        answer1 = fibberish_large.render("100 years", True, (255, 255, 255))
        screen.blit(answer1, (690, 145))

        answer2_rect = pygame.Rect(620, 241, 280, 80)
        gfxdraw.box(screen, answer2_rect, (0, 0, 0, 100))
        answer2 = fibberish_large.render("A decade", True, (255, 255, 255))
        screen.blit(answer2, (690, 270))

        answer3_rect = pygame.Rect(620, 362, 280, 80)
        gfxdraw.box(screen, answer3_rect, (0, 0, 0, 100))
        answer3 = fibberish_large.render("27 years", True, (255, 255, 255))
        screen.blit(answer3, (690, 390))

        answer4_rect = pygame.Rect(620, 483, 280, 80)
        gfxdraw.box(screen, answer4_rect, (0, 0, 0, 100))
        answer4 = fibberish_large.render("55 years", True, (255, 255, 255))
        screen.blit(answer4, (690, 510))
        gfxdraw.box(screen, pygame.Rect(0, 0, WIDTH, HEIGHT), (22, 186, 55, 150))

        correct_message = fibberish_large.render("Correct!", True, (255, 255, 255))
        confirmation = fibberish_medium.render(f"{your_answer} is correct!", True, (255, 255, 255))
        prompt = fibberish.render("Press Space to continue.", True, (255, 255, 255))

        screen.blit(correct_message, (WIDTH // 2 - (correct_message.get_width() / 2), (HEIGHT // 2) - 50))
        screen.blit(confirmation, (WIDTH // 2 - (confirmation.get_width() / 2), HEIGHT // 2))
        screen.blit(prompt, (WIDTH // 2 - (prompt.get_width() / 2), (HEIGHT // 2) + 50))

class Incorrect3:
    def __init__(self):
        pass

    def header(self):
        rect = pygame.Rect(0, 0, WIDTH, HEIGHT // 11)
        return rect

    def subtitle(self):
        tts_list = [Key("T"), Key("T"), Key("S")]
        start = 465
        tts_coordinates = {
            (470, 15): tts_list[0],
            (495, 15): tts_list[1],
            (520, 15): tts_list[2]
        }
        return tts_list, tts_coordinates

    def arrows(self):
        back = Key2("Arrowleft")
        forward = Key2("Arrowright")
        return back, forward

    def dialogue(self):
        sprite_sheet = pygame.image.load("../graphics/icons/sound.png")
        surface = pygame.Surface((30, 31), pygame.SRCALPHA)
        rect = pygame.Rect(0, 0, 30, 31)
        surface.blit(sprite_sheet, (0, 0), rect)

        return pygame.transform.scale(surface, (150, 155)), pygame.Rect(100, 580, 800, 200)

    def draw(self):
        screen.fill(SOFT_AMBER)
        rect = self.header()
        tts_list, tts_coordinates = self.subtitle()
        megaphone_img, box = self.dialogue()
        sentences = ["Quiz Time - Question 3", "How old is TTS Technology?"]
        tts_image = pygame.transform.scale(pygame.image.load("../graphics/clock.jpg"), (500, 444))
        gfxdraw.box(screen, rect, (0, 0, 0, 100))
        for key, item in tts_coordinates.items():
            item.draw(key)
        tts_progress_bar = TTSProgressBar()
        tts_progress_bar.index = 4
        tts_progress_bar.draw((456, 41))
        gfxdraw.box(screen, box, (0, 0, 0, 100))
        screen.blit(megaphone_img, (120, 597))
        fibberish = pygame.font.Font("../fonts/fibberish.ttf", 20)
        fibberish_medium = pygame.font.Font("../fonts/fibberish.ttf", 30)
        fibberish_large = pygame.font.Font("../fonts/fibberish.ttf", 40)
        text = fibberish.render(sentences[0], True, (255, 255, 255))
        text2 = fibberish_large.render(sentences[1], True, (255, 255, 255))
        screen.blit(text, (285, 620))
        screen.blit(text2, (285, 650))
        screen.blit(tts_image, (101, 120))

        answer1_rect = pygame.Rect(620, 120, 280, 80)
        gfxdraw.box(screen, answer1_rect, (0, 0, 0, 100))
        answer1 = fibberish_large.render("100 years", True, (255, 255, 255))
        screen.blit(answer1, (690, 145))

        answer2_rect = pygame.Rect(620, 241, 280, 80)
        gfxdraw.box(screen, answer2_rect, (0, 0, 0, 100))
        answer2 = fibberish_large.render("A decade", True, (255, 255, 255))
        screen.blit(answer2, (690, 270))

        answer3_rect = pygame.Rect(620, 362, 280, 80)
        gfxdraw.box(screen, answer3_rect, (0, 0, 0, 100))
        answer3 = fibberish_large.render("27 years", True, (255, 255, 255))
        screen.blit(answer3, (690, 390))

        answer4_rect = pygame.Rect(620, 483, 280, 80)
        gfxdraw.box(screen, answer4_rect, (0, 0, 0, 100))
        answer4 = fibberish_large.render("55 years", True, (255, 255, 255))
        screen.blit(answer4, (690, 510))

        gfxdraw.box(screen, pygame.Rect(0, 0, WIDTH, HEIGHT), (191, 15, 15, 150))

        correct_message = fibberish_large.render("Incorrect!", True, (255, 255, 255))
        confirmation = fibberish_medium.render(f"{your_answer} is not correct.", True, (255, 255, 255))
        prompt = fibberish.render("Press esc to try again.", True, (255, 255, 255))

        screen.blit(correct_message, (WIDTH // 2 - (correct_message.get_width() / 2), (HEIGHT // 2) - 50))
        screen.blit(confirmation, (WIDTH // 2 - (confirmation.get_width() / 2), HEIGHT // 2))
        screen.blit(prompt, (WIDTH // 2 - (prompt.get_width() / 2), (HEIGHT // 2) + 50))

class TTS4:
    def __init__(self):
        pass

    def header(self):
        rect = pygame.Rect(0, 0, WIDTH, HEIGHT // 11)
        return rect

    def subtitle(self):
        tts_list = [Key("T"), Key("T"), Key("S")]
        start = 465
        tts_coordinates = {
            (470, 15): tts_list[0],
            (495, 15): tts_list[1],
            (520, 15): tts_list[2]
        }
        return tts_list, tts_coordinates

    def arrows(self):
        back = Key2("Arrowleft")
        forward = Key2("Arrowright")
        return back, forward

    def dialogue(self):
        sprite_sheet = pygame.image.load("../graphics/icons/sound.png")
        surface = pygame.Surface((30, 31), pygame.SRCALPHA)
        rect = pygame.Rect(0, 0, 30, 31)
        surface.blit(sprite_sheet, (0, 0), rect)

        return pygame.transform.scale(surface, (150, 155)), pygame.Rect(100, 580, 800, 200)

    def draw(self):
        screen.fill(PINK_LACE)
        rect = self.header()
        tts_list, tts_coordinates = self.subtitle()
        megaphone_img, box = self.dialogue()
        sentences = ["Great Job! Now you know about the history, current use and future of", "text-to-speech technology. You're now ready to move onto the game!"]
        tts_image = pygame.transform.scale(pygame.image.load("../graphics/tts_banner.jpg"), (798, 444))
        gfxdraw.box(screen, rect, (0, 0, 0, 100))
        for key, item in tts_coordinates.items():
            item.draw(key)
        tts_progress_bar = TTSProgressBar()
        tts_progress_bar.index = 5
        tts_progress_bar.draw((456, 41))
        gfxdraw.box(screen, box, (0, 0, 0, 100))
        screen.blit(megaphone_img, (120, 597))
        fibberish = pygame.font.Font("../fonts/fibberish.ttf", 20)
        text = fibberish.render(sentences[0], True, (255, 255, 255))
        text2 = fibberish.render(sentences[1], True, (255, 255, 255))
        screen.blit(text, (285, 620))
        screen.blit(text2, (285, 650))
        screen.blit(tts_image, (101, 120))
        play = [Key2("P"), Key2("L"), Key2("A"), Key2("Y"), Key2("Arrowright")]
        x_pos = 600
        y_pos = 720
        play_coordinates = {
            (x_pos, y_pos): play[0],
            (x_pos + 50, y_pos): play[1],
            (x_pos + 100, y_pos): play[2],
            (x_pos + 150, y_pos): play[3],
            (x_pos + 220, y_pos): play[4]
        }
        for key, item in play_coordinates.items():
            item.draw(key)

class Firewall:
    """This class creates the firewall restricing access to the main game unless the TTS course is complete. Most of its methods follow the same logic as the one used in previous TTS scenes, so the same docstrings apply."""

    def __init__(self):
        """The magic keyword / dunder function __init__ initializes the class."""
        pass

    def header(self):
        rect = pygame.Rect(0, 0, WIDTH, HEIGHT // 11)
        return rect

    def subtitle(self):
        tts_list = [Key("T"), Key("T"), Key("S")]
        start = 465
        tts_coordinates = {
            (470, 15): tts_list[0],
            (495, 15): tts_list[1],
            (520, 15): tts_list[2]
        }
        return tts_list, tts_coordinates

    def arrows(self):
        back = Key2("Arrowleft")
        forward = Key2("Arrowright")
        return back, forward

    def dialogue(self):
        sprite_sheet = pygame.image.load("../graphics/icons/sound.png")
        surface = pygame.Surface((30, 31), pygame.SRCALPHA)
        rect = pygame.Rect(0, 0, 30, 31)
        surface.blit(sprite_sheet, (0, 0), rect)

        return pygame.transform.scale(surface, (150, 155)), pygame.Rect(100, 580, 800, 200)

    def draw(self):
        def draw():
            start = 775
            play_coordinates = {
                (start, 525): play[0],
                (start + 25, 525): play[1],
                (start + 50, 525): play[2],
                (start + 75, 525): play[3]
            }
            tts_coordinates = {
                (start, 560): tts[0],
                (start + 25, 560): tts[1],
                (start + 50, 560): tts[2]
            }
            info_coordinates = {
                (start, 595): info[0],
                (start + 25, 595): info[1],
                (start + 50, 595): info[2],
                (start + 75, 595): info[3]
            }
            assets_coordinates = {
                (start, 630): code[0],
                (start + 25, 630): code[1],
                (start + 50, 630): code[2],
                (start + 75, 630): code[3],
                (start + 100, 630): code[4],
                (start + 125, 630): code[5]
            }

            screen.blit(splashscreen.create_bg()[0], splashscreen.create_bg()[1])
            gfxdraw.box(screen, splashscreen.create_shadow(), (0, 0, 0, 50))
            gfxdraw.box(screen, splashscreen.box(), (50, 50, 50, 200))
            screen.blit(splashscreen.title(), (470, 535))
            for key, item in play_coordinates.items():
                item.draw(key)
            for key, item in tts_coordinates.items():
                item.draw(key)
            for key, item in info_coordinates.items():
                item.draw(key)
            for key, item in assets_coordinates.items():
                item.draw(key)

        gfxdraw.box(screen, pygame.Rect(0, 0, WIDTH, HEIGHT), (191, 15, 15, 150))

        correct_message = fibberish_large.render("Sorry!", True, (255, 255, 255))
        confirmation = fibberish_medium.render("You must complete the TTS Course before playing the game", True, (255, 255, 255))
        prompt = fibberish.render("Press esc to go back.", True, (255, 255, 255))

        screen.blit(correct_message, (WIDTH // 2 - (correct_message.get_width() / 2), (HEIGHT // 2) - 50))
        screen.blit(confirmation, (WIDTH // 2 - (confirmation.get_width() / 2), HEIGHT // 2))
        screen.blit(prompt, (WIDTH // 2 - (prompt.get_width() / 2), (HEIGHT // 2) + 50))

class SonusScene:
    """This class creates the scenes with the wizard, Sonus."""
    def __init__(self, bg_image, sonus_dialogue):
        self.bg_image = pygame.image.load(bg_image)
        self.sonus_dialogue = pygame.image.load(sonus_dialogue)

    def header(self):
        rect = pygame.Rect(0, 0, WIDTH, HEIGHT // 11)
        return rect

    def subtitle(self):
        prologue_list = [Key("P"), Key("R"), Key("O"), Key("L"), Key("O"), Key("G"), Key("U"), Key("E")]
        prologue_coordinates = {
            (410, 20): prologue_list[0],
            (435, 20): prologue_list[1],
            (460, 20): prologue_list[2],
            (485, 20): prologue_list[3],
            (510, 20): prologue_list[4],
            (535, 20): prologue_list[5],
            (560, 20): prologue_list[6],
            (585, 20): prologue_list[7]
        }
        return prologue_list, prologue_coordinates

    def arrows(self):
        back = Key2("Arrowleft")
        forward = Key2("Arrowright")
        return back, forward

    def draw(self):
        rect = self.header()
        prologue_list, prologue_coordinates = self.subtitle()
        back, forward = self.arrows()
        screen.blit(pygame.transform.scale(self.bg_image, (1000, 800)), (0, 0))
        gfxdraw.box(screen, rect, (0, 0, 0, 100))
        screen.blit((self.sonus_dialogue), (-10, 50))
        back.draw((362, 13))
        forward.draw((615, 13))
        for key, item in prologue_coordinates.items():
            item.draw(key)


# MORE VARIABLES
loading = (Key2("L"), Key2("O"), Key2("A"), Key2("D"), Key2("I"), Key2("N"), Key2("G"))
play = [Key("P"), Key("L"), Key("A"), Key("Y")]
play_rect = pygame.Rect(775, 525, 94, 21)

tts = [Key("T"), Key("T"), Key("S")]
tts_rect = pygame.Rect(775, 560, 69, 21)

info = [Key("I"), Key("N"), Key("F"), Key("O")]
info_rect = pygame.Rect(775, 595, 94, 21)

code = [Key("A"), Key("S"), Key("S"), Key("E"), Key("T"), Key("S")]
assets_rect = pygame.Rect(775, 630, 144, 21)

# OBJECTS
splashscreen = Splashscreen()
tts_screen1 = TTS1()
tts_screen2 = TTS2()
tts_screen3 = TTS3()
tts_screen4 = TTSTest1()
correct_screen1 = Correct()
incorrect_screen1 = Incorrect()
tts_screen5 = TTSTest2()
correct_screen2 = Correct2()
incorrect_screen2 = Incorrect2()
tts_screen6 = TTSTest3()
correct_screen3 = Correct3()
incorrect_screen3 = Incorrect3()
tts_screen7 = TTS4()
firewall = Firewall()
progress_bar = ProgressBar()
sonus_scene1 = SonusScene("../graphics/magic_forest.jpg", "../graphics/dialogue1.png")
sonus_scene2 = SonusScene("../graphics/magic_forest.jpg", "../graphics/dialogue2.png")
sonus_scene3 = SonusScene("../graphics/magic_forest.jpg", "../graphics/dialogue3.png")
sonus_scene4 = SonusScene("../graphics/magic_forest.jpg", "../graphics/dialogue4.png")

# CUSTOM EVENTS
INCREASE = pygame.USEREVENT + 1
pygame.time.set_timer(INCREASE, 5000)

NEW_SCENE = pygame.USEREVENT + 2
pygame.time.set_timer(NEW_SCENE, 27000)

# STATE MACHINE
class StateMachine:
    def __init__(self):
        self.scene = "splashscreen"

    def loading_screen(self):
        global running
        draw(screen, progress_bar)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == INCREASE:
                progress_bar.index += 1
                if progress_bar.index == 6:
                    progress_bar.index = 1
            if event.type == NEW_SCENE:
                self.scene = "splashscreen"

    def splashscreen(self):
        pygame.mixer.init()
        global running
        global certificate
        for event in pygame.event.get():
            splashscreen.draw()
            pygame.display.update()

            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(pygame.mouse.get_pos()):
                    if certificate:
                        pygame.mixer.quit()
                        self.scene = "wizard1"
                        certificate = True
                    if not certificate:
                        self.scene = "firewall"

                elif tts_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.mixer.quit()
                    self.scene = "tts_screen1"
                elif info_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.mixer.quit()
                    self.scene = "info_screen"
                elif assets_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.mixer.quit()
                    self.scene = "assets_screen"
    pygame.mixer.music.load("../audio/sonus_music.wav")
    pygame.mixer.music.play()

    def firewall(self):
        global running
        for event in pygame.event.get():
            firewall.draw()
            pygame.display.update()
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.scene = "splashscreen"

    def wizard1(self):
        pygame.mixer.init()
        global running
        global clicks
        for event in pygame.event.get():
            sonus_scene1.draw()
            pygame.display.update()
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and clicks == 0:
                if event.key == pygame.K_SPACE:
                    clicks += 1
                    speech = pygame.mixer.Sound("../audio/wizard1.wav")
                    speech.play()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(615, 13, 38, 42).collidepoint(pygame.mouse.get_pos()):
                    pygame.mixer.quit()
                    clicks = 0
                    self.scene = "wizard2"

    def wizard2(self):
        pygame.mixer.init()
        global running
        global clicks
        for event in pygame.event.get():
            sonus_scene2.draw()
            pygame.display.update()
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and clicks == 0:
                if event.key == pygame.K_SPACE:
                    clicks += 1
                    speech = pygame.mixer.Sound("../audio/wizard2.wav")
                    speech.play()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(362, 16, 38, 42).collidepoint(pygame.mouse.get_pos()):
                    pygame.mixer.quit()
                    clicks = 0
                    self.scene = "wizard1"
                elif pygame.Rect(615, 13, 38, 42).collidepoint(pygame.mouse.get_pos()):
                    pygame.mixer.quit()
                    clicks = 0
                    self.scene = "wizard3"

    def wizard3(self):
        global running
        global clicks
        pygame.mixer.init()
        for event in pygame.event.get():
            sonus_scene3.draw()
            pygame.display.update()
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and clicks == 0:
                if event.key == pygame.K_SPACE:
                    clicks += 1
                    speech = pygame.mixer.Sound("../audio/wizard3.wav")
                    speech.play()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(362, 16, 38, 42).collidepoint(pygame.mouse.get_pos()):
                    clicks = 0
                    pygame.mixer.quit()
                    self.scene = "wizard2"
                elif pygame.Rect(615, 13, 38, 42).collidepoint(pygame.mouse.get_pos()):
                    clicks = 0
                    pygame.mixer.quit()
                    self.scene = "tutorial"

    def tutorial(self):
        pygame.mixer.init()
        global running
        global clicks
        for event in pygame.event.get():
            sonus_scene4.draw()
            pygame.display.update()
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and clicks == 0:
                if event.key == pygame.K_SPACE:
                    clicks += 1
                    speech = pygame.mixer.Sound("../audio/tutorial.wav")
                    speech.play()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(362, 16, 38, 42).collidepoint(pygame.mouse.get_pos()):
                    pygame.mixer.quit()
                    clicks = 0
                    self.scene = "wizard3"
                elif pygame.Rect(615, 13, 38, 42).collidepoint(pygame.mouse.get_pos()):
                    pygame.mixer.quit()
                    clicks = 0
                    self.scene = "level1"

    def level1(self):
        pygame.mixer.init()
        with open("main.py") as f:
            exec(f.read())

    def tts_screen1(self):
        global running
        global hello
        global button_func
        back_arrow_rect = pygame.Rect(406, 13, 38, 42)
        forward_arrow_rect = pygame.Rect(565, 13, 38, 42)

        for event in pygame.event.get():
            pygame.mixer.init()
            tts_screen1.draw()
            pygame.display.update()
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.scene = "splashscreen"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(120, 597, 150, 155).collidepoint(pygame.mouse.get_pos()):
                    speech = pygame.mixer.Sound("../audio/tts1.wav")
                    channel1 = pygame.mixer.Channel(0)
                    if button_func == "play":
                        pygame.mixer.find_channel().play(speech)
                        button_func = "stop"
                    elif button_func == "stop":
                        channel1.stop()
                        button_func = "play"
                elif back_arrow_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.mixer.quit()
                    button_func = "play"
                    self.scene = "splashscreen"
                elif forward_arrow_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.mixer.quit()
                    button_func = "play"
                    self.scene = "tts_screen2"

    def tts_screen2(self):
        global running
        global button_func
        back_arrow_rect = pygame.Rect(406, 13, 38, 42)
        forward_arrow_rect = pygame.Rect(565, 13, 38, 42)

        for event in pygame.event.get():
            pygame.mixer.init()
            tts_screen2.draw()
            pygame.display.update()
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(120, 597, 150, 155).collidepoint(pygame.mouse.get_pos()):
                    speech = pygame.mixer.Sound("../audio/tts2.wav")
                    channel1 = pygame.mixer.Channel(0)
                    if button_func == "play":
                        pygame.mixer.find_channel().play(speech)
                        button_func = "stop"
                    elif button_func == "stop":
                        channel1.stop()
                        button_func = "play"
                elif back_arrow_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.mixer.quit()
                    button_func = "play"
                    self.scene = "tts_screen1"
                elif forward_arrow_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.mixer.quit()
                    button_func = "play"
                    self.scene = "tts_screen3"

    def tts_screen3(self):
        global running
        global button_func
        back_arrow_rect = pygame.Rect(406, 13, 38, 42)
        forward_arrow_rect = pygame.Rect(565, 13, 38, 42)

        for event in pygame.event.get():
            pygame.mixer.init()
            tts_screen3.draw()
            pygame.display.update()
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(120, 597, 150, 155).collidepoint(pygame.mouse.get_pos()):
                    speech = pygame.mixer.Sound("../audio/tts3.wav")
                    channel1 = pygame.mixer.Channel(0)
                    if button_func == "play":
                        pygame.mixer.find_channel().play(speech)
                        button_func = "stop"
                    elif button_func == "stop":
                        channel1.stop()
                        button_func = "play"
                elif back_arrow_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.mixer.quit()
                    button_func = "play"
                    self.scene = "tts_screen2"
                elif forward_arrow_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.mixer.quit()
                    button_func = "play"
                    self.scene = "tts_screen4"

    def tts_screen4(self):
        pygame.mixer.init()
        global running
        global your_answer
        global button_func

        answer1_rect = pygame.Rect(620, 120, 280, 80)
        answer2_rect = pygame.Rect(620, 241, 280, 80)
        answer3_rect = pygame.Rect(620, 362, 280, 80)
        answer4_rect = pygame.Rect(620, 483, 280, 80)

        for event in pygame.event.get():
            tts_screen4.draw()
            pygame.display.update()
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(120, 597, 150, 155).collidepoint(pygame.mouse.get_pos()):
                    speech = pygame.mixer.Sound("../audio/question1.wav")
                    channel1 = pygame.mixer.Channel(0)
                    if button_func == "play":
                        pygame.mixer.find_channel().play(speech)
                        button_func = "stop"
                    elif button_func == "stop":
                        channel1.stop()
                        button_func = "play"
                elif answer1_rect.collidepoint(pygame.mouse.get_pos()):
                    self.scene = "correct"
                    pygame.mixer.quit()
                    button_func = "play"
                    your_answer = "Text to Speech"
                elif answer2_rect.collidepoint(pygame.mouse.get_pos()):
                    self.scene = "incorrect"
                    pygame.mixer.quit()
                    button_func = "play"
                    your_answer = "Speech to Text"
                elif answer3_rect.collidepoint(pygame.mouse.get_pos()):
                    self.scene = "incorrect"
                    pygame.mixer.quit()
                    button_func = "play"
                    your_answer = "Touch Type Software"
                elif answer4_rect.collidepoint(pygame.mouse.get_pos()):
                    self.scene = "incorrect"
                    pygame.mixer.quit()
                    button_func = "play"
                    your_answer = "Type Text System"

    def tts_screen5(self):
        pygame.mixer.init()
        global running
        global your_answer
        global button_func

        answer1_rect = pygame.Rect(620, 120, 280, 80)
        answer2_rect = pygame.Rect(620, 241, 280, 80)
        answer3_rect = pygame.Rect(620, 362, 280, 80)
        answer4_rect = pygame.Rect(620, 483, 280, 80)

        for event in pygame.event.get():
            tts_screen5.draw()
            pygame.display.update()
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(120, 597, 150, 155).collidepoint(pygame.mouse.get_pos()):
                    speech = pygame.mixer.Sound("../audio/question2.wav")
                    channel1 = pygame.mixer.Channel(0)
                    if button_func == "play":
                        pygame.mixer.find_channel().play(speech)
                        button_func = "stop"
                    elif button_func == "stop":
                        channel1.stop()
                        button_func = "play"
                if answer1_rect.collidepoint(pygame.mouse.get_pos()):
                    self.scene = "incorrect2"
                    pygame.mixer.quit()
                    button_func = "play"
                    your_answer = "Canada"
                if answer2_rect.collidepoint(pygame.mouse.get_pos()):
                    self.scene = "incorrect2"
                    pygame.mixer.quit()
                    button_func = "play"
                    your_answer = "China"
                if answer3_rect.collidepoint(pygame.mouse.get_pos()):
                    self.scene = "correct2"
                    pygame.mixer.quit()
                    button_func = "play"
                    your_answer = "Japan"
                if answer4_rect.collidepoint(pygame.mouse.get_pos()):
                    self.scene = "incorrect2"
                    pygame.mixer.quit()
                    button_func = "play"
                    your_answer = "Netherlands"

    def tts_screen6(self):
        pygame.mixer.init()
        global running
        global button_func
        global your_answer

        answer1_rect = pygame.Rect(620, 120, 280, 80)
        answer2_rect = pygame.Rect(620, 241, 280, 80)
        answer3_rect = pygame.Rect(620, 362, 280, 80)
        answer4_rect = pygame.Rect(620, 483, 280, 80)

        for event in pygame.event.get():
            tts_screen6.draw()
            pygame.display.update()
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(120, 597, 150, 155).collidepoint(pygame.mouse.get_pos()):
                    speech = pygame.mixer.Sound("../audio/question3.wav")
                    channel1 = pygame.mixer.Channel(0)
                    if button_func == "play":
                        pygame.mixer.find_channel().play(speech)
                        button_func = "stop"
                    elif button_func == "stop":
                        channel1.stop()
                        button_func = "play"
                if answer1_rect.collidepoint(pygame.mouse.get_pos()):
                    self.scene = "incorrect3"
                    pygame.mixer.quit()
                    button_func = "play"
                    your_answer = "100 years"
                if answer2_rect.collidepoint(pygame.mouse.get_pos()):
                    self.scene = "incorrect3"
                    pygame.mixer.quit()
                    button_func = "play"
                    your_answer = "A decade"
                if answer3_rect.collidepoint(pygame.mouse.get_pos()):
                    self.scene = "incorrect3"
                    pygame.mixer.quit()
                    button_func = "play"
                    your_answer = "27 years"
                if answer4_rect.collidepoint(pygame.mouse.get_pos()):
                    self.scene = "correct3"
                    pygame.mixer.quit()
                    button_func = "play"
                    your_answer = "55 years"

    def tts_screen7(self):
        pygame.mixer.init()
        global running
        global button_func
        global certificate
        hyperlink_rect = pygame.Rect(600, 720, 258, 42)

        for event in pygame.event.get():
            tts_screen7.draw()
            pygame.display.update()
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(120, 597, 150, 155).collidepoint(pygame.mouse.get_pos()):
                    speech = pygame.mixer.Sound("../audio/congrats.wav")
                    channel1 = pygame.mixer.Channel(0)
                    if button_func == "play":
                        pygame.mixer.find_channel().play(speech)
                        button_func = "stop"
                    elif button_func == "stop":
                        channel1.stop()
                        button_func = "play"
                if hyperlink_rect.collidepoint(pygame.mouse.get_pos()):
                    certificate = True
                    button_func = "play"
                    pygame.mixer.quit()
                    self.scene = "splashscreen"

    def correct(self):
        global running
        for event in pygame.event.get():
            correct_screen1.draw()
            pygame.display.update()
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.scene = "tts_screen5"

    def incorrect(self):
        global running
        for event in pygame.event.get():
            incorrect_screen1.draw()
            pygame.display.update()
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.scene = "tts_screen4"

    def correct2(self):
        global running
        for event in pygame.event.get():
            correct_screen2.draw()
            pygame.display.update()
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.scene = "tts_screen6"

    def incorrect2(self):
        global running
        for event in pygame.event.get():
            incorrect_screen2.draw()
            pygame.display.update()
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.scene = "tts_screen5"

    def correct3(self):
        global running
        for event in pygame.event.get():
            correct_screen3.draw()
            pygame.display.update()
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.scene = "tts_screen7"

    def incorrect3(self):
        global running
        for event in pygame.event.get():
            incorrect_screen3.draw()
            pygame.display.update()
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.scene = "tts_screen6"

    def info_screen(self):
        global running
        for event in pygame.event.get():
            screen.fill((255, 0, 0))
            pygame.display.update()
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.scene = "splashscreen"

    def assets_screen(self):
        global running
        for event in pygame.event.get():
            screen.fill((255, 255, 0))
            pygame.display.update()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.scene = "splashscreen"

    def state_manager(self):
        if self.scene == "loading_screen":
            self.loading_screen()
        elif self.scene == "splashscreen":
            self.splashscreen()
        elif self.scene == "wizard1":
            self.wizard1()
        elif self.scene == "wizard2":
            self.wizard2()
        elif self.scene == "wizard3":
            self.wizard3()
        elif self.scene == "tts_screen1":
            self.tts_screen1()
        elif self.scene == "tts_screen2":
            self.tts_screen2()
        elif self.scene == "tts_screen3":
            self.tts_screen3()
        elif self.scene == "tts_screen4":
            self.tts_screen4()
        elif self.scene == "tts_screen5":
            self.tts_screen5()
        elif self.scene == "info_screen":
            self.info_screen()
        elif self.scene == "assets_screen":
            self.assets_screen()
        elif self.scene == "correct":
            self.correct()
        elif self.scene == "incorrect":
            self.incorrect()
        elif self.scene == "correct2":
            self.correct2()
        elif self.scene == "incorrect2":
            self.incorrect2()
        elif self.scene == "tts_screen6":
            self.tts_screen6()
        elif self.scene == "correct3":
            self.correct3()
        elif self.scene == "incorrect3":
            self.incorrect3()
        elif self.scene == "tts_screen7":
            self.tts_screen7()
        elif self.scene == "firewall":
            self.firewall()
        elif self.scene == "tutorial":
            self.tutorial()
        elif self.scene == "level1":
            self.level1()

state_manager = StateMachine()

# GAME LOOP
while running:
    state_manager.state_manager()
pygame.quit()
