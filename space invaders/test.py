import pygame
import math
import random
import time
from pygame.locals import *

pygame.init()

# set up the display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# load images
bg = pygame.image.load("starbg.png")
player = pygame.image.load("ship_3.png")
powerup = pygame.image.load("shield.png")
meteor = pygame.image.load("meteor.png")
coin = pygame.image.load("coin.png")
weapon = pygame.image.load("weapon.png")

# change the size of the coin image
coin = pygame.transform.scale(coin, (50, 50))
weapon = pygame.transform.scale(weapon, (50, 50))
powerup = pygame.transform.scale(powerup, (50, 50))
player = pygame.transform.scale(player, (60, 60))

# load sounds
shoot_sound = pygame.mixer.Sound("shoot.wav")
asteriods_sound = pygame.mixer.Sound("bangSmall.wav")
powerup_sound = pygame.mixer.Sound("bangLarge.wav")

# game name and window
pygame.display.set_caption("Space Invaders")
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


# game constants
game_over = False
lives = 3
score = 0
sheild = False
weapon_check = False
sheild_timer = 0
weapon_timer = 0
highscore = 0
is_sound_on = True

# read highscore from file
with open("highscore.txt", "r") as f:
    highscore = f.read()
    highscore = int(highscore)


# GameObject class for which other classes will inherit from and should have all relationships implementation
class GameObject(object):
    """ 

    The game object class is the parent class for all other classes in the game. 
    It contains the basic attributes and methods that all other classes will inherit from.

    """

    # constructor
    def __init__(self, x, y, img=None):
        self.img = img
        self.x = x
        self.y = y
        if img is not None:
            self.width = self.img.get_width()
            self.height = self.img.get_height()

    # draw method
    def draw(self, win):
        win.blit(self.img, (self.x, self.y))


# Player class which inherits from GameObject class
class Player(GameObject):
    """

    The player class inherits from the GameObject class and contains all the attributes and 
    methods that the player will have.

    """

    # constructor
    def __init__(self, x, y, img=None):
        super().__init__(x, y, img)
        self.width = self.img.get_width()
        self.height = self.img.get_height()

        # set the angle of the player to 0 degrees initially
        self.angle = 0

        # rotate the image to the angle of the player
        self.rotate_angle = pygame.transform.rotate(self.img, self.angle)

        # get the rectangle of the rotated image
        self.rotate_angle_rect = self.rotate_angle.get_rect(
            center=(self.x, self.y))

        # get the cosine and sine of the angle of the player
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))

        # get the head of the player
        self.head = (self.x + self.cosine * 50, self.y + self.sine * 50)

    # draw method

    def draw(self, win):
        win.blit(self.rotate_angle, self.rotate_angle_rect)

    # rotate method
    def rotate(self):

        # rotate the image to the angle of the player
        self.rotate_angle = pygame.transform.rotate(self.img, self.angle)

        # get the rectangle of the rotated image
        self.rotate_angle_rect = self.rotate_angle.get_rect(
            center=(self.x, self.y))

        # get the cosine and sine of the angle of the player
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))

        # get the head of the player
        self.head = (self.x + self.cosine * 50, self.y + self.sine * 50)

    # move method
    def move(self):

        # get the keys pressed
        keys = pygame.key.get_pressed()

        # move the player based on the keys pressed
        if keys[pygame.K_LEFT]:
            self.angle += 1
            self.rotate()
        if keys[pygame.K_RIGHT]:
            self.angle -= 1
            self.rotate()
        if keys[pygame.K_UP]:
            self.x += self.cosine * 5
            self.y -= self.sine * 5
            self.rotate()
        if keys[pygame.K_DOWN]:
            self.x -= self.cosine * 5
            self.y += self.sine * 5
            self.rotate()

    # check if player is off screen

    def check_off_screen(self):
        if self.x < 0:
            self.x = SCREEN_WIDTH
        if self.x > SCREEN_WIDTH:
            self.x = 0
        if self.y < 0:
            self.y = SCREEN_HEIGHT
        if self.y > SCREEN_HEIGHT:
            self.y = 0


