import pygame
from pygame.locals import *
import button
import random

pygame.init()

# Display Screen Variables
screen_width = 640
screen_height = 750

# Define Font
font = pygame.font.SysFont('Futura', 60)

# Color Variables
white = (255, 255, 255)

# Bird Skins
skin1 = ('bird11')
skin2 = ('bird22')
skin3 = ('bird33')

# Game Variables
game_menu = 'game menu'
ground_scroll = 0
scroll_speed = 4
bird_flying = False
game_over = False
pipe_space = 160  # Can Increase Difficulty by Decreasing Pipe Space
pipe_freq = 1500  # milliseconds
last_pipe = pygame.time.get_ticks() - pipe_freq
score = 0
pipe_pass = False
current_skin = skin1


# Load Images
bg = pygame.image.load('bg.png')
ground = pygame.image.load('ground.png')

# Function for Displaying Pygame Screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

# Function for Printing Score on Screen


def draw_text(text, font, text_col,  x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Function for Resetting the Game


def reset_game(flappy_bird):
    pipe_group.empty()
    flappy_bird.rect.x = 100
    flappy_bird.rect.y = int(screen_height / 2)
    score = 0
    return score


# Function for Displaying Menu
def menu():
    global game_menu, screen_height, screen_width, bg, ground, current_skin, skin1, skin2, skin3

    # Load Button Images
    start_img = pygame.image.load('Start-button-sprite-3.png').convert_alpha()
    change_skin_img = pygame.image.load(
        'Start-button-sprite-2.png').convert_alpha()
    quit_img = pygame.image.load('Start-button-sprite(1).png').convert_alpha()

    # Create Button Instances
    start_button = button.Button(220, 250, start_img, 0.5)
    change_skin_button = button.Button(220, 350, change_skin_img, 0.5)
    quit_button = button.Button(220, 450, quit_img, 0.5)

    # Load Bird Skin
    bird_skin1_img = pygame.image.load('bird111.png').convert_alpha()
    bird_skin2_img = pygame.image.load('bird221.png').convert_alpha()
    bird_skin3_img = pygame.image.load('bird331.png').convert_alpha()

    # Create Instance of Bird Skin
    bird_skin1_button = button.Button(180, 350, bird_skin1_img, 1)
    bird_skin2_button = button.Button(280, 350, bird_skin2_img, 1)
    bird_skin3_button = button.Button(380, 350, bird_skin3_img, 1)

    run = True
    while run:

        # Draw Background
        screen.blit(bg, (0, 0))

        # Draw the ground and scroll
        screen.blit(ground, (0, 600))

        # Draw the start button
        if game_menu == 'game menu':
            if start_button.draw(screen):
                game_menu = 'start'
            if change_skin_button.draw(screen):
                game_menu = 'change skin'
            if quit_button.draw(screen):
                game_menu = 'quit'

        # Checks for Button Clicks (Which BUtton has been Clicked)
        if game_menu == 'start':
            playgame()
        if game_menu == 'quit':
            pygame.quit()
        if game_menu == 'change skin':
            screen.blit(bg, (0, 0))
            screen.blit(ground, (0, 600))

            if bird_skin1_button.draw(screen):
                print('bird skin 1')
                current_skin = skin1
                game_menu = 'game menu'

            if bird_skin2_button.draw(screen):
                print('bird skin 2')
                current_skin = skin2
                game_menu = 'game menu'

            if bird_skin3_button.draw(screen):
                print('bird skin 3')
                current_skin = skin3
                game_menu = 'game menu'

        # checking for a particular event during the game
        for event in pygame.event.get():
            # if the event is quit, then quit the game
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f'{current_skin + str(num)}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):

        # Gravity
        if bird_flying == True:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 600:
                self.rect.y += int(self.vel)

        if game_over == False:
            # Jump
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            # Handle the Animation
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            # Rotate the bird
            if bird_flying == True:
                self.image = pygame.transform.rotate(
                    self.images[self.index], self.vel * -2)

        else:
            self.image = pygame.transform.rotate(
                self.images[self.index], -90)


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('pipe.png')
        self.rect = self.image.get_rect()
        # Position 1 is from the top, -1 is from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_space / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_space / 2)]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()


bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()


# Load Button Images
restart_button_img = pygame.image.load('restart.png').convert_alpha()
quit_button_img = pygame.image.load(
    'Start-button-sprite(1) copy.png').convert_alpha()


# Create Button Instances
restart_button = button.Button(250, 250, restart_button_img, 1)
quit_button = button.Button(250, 350, quit_button_img, 1)


def playgame():

    global ground_scroll, scroll_speed, screen_height, screen_width, bg, ground, game_menu, bird_flying, game_over, pipe_freq, last_pipe, score, pipe_pass

    clock = pygame.time.Clock()

    # Speed of the game (Increase to make game faster and Difficult)
    fps = 60

    # Creating Bird
    flappy_bird = Bird(100, int(screen_height/2))
    bird_group.add(flappy_bird)

    # Display Screen
    run = True
    while run:

        clock.tick(fps)

        # Draw Background
        screen.blit(bg, (0, 0))

        # Draw the Bird and Pipe
        bird_group.draw(screen)
        bird_group.update()
        pipe_group.draw(screen)

        # Draw the ground and scroll
        screen.blit(ground, (ground_scroll, 600))

        # Check for Score
        if len(pipe_group) > 0:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
                    and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
                    and pipe_pass == False:
                pipe_pass = True

            if pipe_pass == True:
                if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                    score += 1
                    pipe_pass = False

        #  Printing Score on the Screen
        draw_text(str(score), font, white, int(screen_width / 2), 20)

        # Check if bird has hit the pipe
        if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy_bird.rect.top < 0:
            game_over = True

        # check if bird has hit the ground
        if flappy_bird.rect.bottom >= 600:
            game_over = True
            bird_flying = False

        # Draw the ground and scroll
        if game_over == False and bird_flying == True:

            # Generate new pipes
            time_now = pygame.time.get_ticks()
            if time_now - last_pipe > pipe_freq:
                pipe_height = random.randint(-100, 100)
                top_pipe = Pipe(screen_width, int(
                    screen_height/2) + pipe_height, 1)
                bottom_pipe = Pipe(screen_width, int(
                    screen_height/2) + pipe_height, -1)
                pipe_group.add(bottom_pipe)
                pipe_group.add(top_pipe)
                last_pipe = time_now

            ground_scroll -= scroll_speed
            if abs(ground_scroll) > 30:
                ground_scroll = 0

            pipe_group.update()

        # check for game over and restart
        if game_over == True:
            if restart_button.draw(screen):
                game_over = False
                score = reset_game(flappy_bird)
            if quit_button.draw(screen):
                pygame.quit()

        # checking for a particular event during the game
        for event in pygame.event.get():
            # if the event is quit, then quit the game
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and bird_flying == False and game_over == False:
                bird_flying = True

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    menu()
