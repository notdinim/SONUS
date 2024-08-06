# NAMES: DINIM ONIGYE & EDAFE ETUKE
# TILE CLASSES

# IMPORTS
import pygame
# https://www.programiz.com/python-programming/class
class Tile(pygame.sprite.Sprite):
	"""This class creates a basic Tile, used for inheritance."""
	def __init__(self,size,x,y):
		super().__init__()
		self.image = pygame.Surface((size,size))
		self.rect = self.image.get_rect(topleft = (x,y))

	def update(self, x_shift):
		self.rect.x += x_shift

class StaticTile(Tile):
	"""This class creates a basic Tile, inherited from the Tile class"""
	def __init__(self,size,x,y,surface):
		super().__init__(size,x,y)
		self.image = surface

class Crate(StaticTile):
	"""This class inherits from the StaticTile class to create the chests/crates."""
	def __init__(self,size,x,y):
		super().__init__(size,x,y,pygame.image.load('../graphics/terrain/chest.png').convert_alpha())
		offset_y = y + size
		self.rect = self.image.get_rect(bottomleft = (x,offset_y))