import pygame
from tiles import AnimatedTile, AnimatedTileEnemy
from random import randint


class Enemy(AnimatedTileEnemy):
    # class for the enemy object that inherits from the animated tile class and the animated tile enemy class and has the following attributes:
    def __init__(self, size, x, y):
        super().__init__(size, x, y, 'graphics/enemy/run')
        # size: the size of the enemy object
        self.rect.y += size - self.image.get_size()[1]

        # speed of the enemy object
        self.speed = randint(3, 5)

    # function to move the enemy object
    def move(self):
        self.rect.x += self.speed

    # function to reverse the image of the enemy object
    def reverse_image(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)

    #  function to reverse the direction of the enemy object
    def reverse(self):
        self.speed *= -1

    # function to update the enemy object
    def update(self, shift):
        self.rect.x += shift
        self.animate()
        self.move()
        self.reverse_image()
