import pygame
import sys
from settings import *
from level import Level
from overworld import Overworld
from ui import UI


class Game:
    # game attributes and user interface creation
    def __init__(self):

        # game attributes
        self.max_level = 2
        self.max_health = 100
        self.cur_health = 100
        self.coins = 0

        # audio
        self.level_bg_music = pygame.mixer.Sound('audio/level_music.wav')
        self.overworld_bg_music = pygame.mixer.Sound(
            'audio/overworld_music.wav')

        # overworld creation
        self.overworld = Overworld(
            0, self.max_level, screen, self.create_level)
        self.status = 'overworld'
        self.overworld_bg_music.play(loops=-1)

        # user interface
        self.ui = UI(screen)

    # level creation and overworld creation functions for the overworld class  to call
    def create_level(self, current_level):
        # create level object and set status to level
        self.level = Level(current_level, screen, self.create_overworld,
                           self.change_coins, self.change_health)

        # set the status to level and stop the overworld music and play the level music
        self.status = 'level'
        self.overworld_bg_music.stop()
        self.level_bg_music.play(loops=-1)

    # overworld creation function for the level class to call
    def create_overworld(self, current_level, new_max_level):
        # check  if the new max level is greater than the current max level and set the max level to the new max level
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        # create overworld object and set status to overworld
        self.overworld = Overworld(
            current_level, self.max_level, screen, self.create_level)
        self.status = 'overworld'

        # stop the level music and play the overworld music
        self.overworld_bg_music.play(loops=-1)
        self.level_bg_music.stop()

    # functions for the level class to call to change the coins and health
    def change_coins(self, amount):
        self.coins += amount

    # function for the level class to call to change the health
    def change_health(self, amount):
        self.cur_health += amount

    # function to check if the player has died
    def check_game_over(self):
        if self.cur_health <= 0:
            self.cur_health = 100
            self.coins = 0
            self.max_level = 0
            self.overworld = Overworld(
                0, self.max_level, screen, self.create_level)
            self.status = 'overworld'
            self.level_bg_music.stop()
            self.overworld_bg_music.play(loops=-1)

    # function to run the game
    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()
            self.ui.show_health(self.cur_health, self.max_health)
            self.ui.show_coins(self.coins)
            self.check_game_over()


# Pygame setup
pygame.init()

# game name
pygame.display.set_caption('Ninja Clash')

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('grey')
    game.run()

    pygame.display.update()
    clock.tick(60)
