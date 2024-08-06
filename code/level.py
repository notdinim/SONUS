# NAMES: DINIM ONIGYE & EDAFE ETUKE
# LEVEL CODE

# IMPORTS
import pygame
from pygame import gfxdraw
from settings import *
from support import import_csv_layout, import_cut_graphics
from settings import tile_size
from tiles import StaticTile, Crate
from player import Player
# from gtts import gTTS
from random import randint

# FUNCTIONS
def load_sprite_keys(letter, width, height):
	path = "../graphics/SimpleKeys/Jumbo/Light/Spritesheets/" + f"{letter.upper()}.png"
	sprite_sheet = pygame.image.load(path)

	sprite = []

	for i in range(sprite_sheet.get_width() // width):
		surface = pygame.Surface((width, height), pygame.SRCALPHA)
		rect = pygame.Rect(i * width, 0, width, height)
		surface.blit(sprite_sheet, (0, 0), rect)
		sprite.append(surface)

	return sprite

# CLASSES
class Key:
	"""This function creates a key object of a letter of choice."""
	ANIMATION_DELAY = 30

	def __init__(self, letter):
		"""The magic keyword / dunder function __init__ initializes the class."""
		self.animation_count = 0
		self.sprites = load_sprite_keys(letter, 19, 21)

	def draw(self, placement, display):
		"""This function draws the key on a display of choice, in a specific place."""
		sprite_index = (self.animation_count // self.ANIMATION_DELAY % len(self.sprites))
		self.sprite = self.sprites[sprite_index]
		self.animation_count += 1
		display.blit(self.sprite, placement)

class Level:
	"""This class creates a level object (specifically level 1) that takes in a tile map and a pygame.Surface to be drawn upon."""

	def __init__(self,level_data,surface):
		"""The magic keyword / dunder function __init__ initializes the class."""
		# general setup
		self.display_surface = surface # screen to be drawn on
		self.world_shift = 0 # default side-scroll
		self.current_x = None # variable containing player's x position
		self.talk = True # boolean controlling playback
		self.speaker_on = False # other boolean controlling playback
		self.collected_words = {} # dictionary containing words collected by player

		# Player Setup
		self.player_layout = import_csv_layout(level_data['player'])
		self.player = pygame.sprite.GroupSingle()
		self.goal = pygame.sprite.GroupSingle()
		self.player_setup(self.player_layout)

		# Terrain Tiles Setup
		terrain_layout = import_csv_layout(level_data['terrain'])
		self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')

		# Grass Tiles Setup
		grass_layout = import_csv_layout(level_data['grass'])
		self.grass_sprites = self.create_tile_group(grass_layout,'grass')

		# Chest Tiles Setup
		chest_layout = import_csv_layout(level_data['chests'])
		self.chest_sprites = self.create_tile_group(chest_layout,'chests')

	def create_tile_group(self,layout,type):
		"""This function creates a pyagme.sprite.Group() object that allows all tiles of the same type to be controlled at once."""
		sprite_group = pygame.sprite.Group()

		# Getting Tile Positions
		for row_index, row in enumerate(layout):
			for col_index,val in enumerate(row):
				if val != '-1':
					x = col_index * tile_size
					y = row_index * tile_size

					# Terrain Tile Group Setup
					if type == 'terrain':
						terrain_tile_list = import_cut_graphics('../graphics/terrain/tileset.png')
						tile_surface = terrain_tile_list[int(val)]
						sprite = StaticTile(tile_size,x,y, tile_surface)

					# Grass Tile Group Setup
					if type == 'grass':
						grass_tile_list = import_cut_graphics('../graphics/terrain/grass.png')
						tile_surface = grass_tile_list[int(val)]
						sprite = StaticTile(tile_size,x,y,tile_surface)

					# Chests Tile Group Setup
					if type == 'chests':
						sprite = Crate(tile_size,x,y)

					sprite_group.add(sprite)

		return sprite_group

	def player_setup(self,layout):
		"""This function places te player in the starting position."""
		for row_index, row in enumerate(layout):
			for col_index,val in enumerate(row):
				x = col_index * tile_size
				y = row_index * tile_size
				if val == '0':
					sprite = Player((x, y), self.display_surface)
					self.player.add(sprite)
				if val == '1':
					start = pygame.image.load("../graphics/terrain/start.jpg").convert_alpha()
					sprite = StaticTile(tile_size,x,y,start)
					self.goal.add(sprite)

	def horizontal_movement_collision(self):
		"""This function controls the horizontal collisions of the player with the terrain."""
		player = self.player.sprite
		player.rect.x += player.direction.x * player.speed
		collidable_sprites = self.terrain_sprites.sprites()
		for sprite in collidable_sprites:
			if sprite.rect.colliderect(player.rect):
				if player.direction.x < 0:
					player.rect.left = sprite.rect.right
					player.on_left = True
					self.current_x = player.rect.left
				elif player.direction.x > 0:
					player.rect.right = sprite.rect.left
					player.on_right = True
					self.current_x = player.rect.right

		if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
			player.on_left = False
		if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
			player.on_right = False

	def vertical_movement_collision(self):
		"""This function controls the vertical collision between the player and the terrain."""
		player = self.player.sprite
		player.apply_gravity()
		collidable_sprites = self.terrain_sprites.sprites()

		for sprite in collidable_sprites:
			if sprite.rect.colliderect(player.rect):
				if player.direction.y > 0:
					player.rect.bottom = sprite.rect.top
					player.direction.y = 0
					player.on_ground = True
				elif player.direction.y < 0:
					player.rect.top = sprite.rect.bottom
					player.direction.y = 0
					player.on_ceiling = True

		if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
			player.on_ground = False
		if player.on_ceiling and player.direction.y > 0.1:
			player.on_ceiling = False

	def scroll_x(self):
		"""This function controls the side-scrolling feature, getting influenced by the player position."""
		player = self.player.sprite
		player_x = player.rect.centerx
		direction_x = player.direction.x

		if player_x < screen_width / 4 and direction_x < 0:
			self.world_shift = 10
			player.speed = 0
		elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
			self.world_shift = -10
			player.speed = 0
		else:
			self.world_shift = 0
			player.speed = 10

	def collection(self):
		"""This function controls the chest collection feature."""
		keys = [(410, 60), (480, 60), (600, 60), (670, 60)]
		move = 400
		words = [pygame.transform.scale(pygame.image.load("../graphics/my.png"), (47, 26)), pygame.transform.scale(pygame.image.load("../graphics/name.png"), (93, 26)), pygame.transform.scale(pygame.image.load("../graphics/is.png"), (43, 23)), pygame.transform.scale(pygame.image.load("../graphics/sonus.png"), (117, 26))]
		chest_collisions = pygame.sprite.spritecollide(self.player.sprite, self.chest_sprites, True)
		index = -len(self.chest_sprites.sprites()) - 1
		for chest in chest_collisions:
			self.collected_words[keys[index]] = words[index]

	def check_death(self):
		"""This function controls the next steps after the player falls."""
		if self.player.sprite.rect.top > screen_height:
			self.collected_words = {}
			self.speaker_on = False
			with open("respawn.py") as f:
				exec(f.read())

	def draw_subtitle(self):
		"""This function draws a subtitle at the top of the game screen."""

		level1_list = [Key("L"), Key("E"), Key("V"), Key("E"), Key("L"), Key("1")]
		level1_coordinates = {
			(520, 20): level1_list[0],
			(545, 20): level1_list[1],
			(570, 20): level1_list[2],
			(595, 20): level1_list[3],
			(620, 20): level1_list[4],
			(665, 20): level1_list[5]
		}
		return level1_list, level1_coordinates

	def draw_dialogue(self):
		"""This function draws the sound icon when needed."""
		sprite_sheet = pygame.image.load("../graphics/icons/sound.png")
		surface = pygame.Surface((30, 31), pygame.SRCALPHA)
		rect = pygame.Rect(0, 0, 30, 31)
		surface.blit(sprite_sheet, (0, 0), rect)

		return pygame.transform.scale(surface, (75, 77.5))

	def run(self):
		"""This function runs the level."""
		global completed

		self.terrain_sprites.draw(self.display_surface)
		self.terrain_sprites.update(self.world_shift)

		self.grass_sprites.update(self.world_shift)
		self.grass_sprites.draw(self.display_surface)

		self.chest_sprites.update(self.world_shift)
		self.chest_sprites.draw(self.display_surface)

		self.check_death()
		self.collection()

		self.player.update()
		self.horizontal_movement_collision()
		self.vertical_movement_collision()
		self.scroll_x()
		self.player.draw(self.display_surface)
		self.goal.update(self.world_shift)
		self.goal.draw(self.display_surface)

		# drawings
		gfxdraw.box(self.display_surface, pygame.Rect(0, 0, screen_width, screen_height / 7), (40, 41, 41, 200))
		level1_list, level1_coordinates = self.draw_subtitle()
		for key, item in level1_coordinates.items():
			item.draw(key, self.display_surface)
		if len(self.collected_words) == 0:
			pass
		else:
			for key, item in self.collected_words.items():
				self.display_surface.blit(item, key)

		if len(self.chest_sprites.sprites()) == 0:
			self.speaker_on = True

		if self.speaker_on:
			megaphone = self.draw_dialogue()
			self.display_surface.blit(megaphone, (300, 10))

		if self.talk:
			keys = pygame.key.get_pressed()
			if keys[pygame.K_SPACE] and self.speaker_on:
				pygame.mixer.init()
				sentence1 = pygame.mixer.Sound("../audio/sentence1.wav")
				sentence1.play()
				unlocked2 = True
				self.speaker_on = False
				pygame.time.delay(3000)
				with open("main2.py") as f:
					exec(f.read())

class Level2:
	"""This class creates a level object (specifically level 2) that takes in a tile map and a pygame.Surface to be drawn upon."""

	def __init__(self,level_data,surface):
		"""The magic keyword / dunder function __init__ initializes the class."""
		# general setup
		self.display_surface = surface
		self.world_shift = 0
		self.current_x = None
		self.talk = True
		self.collected_words = {}
		self.speaker_on = False

		self.player_layout = import_csv_layout(level_data['player'])
		self.player = pygame.sprite.GroupSingle()
		self.goal = pygame.sprite.GroupSingle()
		self.player_setup(self.player_layout)

		terrain_layout = import_csv_layout(level_data['terrain'])
		self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')

		chest_layout = import_csv_layout(level_data['chests'])
		self.chest_sprites = self.create_tile_group(chest_layout,'chests')

	def create_tile_group(self,layout,type):
		"""This function creates a pyagme.sprite.Group() object that allows all tiles of the same type to be controlled at once."""
		sprite_group = pygame.sprite.Group()

		for row_index, row in enumerate(layout):
			for col_index,val in enumerate(row):
				if val != '-1':
					x = col_index * tile_size
					y = row_index * tile_size

					if type == 'terrain':
						terrain_tile_list = import_cut_graphics('../graphics/terrain/tileset.png')
						tile_surface = terrain_tile_list[int(val)]
						sprite = StaticTile(tile_size,x,y, tile_surface)

					if type == 'chests':
						sprite = Crate(tile_size,x,y)

					sprite_group.add(sprite)

		return sprite_group

	def player_setup(self,layout):
		"""This function places te player in the starting position."""
		for row_index, row in enumerate(layout):
			for col_index,val in enumerate(row):
				x = col_index * tile_size
				y = row_index * tile_size
				if val == '0':
					sprite = Player((x, y), self.display_surface)
					self.player.add(sprite)
				if val == '1':
					start = pygame.image.load("../graphics/terrain/start.jpg").convert_alpha()
					sprite = StaticTile(tile_size,x,y,start)
					self.goal.add(sprite)

	def horizontal_movement_collision(self):
		"""This function controls the horizontal collisions of the player with the terrain."""
		player = self.player.sprite
		player.rect.x += player.direction.x * player.speed
		collidable_sprites = self.terrain_sprites.sprites()
		for sprite in collidable_sprites:
			if sprite.rect.colliderect(player.rect):
				if player.direction.x < 0:
					player.rect.left = sprite.rect.right
					player.on_left = True
					self.current_x = player.rect.left
				elif player.direction.x > 0:
					player.rect.right = sprite.rect.left
					player.on_right = True
					self.current_x = player.rect.right

		if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
			player.on_left = False
		if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
			player.on_right = False

	def vertical_movement_collision(self):
		"""This function controls the vertical collision between the player and the terrain."""
		player = self.player.sprite
		player.apply_gravity()
		collidable_sprites = self.terrain_sprites.sprites()

		for sprite in collidable_sprites:
			if sprite.rect.colliderect(player.rect):
				if player.direction.y > 0:
					player.rect.bottom = sprite.rect.top
					player.direction.y = 0
					player.on_ground = True
				elif player.direction.y < 0:
					player.rect.top = sprite.rect.bottom
					player.direction.y = 0
					player.on_ceiling = True

		if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
			player.on_ground = False
		if player.on_ceiling and player.direction.y > 0.1:
			player.on_ceiling = False

	def scroll_x(self):
		"""This function controls the side-scrolling feature, getting influenced by the player position."""
		player = self.player.sprite
		player_x = player.rect.centerx
		direction_x = player.direction.x

		if player_x < screen_width / 4 and direction_x < 0:
			self.world_shift = 10
			player.speed = 0
		elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
			self.world_shift = -10
			player.speed = 0
		else:
			self.world_shift = 0
			player.speed = 10

	def collection(self):
		"""This function controls the chest collection feature."""
		keys = [(140, 60), (190, 60), (370, 60), (480, 60), (680, 60), (820, 60), (960, 60)]
		move = 400
		words = [pygame.transform.scale(pygame.image.load("../graphics/im.png"), (42, 26)), pygame.transform.scale(pygame.image.load("../graphics/craving.png"), (171, 26)), pygame.transform.scale(pygame.image.load("../graphics/some.png"), (96, 26)), pygame.transform.scale(pygame.image.load("../graphics/hawaiian.png"), (196, 25)), pygame.transform.scale(pygame.image.load("../graphics/pizza.png"), (123, 25)), pygame.transform.scale(pygame.image.load("../graphics/right.png"), (119, 25)), pygame.transform.scale(pygame.image.load("../graphics/now.png"), (73, 25))]
		chest_collisions = pygame.sprite.spritecollide(self.player.sprite, self.chest_sprites, True)
		index = -len(self.chest_sprites.sprites()) - 1
		for chest in chest_collisions:
			self.collected_words[keys[index]] = words[index]

	def check_death(self):
		"""This function controls the next steps after the player falls."""
		if self.player.sprite.rect.top > screen_height:
			self.collected_words = {}
			self.speaker_on = False
			with open("respawn2.py") as f:
				exec(f.read())

	def draw_subtitle(self):
		"""This function draws a subtitle at the top of the game screen."""
		level1_list = [Key("L"), Key("E"), Key("V"), Key("E"), Key("L"), Key("2")]
		level1_coordinates = {
			(520, 20): level1_list[0],
			(545, 20): level1_list[1],
			(570, 20): level1_list[2],
			(595, 20): level1_list[3],
			(620, 20): level1_list[4],
			(665, 20): level1_list[5]
		}
		return level1_list, level1_coordinates

	def draw_dialogue(self):
		"""This function draws the sound icon when needed."""
		sprite_sheet = pygame.image.load("../graphics/icons/sound.png")
		surface = pygame.Surface((30, 31), pygame.SRCALPHA)
		rect = pygame.Rect(0, 0, 30, 31)
		surface.blit(sprite_sheet, (0, 0), rect)

		return pygame.transform.scale(surface, (75, 77.5))

	def run(self):
		"""This function runs the level."""
		self.terrain_sprites.draw(self.display_surface)
		self.terrain_sprites.update(self.world_shift)

		self.chest_sprites.update(self.world_shift)
		self.chest_sprites.draw(self.display_surface)

		self.check_death()
		self.collection()

		self.player.update()
		self.horizontal_movement_collision()
		self.vertical_movement_collision()
		self.scroll_x()
		self.player.draw(self.display_surface)
		self.goal.update(self.world_shift)
		self.goal.draw(self.display_surface)

		# drawings
		gfxdraw.box(self.display_surface, pygame.Rect(0, 0, screen_width, screen_height / 7), (40, 41, 41, 200))
		level1_list, level1_coordinates = self.draw_subtitle()
		for key, item in level1_coordinates.items():
			item.draw(key, self.display_surface)
		if len(self.collected_words) == 0:
			pass
		else:
			for key, item in self.collected_words.items():
				self.display_surface.blit(item, key)

		if len(self.chest_sprites.sprites()) == 0:
			self.speaker_on = True
			completed2 = True

		if self.speaker_on:
			megaphone = self.draw_dialogue()
			self.display_surface.blit(megaphone, (30, 10))

		if self.talk:
			keys = pygame.key.get_pressed()
			if keys[pygame.K_SPACE] and self.speaker_on:

				pygame.mixer.init()
				sentence2 = pygame.mixer.Sound("../audio/sentence2.wav")
				sentence2.play()
				unlocked3 = True
				self.speaker_on = False
				pygame.time.delay(3500)
				with open("main3.py") as f:
					exec(f.read())

class Level3:
	"""This class creates a level object (specifically level 3) that takes in a tile map and a pygame.Surface to be drawn upon."""

	def __init__(self,level_data,surface):
		"""The magic keyword / dunder function __init__ initializes the class."""
		# general setup
		self.display_surface = surface
		self.world_shift = 0
		self.current_x = None
		self.talk = True
		self.speaker_on = False
		self.collected_words = {}

		self.player_layout = import_csv_layout(level_data['player'])
		self.player = pygame.sprite.GroupSingle()
		self.goal = pygame.sprite.GroupSingle()
		self.player_setup(self.player_layout)

		terrain_layout = import_csv_layout(level_data['terrain'])
		self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')

		grass_layout = import_csv_layout(level_data['grass'])
		self.grass_sprites = self.create_tile_group(grass_layout,'grass')

		chest_layout = import_csv_layout(level_data['chests'])
		self.chest_sprites = self.create_tile_group(chest_layout,'chests')

	def create_tile_group(self,layout,type):
		"""This function creates a pyagme.sprite.Group() object that allows all tiles of the same type to be controlled at once."""
		sprite_group = pygame.sprite.Group()

		for row_index, row in enumerate(layout):
			for col_index,val in enumerate(row):
				if val != '-1':
					x = col_index * tile_size
					y = row_index * tile_size

					if type == 'terrain':
						terrain_tile_list = import_cut_graphics('../graphics/terrain/tileset.png')
						tile_surface = terrain_tile_list[int(val)]
						sprite = StaticTile(tile_size,x,y, tile_surface)

					if type == 'grass':
						grass_tile_list = import_cut_graphics('../graphics/terrain/grass.png')
						tile_surface = grass_tile_list[int(val)]
						sprite = StaticTile(tile_size,x,y,tile_surface)

					if type == 'chests':
						sprite = Crate(tile_size,x,y)

					sprite_group.add(sprite)

		return sprite_group

	def player_setup(self,layout):
		"""This function places te player in the starting position."""
		for row_index, row in enumerate(layout):
			for col_index,val in enumerate(row):
				x = col_index * tile_size
				y = row_index * tile_size
				if val == '0':
					sprite = Player((x, y), self.display_surface)
					self.player.add(sprite)
				if val == '1':
					start = pygame.image.load("../graphics/terrain/start.jpg").convert_alpha()
					sprite = StaticTile(tile_size,x,y,start)
					self.goal.add(sprite)

	def horizontal_movement_collision(self):
		"""This function controls the horizontal collisions of the player with the terrain."""
		player = self.player.sprite
		player.rect.x += player.direction.x * player.speed
		collidable_sprites = self.terrain_sprites.sprites()
		for sprite in collidable_sprites:
			if sprite.rect.colliderect(player.rect):
				if player.direction.x < 0:
					player.rect.left = sprite.rect.right
					player.on_left = True
					self.current_x = player.rect.left
				elif player.direction.x > 0:
					player.rect.right = sprite.rect.left
					player.on_right = True
					self.current_x = player.rect.right

		if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
			player.on_left = False
		if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
			player.on_right = False

	def vertical_movement_collision(self):
		"""This function controls the vertical collision between the player and the terrain."""
		player = self.player.sprite
		player.apply_gravity()
		collidable_sprites = self.terrain_sprites.sprites()

		for sprite in collidable_sprites:
			if sprite.rect.colliderect(player.rect):
				if player.direction.y > 0:
					player.rect.bottom = sprite.rect.top
					player.direction.y = 0
					player.on_ground = True
				elif player.direction.y < 0:
					player.rect.top = sprite.rect.bottom
					player.direction.y = 0
					player.on_ceiling = True

		if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
			player.on_ground = False
		if player.on_ceiling and player.direction.y > 0.1:
			player.on_ceiling = False

	def scroll_x(self):
		"""This function controls the side-scrolling feature, getting influenced by the player position."""
		player = self.player.sprite
		player_x = player.rect.centerx
		direction_x = player.direction.x

		if player_x < screen_width / 4 and direction_x < 0:
			self.world_shift = 10
			player.speed = 0
		elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
			self.world_shift = -10
			player.speed = 0
		else:
			self.world_shift = 0
			player.speed = 10

	def collection(self):
		"""This function controls the chest collection feature."""
		keys = [(160, 60), (290, 60), (500, 60), (580, 60), (680, 60), (900, 60)]
		move = 400
		words = [pygame.transform.scale(pygame.image.load("../graphics/nice.png"), (113, 29)), pygame.transform.scale(pygame.image.load("../graphics/weather.png"), (200, 29)), pygame.transform.scale(pygame.image.load("../graphics/we.png"), (59, 29)), pygame.transform.scale(pygame.image.load("../graphics/are.png"), (86, 29)), pygame.transform.scale(pygame.image.load("../graphics/having.png"), (193, 29)), pygame.transform.scale(pygame.image.load("../graphics/right_q.png"), (168, 29))]
		chest_collisions = pygame.sprite.spritecollide(self.player.sprite, self.chest_sprites, True)
		index = -len(self.chest_sprites.sprites()) - 1
		for chest in chest_collisions:
			self.collected_words[keys[index]] = words[index]

	def check_death(self):
		"""This function controls the next steps after the player falls."""
		if self.player.sprite.rect.top > screen_height:
			self.collected_words = {}
			self.speaker_on = False
			with open("respawn3.py") as f:
				exec(f.read())

	def draw_subtitle(self):
		"""This function draws a subtitle at the top of the game screen."""
		level1_list = [Key("L"), Key("E"), Key("V"), Key("E"), Key("L"), Key("3")]
		level1_coordinates = {
			(520, 20): level1_list[0],
			(545, 20): level1_list[1],
			(570, 20): level1_list[2],
			(595, 20): level1_list[3],
			(620, 20): level1_list[4],
			(665, 20): level1_list[5]
		}
		return level1_list, level1_coordinates

	def draw_dialogue(self):
		"""This function draws the sound icon when needed."""
		sprite_sheet = pygame.image.load("../graphics/icons/sound.png")
		surface = pygame.Surface((30, 31), pygame.SRCALPHA)
		rect = pygame.Rect(0, 0, 30, 31)
		surface.blit(sprite_sheet, (0, 0), rect)

		return pygame.transform.scale(surface, (75, 77.5))

	def run(self):
		"""This function runs the level."""
		self.terrain_sprites.draw(self.display_surface)
		self.terrain_sprites.update(self.world_shift)

		self.grass_sprites.update(self.world_shift)
		self.grass_sprites.draw(self.display_surface)

		self.chest_sprites.update(self.world_shift)
		self.chest_sprites.draw(self.display_surface)

		self.check_death()
		self.collection()

		self.player.update()
		self.horizontal_movement_collision()
		self.vertical_movement_collision()
		self.scroll_x()
		self.player.draw(self.display_surface)
		self.goal.update(self.world_shift)
		self.goal.draw(self.display_surface)

		# drawings
		gfxdraw.box(self.display_surface, pygame.Rect(0, 0, screen_width, screen_height / 7), (40, 41, 41, 200))
		level1_list, level1_coordinates = self.draw_subtitle()
		for key, item in level1_coordinates.items():
			item.draw(key, self.display_surface)
		if len(self.collected_words) == 0:
			pass
		else:
			for key, item in self.collected_words.items():
				self.display_surface.blit(item, key)

		if len(self.chest_sprites.sprites()) == 0:
			self.speaker_on = True
			completed3 = True

		if self.speaker_on:
			megaphone = self.draw_dialogue()
			self.display_surface.blit(megaphone, (50, 10))

		if self.talk:
			keys = pygame.key.get_pressed()
			if keys[pygame.K_SPACE] and self.speaker_on:

				pygame.mixer.init()
				sentence3 = pygame.mixer.Sound("../audio/sentence3.wav")
				sentence3.play()
				self.speaker_on = False
				pygame.time.delay(3500)
				with open("end_screen.py") as f:
					exec(f.read())
