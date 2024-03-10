import pygame
from support import import_folder


class ParticleEffect(pygame.sprite.Sprite):
    # This class is used to create particle effects for the player and enemies when they jump, land, or are hit by a bullet. It is also used to create the explosion effect when an enemy dies.
    def __init__(self, pos, type):
        super().__init__()
        self.frame_index = 0
        self.animation_speed = 0.5
        # This line of code is used to check what type of particle effect is being created. Depending on the type, the frames list is set to the correct folder.
        if type == 'jump':
            self.frames = import_folder(
                'graphics/character/dust_particles/jump')
        if type == 'land':
            self.frames = import_folder(
                'graphics/character/dust_particles/land')
        if type == 'explosion':
            self.frames = import_folder('graphics/enemy/explosion')

        # This line of code is used to set the image and rect attributes of the particle effect.
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    # This method is used to animate the particle effect.
    def animate(self):
        #  This line of code is used to increase the frame index by the animation speed.
        self.frame_index += self.animation_speed
        # This line of code is used to check if the frame index is greater than the length of the frames list. If it is, the particle effect is killed.
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    # This method is used to update the particle effect. It is called in the main game loop.
    def update(self, x_shift):
        self.animate()
        self.rect.x += x_shift