# Bullet class which inherits from GameObject class
class Bullet(GameObject):
    """ 

    The bullet class inherits from the GameObject class and contains all the attributes and
    methods that the bullet will have.

    """

    # constructor
    def __init__(self):
        super().__init__(player.head[0], player.head[1])

        # bullet direction it should shoot from the player head
        self.x = player.head[0]
        self.y = player.head[1]

        # bullet width and height
        self.width = 5
        self.height = 5

        # bullet cosine and sine where it should shoot from the player head
        self.bullet_cosine = player.cosine
        self.bullet_sine = player.sine

        # bullet speed
        self.bullet_speed = (self.bullet_cosine * 10, self.bullet_sine * 10)

    # move method
    def move(self):
        self.x += self.bullet_speed[0]
        self.y -= self.bullet_speed[1]

    # draw method
    def draw(self, win):
        pygame.draw.rect(win, (255, 0, 0),
                         (self.x, self.y, self.width, self.height))

    # check if bullet is off screen

    def check_off_screen(self):
        if self.x < 0 or self.x > SCREEN_WIDTH or self.y < 0 or self.y > SCREEN_HEIGHT:
            return True
        else:
            return False


# Powerup class which inherits from GameObject class
class Powerup(GameObject):
    """

    The powerup class inherits from the GameObject class and contains all the attributes and
    methods that the powerup will have.

    """

    # constructor
    def __init__(self, x, y, img=None):
        super().__init__(x, y, img)
        self.width = 50
        self.height = 50

        # powerup direction it should move randomly
        if self.x < SCREEN_WIDTH // 2:
            self.xdir = 1
        else:
            self.xdir = -1

        if self.y < SCREEN_HEIGHT // 2:
            self.ydir = 1
        else:
            self.ydir = -1

        # powerup velocity
        self.velocity = (self.xdir * random.randint(1, 5),
                         self.ydir * random.randint(1, 5))

    # move method
    def draw(self, win):
        win.blit(powerup, (self.x, self.y))


class Asteroid(GameObject):
    """ 

    The asteroid class inherits from the GameObject class and contains all the attributes and
    methods that the asteroid will have.

    """

    # constructor
    def __init__(self, x, y, img=None):
        super().__init__(x, y, img)
        self.width = 50
        self.height = 50

        # asteroid direction it should move randomly
        if self.x < SCREEN_WIDTH // 2:
            self.xdir = 1
        else:
            self.xdir = -1

        if self.y < SCREEN_HEIGHT // 2:
            self.ydir = 1
        else:
            self.ydir = -1

        # asteroid velocity
        self.velocity = (self.xdir * random.randint(1, 5),
                         self.ydir * random.randint(1, 5))

    # move method

    def draw(self, win):
        win.blit(meteor, (self.x, self.y))


# class for health bar
class HealthBar(GameObject):
    """ 

    The health bar class inherits from the GameObject class and contains all the attributes and
    methods that the health bar will have.

    """

    # constructor
    def __init__(self, x, y, img=None):
        super().__init__(x, y, img)

        # health bar width and height
        self.width = 150
        self.height = 20

        # health bar color
        self.max_health = 100
        self.health = self.max_health
        self.color = (0, 255, 0)

    # draw method
    def draw(self, win):
        pygame.draw.rect(win, (255, 255, 255), (self.x - 2,
                         self.y - 2, self.width + 4, self.height + 4))
        pygame.draw.rect(win, (0, 0, 0), (self.x - 1, self.y -
                         1, self.width + 2, self.height + 2))
        pygame.draw.rect(win, self.color, (self.x, self.y, int(
            self.width * self.health / self.max_health), self.height))

    # decrease health method
    def decrease_health(self):
        self.health -= 1
        if self.health <= 0:
            self.health = self.max_health
            return True
        return False

    # increase health method
    def increase_health(self):
        self.health += 1
        if self.health >= 100:
            self.health = self.max_health
            return True
        return False


class Coin(GameObject):
    def __init__(self, x, y, img=None):
        super().__init__(x, y, img)
        self.width = 50
        self.height = 50

        # powerup direction it should move randomly
        if self.x < SCREEN_WIDTH // 2:
            self.xdir = 1
        else:
            self.xdir = -1

        if self.y < SCREEN_HEIGHT // 2:
            self.ydir = 1
        else:
            self.ydir = -1

        # powerup velocity
        self.velocity = (self.xdir * random.randint(1, 5),
                         self.ydir * random.randint(1, 5))

    def draw(self, win):
        win.blit(coin, (self.x, self.y))


