# NAMES: DINIM ONIGYE & EDAFE ETUKE
# PLAYER CONTROLS

# IMPORTS
import pygame
from support import import_folder

# SETUP
pygame.init()

# CLASSES
class Player(pygame.sprite.Sprite):
    """This class creates a player object which is used in the level class."""
    def __init__(self, pos, surface):
        """The magic keyword / dunder function __init__ initializes the class."""
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        # player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16

        # player status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

    def import_character_assets(self):
        """This function gets the different sprites for player movement (or being idle)"""
        character_path = '../graphics/character/'
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        """This function animates the player by switching through the different sprites when the player is running, falling, jumping or being idle."""
        animation = self.animations[self.status]

        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image

        # set the rect
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright=self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)

    def get_input(self):
        """This function gets keyboard input and uses it to move the character."""
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        if keys[pygame.K_UP] and self.on_ground:
            self.jump()

    def get_status(self):
        """This function figures out what the player is doing based on its velocity in the x and y directions."""
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def apply_gravity(self):
        """This function simulates gravity for the player."""
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        """This function allows the player to defy gravity for a short while."""
        self.direction.y = self.jump_speed

    def update(self):
        """This function is a built-in function for pygame.sprite.Sprite used to update whole groups at once."""
        self.get_input()
        self.get_status()
        self.animate()
