import pygame
from support import import_folder, character_import


class Tile(pygame.sprite.Sprite):

    """

    Base class for all tiles. Tile is a sprite that can be added to a group. 
    Tiles are used to create the level. 

    """

    def __init__(self, size, x, y):
        super().__init__()

        # Creates a surface for the tile and sets the rect attribute to the surface's rect
        self.image = pygame.Surface((size, size))

        # Sets the rect attribute to the surface's rect
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, shift):
        # Shifts the tile to the left by the amount specified in the shift parameter
        self.rect.x += shift


class StaticTile(Tile):
    """

    Base class for all static tiles. Static tiles are tiles that do not move.

    """

    def __init__(self, size, x, y, surface):

        # Calls the parent class's constructor method and passes the size, x, and y parameters to it
        super().__init__(size, x, y)

        # Sets the image attribute to the surface parameter
        self.image = surface


class Crate(StaticTile):
    """ 

    Crate tile. Class for the crate tile. Crate tiles are static tiles that do not move.

    """

    def __init__(self, size, x, y):
        # Calls the parent class's constructor method and passes the size, x, and y parameters to it
        super().__init__(size, x, y, pygame.image.load(
            'graphics/terrain/crate.png').convert_alpha())

        # offset_y is the y coordinate of the bottom of the crate
        offset_y = y + size

        # Sets the rect attribute to the surface's rect
        self.rect = self.image.get_rect(bottomleft=(x, offset_y))


class AnimatedTile(Tile):
    """ 

    Animated tile. Class for animated tiles. Animated tiles are tiles that move.

    """

    def __init__(self, size, x, y, path):

        # Calls the parent class's constructor method and passes the size, x, and y parameters to it
        super().__init__(size, x, y)

        # Sets the frames attribute to a list of surfaces
        self.frames = import_folder(path)
        self.frame_index = 0

        # Sets the image attribute to the first surface in the frames list
        self.image = self.frames[self.frame_index]

    def animate(self):

        # Increments the frame_index attribute by 0.15 and sets the image attribute to the surface at the frame_index position in the frames list
        self.frame_index += 0.15

        # If the frame_index attribute is greater than or equal to the length of the frames list, set the frame_index attribute to 0
        if self.frame_index >= len(self.frames):
            self.frame_index = 0

        # Sets the image attribute to the surface at the frame_index position in the frames list
        self.image = self.frames[int(self.frame_index)]

    def update(self, shift):

        # animates the tile and shifts it to the left by the amount specified in the shift parameter
        self.animate()
        self.rect.x += shift


class AnimatedTileEnemy(Tile):
    """ 

    Animated tile. Class for animated tiles. Animated tiles are tiles that move.

    """

    def __init__(self, size, x, y, path):

        # Calls the parent class's constructor method and passes the size, x, and y parameters to it
        super().__init__(size, x, y)

        # Sets the frames attribute to a list of surfaces
        self.frames = character_import(path)
        self.frame_index = 0

        # Sets the image attribute to the first surface in the frames list
        self.image = self.frames[self.frame_index]

    def animate(self):

        # Increments the frame_index attribute by 0.15 and sets the image attribute to the surface at the frame_index position in the frames list
        self.frame_index += 0.15

        # If the frame_index attribute is greater than or equal to the length of the frames list, set the frame_index attribute to 0
        if self.frame_index >= len(self.frames):
            self.frame_index = 0

        # Sets the image attribute to the surface at the frame_index position in the frames list
        self.image = self.frames[int(self.frame_index)]

    def update(self, shift):

        # animates the tile and shifts it to the left by the amount specified in the shift parameter
        self.animate()
        self.rect.x += shift


class Coin(AnimatedTile):
    """ 

    Coin tile. Class for the coin tile. Coin tiles are animated tiles that move. 

    """

    def __init__(self, size, x, y, path, value):
        # Calls the parent class's constructor method and passes the size, x, and y parameters to it
        super().__init__(size, x, y, path)

        # center_x is the x coordinate of the center of the coin
        center_x = x + int(size / 2)

        # center_y is the y coordinate of the center of the coin
        center_y = y + int(size / 2)

        # Sets the rect attribute to the surface's rect
        self.rect = self.image.get_rect(center=(center_x, center_y))

        # Sets the value attribute to the value parameter
        self.value = value


class Palm(AnimatedTile):
    """ 

    Palm tile. Class for the palm tile. Palm tiles are animated tiles that move. 

    """

    def __init__(self, size, x, y, path, offset):
        # Calls the parent class's constructor method and passes the size, x, and y parameters to it
        super().__init__(size, x, y, path)

        # offset_y is the y coordinate of the bottom of the palm
        offset_y = y - offset

        # Sets the rect attribute to the surface's rect
        self.rect.topleft = (x, offset_y)
