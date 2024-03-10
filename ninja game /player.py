import pygame
from support import import_folder, character_import
from math import sin


class Player(pygame.sprite.Sprite):
    # player class inherits from pygame sprite class and is used to create the player object
    def __init__(self, pos, surface, create_jump_particles, change_health):
        super().__init__()

        # character animations
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        # dust particles
        self.import_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.display_surface = surface
        self.create_jump_particles = create_jump_particles

        # player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16
        self.collision_rect = pygame.Rect(
            self.rect.topleft, (50, self.rect.height))

        # player status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

        # health management
        self.change_health = change_health
        self.invincible = False
        self.invincibility_duration = 500
        self.hurt_time = 0

        # audio
        self.jump_sound = pygame.mixer.Sound('audio/effects/jump.wav')
        self.jump_sound.set_volume(0.5)
        self.hit_sound = pygame.mixer.Sound('audio/effects/hit.wav')

    # import character assets function imports all the character animations and stores them in a dictionary
    def import_character_assets(self):
        character_path = 'graphics/character/'
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = character_import(full_path)

    # import dust run particles function imports all the dust particles and stores them in a list
    def import_dust_run_particles(self):
        self.dust_run_particles = import_folder(
            'graphics/character/dust_particles/run')

    # animation function is used to animate the character
    def animate(self):
        animation = self.animations[self.status]

        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # set image
        image = animation[int(self.frame_index)]
        # check if the player is facing right and if so set the image to the right of the player and vice versa
        if self.facing_right:
            self.image = image
            self.rect.bottomleft = self.collision_rect.bottomleft
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image
            self.rect.bottomright = self.collision_rect.bottomright

        # check if the player is invincible and if so change the alpha value of the image to create a flashing effect
        if self.invincible:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    # run dust animation function is used to animate the dust particles when the player is running
    def run_dust_animation(self):
        # check if the player is running and on the ground and if so animate the dust particles accordingly
        if self.status == 'run' and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            # loop over frame index if it is greater than the length of the list of dust particles
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0

            # blit the dust particles to the screen
            dust_particle = self.dust_run_particles[int(self.dust_frame_index)]

            # check if the player is facing right and if so blit the dust particles to the left of the player
            if self.facing_right:
                pos = self.rect.bottomleft - pygame.math.Vector2(6, 10)
                self.display_surface.blit(dust_particle, pos)
            # if the player is facing left then flip the dust particles and blit them to the right of the player
            else:
                pos = self.rect.bottomright - pygame.math.Vector2(6, 10)
                flipped_dust_particle = pygame.transform.flip(
                    dust_particle, True, False)
                self.display_surface.blit(flipped_dust_particle, pos)

    # get input function is used to get the input from the player and change the direction of the player accordingly
    def get_input(self):
        keys = pygame.key.get_pressed()

        # check if the player is pressing the right or left key and if so change the direction of the player accordingly
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        # check if the player is pressing the space key and if so make the player jump and create the jump particles at the bottom of the player and play the jump sound
        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()
            self.create_jump_particles(self.rect.midbottom)

    # get status function is used to get the status of the player and change the status accordingly based on the direction of the player
    def get_status(self):
        # check if the player is jumping or falling and if so change the status of the player accordingly
        if self.direction.y < 0:
            self.status = 'jump'
        # check if the player is falling and if so change the status of the player accordingly
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            # check if the player is running and if so change the status of the player accordingly
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    # apply gravity function is used to apply gravity to the player and change the direction of the player accordingly
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.collision_rect.y += self.direction.y

    # jump function is used to make the player jump and play the jump sound accordingly
    def jump(self):
        self.direction.y = self.jump_speed
        self.jump_sound.play()

    # get damage function is used to get the damage from the player and change the health of the player accordingly
    def get_damage(self):
        if not self.invincible:
            self.hit_sound.play()
            self.change_health(-10)
            self.invincible = True
            self.hurt_time = pygame.time.get_ticks()

    # change health function is used to change the health of the player and if the health of the player is less than or equal to 0 then change the status of the player to dead
    def invincibility_timer(self):
        # check if the player is invincible and if so change the status of the player accordingly
        if self.invincible:
            current_time = pygame.time.get_ticks()
            # check if the current time is greater than the time the player was hurt plus the invincibility duration and if so change the status of the player to not invincible
            if current_time - self.hurt_time >= self.invincibility_duration:
                self.invincible = False

    # wave value function is used to create a flashing effect when the player is invincible
    def wave_value(self):
        value = sin(pygame.time.get_ticks())

        # check if the value is greater than or equal to 0 and if so return 255 and if not return 0
        if value >= 0:
            return 255
        else:
            return 0

    # update function is used to update the player and change the status of the player accordingly
    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.run_dust_animation()
        self.invincibility_timer()
        self.wave_value()
