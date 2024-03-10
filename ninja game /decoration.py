from settings import vertical_tile_number, tile_size, screen_width
import pygame
from tiles import AnimatedTile


class Sky:
    # class for the sky object that has the following attributes: horizon, style  and has the following methods: __init__, draw
    def __init__(self, horizon, style='level'):
        self.top = pygame.image.load(
            'graphics/decoration/sky/sky_top.png').convert()
        self.bottom = pygame.image.load(
            'graphics/decoration/sky/sky_bottom.png').convert()
        self.middle = pygame.image.load(
            'graphics/decoration/sky/sky_middle.png').convert()
        self.horizon = horizon

        # stretch the sky to the screen size and horizon height if the style is level
        self.top = pygame.transform.scale(self.top, (screen_width, tile_size))
        self.bottom = pygame.transform.scale(
            self.bottom, (screen_width, tile_size))
        self.middle = pygame.transform.scale(
            self.middle, (screen_width, tile_size))

    # function to draw the sky object on the screen
    def draw(self, surface):
        for row in range(vertical_tile_number):
            y = row * tile_size
            if row < self.horizon:
                surface.blit(self.top, (0, y))
            elif row == self.horizon:
                surface.blit(self.middle, (0, y))
            else:
                surface.blit(self.bottom, (0, y))


class Water:
    # class for the water object that has the following attributes: water_sprites and has the following methods: __init__, draw
    def __init__(self, top, level_width):
        water_start = -screen_width
        water_tile_width = 192
        # calculate the amount of water tiles needed to fill the screen and add a few more for the scrolling effect
        tile_x_amount = int(
            (level_width + screen_width * 2) / water_tile_width)
        self.water_sprites = pygame.sprite.Group()

        # create the water tiles and add them to the water_sprites group making sure that the water tiles are placed correctly
        for tile in range(tile_x_amount):
            x = tile * water_tile_width + water_start
            y = top
            sprite = AnimatedTile(192, x, y, 'graphics/decoration/water')
            self.water_sprites.add(sprite)

    # function to draw the water object on the screen
    def draw(self, surface, shift):
        self.water_sprites.update(shift)
        self.water_sprites.draw(surface)