class Weapon(GameObject):
    def __init__(self, x, y, img=None):
        super().__init__(x, y, img)
        self.width = 50
        self.height = 50

        # powerup direction it should move randomly
        if self.x < SCREEN_WIDTH // 2:
            self.xdir = 1
        else:
            self.xdir = -1

        if self.y < SCREEN_HEIGHT // 2:
            self.ydir = 1
        else:
            self.ydir = -1

        # powerup velocity
        self.velocity = (self.xdir * random.randint(1, 5),
                         self.ydir * random.randint(1, 5))

    def draw(self, win):
        win.blit(weapon, (self.x, self.y))


def main():
    """ 

    The main function contains the main game loop and all the game logic.

    """

    # global variables
    global lives, game_over, score, sheild, sheild_timer, highscore, weapon_check, weapon_timer

    # initialize pygame and create window
    win.blit(bg, (0, 0))

    # Initializing Text
    font = pygame.font.SysFont("comicsans", 30, True)
    text = font.render("Lives: " + str(lives), 1, (255, 255, 255))
    playagain = font.render(
        "Play Again. Press S to Resatrt", 1, (255, 255, 255))
    scoretext = font.render("Score: " + str(score), 1, (255, 255, 255))
    highscoretext = font.render(
        "High Score: " + str(highscore), 1, (255, 255, 255))

    # draw player
    player.draw(win)

    # shoot bullets
    for bullet in player_bullets:
        bullet.draw(win)
        bullet.move()

    # draw powerups
    for s in stars:
        s.draw(win)
        s.x += s.velocity[0]
        s.y += s.velocity[1]

    # draw weapons
    for w in weapons:
        w.draw(win)
        w.x += w.velocity[0]
        w.y += w.velocity[1]

        # if player collides with the weapon powerup
        if player.x < w.x + w.width and player.x + player.width > w.x and player.y < w.y + w.height and player.y + player.height > w.y:
            weapon_check = True
            weapons.pop(weapons.index(w))
            break

    # draw coins
    for coin in coins:
        coin.draw(win)
        coin.x += coin.velocity[0]
        coin.y += coin.velocity[1]

        # check if the coin goes out of the screen
        if coin.x < 0 or coin.x > SCREEN_WIDTH or coin.y < 0 or coin.y > SCREEN_HEIGHT:
            coins.pop(coins.index(coin))
            break

        # check if the player collides with the coin powerup
        if player.x < coin.x + coin.width and player.x + player.width > coin.x and player.y < coin.y + coin.height and player.y + player.height > coin.y:
            coins.pop(coins.index(coin))
            score += 10
            break

    # draw asteriods
    for asteriod in asteriods:
        asteriod.draw(win)
        asteriod.x += asteriod.velocity[0]
        asteriod.y += asteriod.velocity[1]

        # asteriod collision with player
        if asteriod.x < player.x + player.width and asteriod.x + asteriod.width > player.x and asteriod.y < player.y + player.height and asteriod.y + asteriod.height > player.y:
            # check if the player has sheild
            if sheild:
                if health_bar.increase_health():
                    # 2000 is the time the sheild will last
                    if sheild_timer > 2000:
                        sheild = False
                        sheild_timer = 0

            # if the player does not have sheild then decrease health and check if the player has lives left
            else:
                # decrease health
                if health_bar.decrease_health():
                    lives -= 1
                    asteriods.pop(asteriods.index(asteriod))
                    health_bar.health = health_bar.max_health
                    if lives == 0:
                        game_over = True
                        if score > highscore:
                            highscore = score
                        win.blit(playagain, (SCREEN_WIDTH // 2 -
                                 200, SCREEN_HEIGHT // 2 - 50))
                        pygame.display.update()
                        pygame.time.delay(2000)
                        main()
                        break

        # bullet collision with asteriod and increase score if the bullet collides with the asteriod and remove the asteriod and bullet
        for bullet in player_bullets:
            if bullet.x < asteriod.x + asteriod.width and bullet.x + bullet.width > asteriod.x and bullet.y < asteriod.y + asteriod.height and bullet.y + bullet.height > asteriod.y:
                score += 5
                asteriods_sound.play()
                asteriods.pop(asteriods.index(asteriod))
                player_bullets.pop(player_bullets.index(bullet))
                break

        # check if the star is off screen and remove it from the list of stars if it is off screen
        for s in stars:
            if s.x < 0 or s.x > SCREEN_WIDTH or s.y < 0 or s.y > SCREEN_HEIGHT:
                stars.pop(stars.index(s))
                break
            if player.x < s.x + s.width and player.x + player.width > s.x and player.y < s.y + s.height and player.y + player.height > s.y:
                score += 1
                powerup_sound.play()
                stars.pop(stars.index(s))
                sheild = True
                break

        # check if the lives are 0 and if they are then end the game
        if lives <= 0:
            game_over = True

            # save highscore
            if score > highscore:
                highscore = score
                with open("highscore.txt", "w") as f:
                    f.write(str(highscore))

            break

        # draw sheild around player
        if sheild:
            # draw circle around player
            pygame.draw.circle(win, (255, 255, 255), (player.x + player.width // 2,
                                                      player.y + player.height // 2), 50, 2)

        if weapon_check:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    # shoot bullets
                    player_bullets.append(Bullet())
                    shoot_sound.play()
                    if weapon_timer > 2000:
                        weapon_check = False
                        weapon_timer = 0

    # print game over text if the game is over
    if game_over:
        win.blit(playagain, (SCREEN_WIDTH//2 - playagain.get_width() // 2,
                             SCREEN_HEIGHT//2 - playagain.get_height() // 2))

    # draw health bar on screen
    health_bar.draw(win)

    # draw text on screen
    win.blit(text, (10, 10))
    win.blit(scoretext, (SCREEN_WIDTH - scoretext.get_width() - 10, 10))
    win.blit(highscoretext, (SCREEN_WIDTH - highscoretext.get_width() - 10, 40))
    pygame.display.update()


# game variables
player = Player(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, player)
health_bar = HealthBar(SCREEN_WIDTH//2 - 100, 30)
player_bullets = []
asteriods = []
stars = []
coins = []
weapons = []
count = 0
run = True

# game loop
while run:

    # set fps
    clock.tick(60)

    # flag to draw asteriods and stars on screen if the game is not over and increase count by 1
    count += 1

    if not game_over:
        sheild_timer += 1
        weapon_timer += 1

        # random axis to spawn asteriods and stars
        random_point = (random.randint(0, SCREEN_WIDTH),
                        random.randint(0, SCREEN_HEIGHT))

        if count % 50 == 0:
            asteriods.append(
                Asteroid(random_point[0], random_point[1], meteor))

        # random axis to spawn asteriods and stars
        random_point = (random.randint(0, SCREEN_WIDTH),
                        random.randint(0, SCREEN_HEIGHT))

        if count % 100 == 0:
            coins.append(Coin(random_point[0], random_point[1], coin))

        if count % 200 == 0:
            weapons.append(Weapon(random_point[0], random_point[1], weapon))

        # random axis to spawn asteriods and stars
        random_point = (random.randint(0, SCREEN_WIDTH),
                        random.randint(0, SCREEN_HEIGHT))

        if count % 500 == 0:
            stars.append(Powerup(random_point[0], random_point[1], powerup))

        # check if the player is off screen
        player.check_off_screen()

        # check if the player bullets are off screen and remove them from the list of bullets if they are off screen
        if len(player_bullets) > 0:
            for bullet in player_bullets:
                if bullet.check_off_screen():
                    player_bullets.pop(player_bullets.index(bullet))

        # move the player as the user presses the arrow keys
        player.move()

    # loop through all the events
    for event in pygame.event.get():
        # check if the user wants to quit the game
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            game_over = False
            lives = 3
            player_bullets = []
            asteriods = []
            count = 0
            score = 0
        # check if the user presses the m key and if the game is not over then toggle the sound
        if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
            is_sound_on = not is_sound_on

    main()

pygame.quit()