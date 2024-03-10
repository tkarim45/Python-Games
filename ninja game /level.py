import pygame
from support import import_csv_layout, import_cut_graphics
from settings import tile_size, screen_height, screen_width
from tiles import Tile, StaticTile, Crate, Coin
from enemy import Enemy
from decoration import Sky, Water
from player import Player
from particles import ParticleEffect
from game_data import levels


class Level:
    # initialize the level class and set up the level and the player
    def __init__(self, current_level, surface, create_overworld, change_coins, change_health):
        # general setup
        self.display_surface = surface
        self.world_shift = 0
        self.current_x = None

        # audio
        self.coin_sound = pygame.mixer.Sound('audio/effects/coin.wav')
        self.stomp_sound = pygame.mixer.Sound('audio/effects/stomp.wav')

        # overworld connection
        self.create_overworld = create_overworld
        self.current_level = current_level
        level_data = levels[self.current_level]
        self.new_max_level = level_data['unlock']

        # player
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout, change_health)

        # user interface
        self.change_coins = change_coins

        # dust
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

        # explosion particles
        self.explosion_sprites = pygame.sprite.Group()

        # terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(
            terrain_layout, 'terrain')

        # grass setup
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')

        # crates
        crate_layout = import_csv_layout(level_data['crates'])
        self.crate_sprites = self.create_tile_group(crate_layout, 'crates')

        # coins
        coin_layout = import_csv_layout(level_data['coins'])
        self.coin_sprites = self.create_tile_group(coin_layout, 'coins')

        # enemy
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')

        # constraint
        constraint_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(
            constraint_layout, 'constraint')

        # decoration
        self.sky = Sky(8)
        level_width = len(terrain_layout[0]) * tile_size
        self.water = Water(screen_height - 20, level_width)

    # create tile group method to create the tile groups
    def create_tile_group(self, layout, type):
        # create a sprite group
        sprite_group = pygame.sprite.Group()

        # loop through the layout and create the tiles
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                # only create a tile if the value is not -1
                if val != '-1':
                    # calculate the x and y position of the tile
                    x = col_index * tile_size
                    y = row_index * tile_size

                    # create the terrain based on the type of tile it is
                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics(
                            'graphics/terrain/terrain_tiles.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    # create the grass based on the type of tile it is
                    if type == 'grass':
                        grass_tile_list = import_cut_graphics(
                            'graphics/decoration/grass/grass.png')
                        tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    # create the crates based on the type of tile it is
                    if type == 'crates':
                        sprite = Crate(tile_size, x, y)

                    # create the coin based on the type of tile it is
                    if type == 'coins':
                        # create the gold coin if the value is 0
                        if val == '0':
                            sprite = Coin(tile_size, x, y,
                                          'graphics/coins/gold', 5)

                        # create the silver coin if the value is 1
                        if val == '1':
                            sprite = Coin(tile_size, x, y,
                                          'graphics/coins/silver', 1)

                    # create enemies if the type is set to enemies
                    if type == 'enemies':
                        sprite = Enemy(tile_size, x, y)

                    # create constraints if the type is set to constraints
                    if type == 'constraint':
                        sprite = Tile(tile_size, x, y)

                    # add the sprite to the sprite group
                    sprite_group.add(sprite)

        # return the sprite group
        return sprite_group

    # player setup method to set up the player
    def player_setup(self, layout, change_health):
        # loop through the layout and create the player
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                # calculate the x and y position of the tile
                x = col_index * tile_size
                y = row_index * tile_size
                # create the player if the value is 0
                if val == '0':
                    sprite = Player((x, y), self.display_surface,
                                    self.create_jump_particles, change_health)
                    self.player.add(sprite)
                # create the goal if the value is 1
                if val == '1':
                    hat_surface = pygame.image.load(
                        'graphics/character/hat.png').convert_alpha()
                    # create the sprite and add it to the sprite group
                    sprite = StaticTile(tile_size, x, y, hat_surface)
                    self.goal.add(sprite)

    # enemy collision method to check if the player has collided with an enemy
    def enemy_collision_reverse(self):
        # loop through the enemy sprites and check if the player has collided with them
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse()

    # create jump particles method to create the jump particles
    def create_jump_particles(self, pos):
        # create the jump particles
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10, 5)
        else:
            pos += pygame.math.Vector2(10, -5)

        #  create the jump particle sprite and add it to the sprite group
        jump_particle_sprite = ParticleEffect(pos, 'jump')
        self.dust_sprite.add(jump_particle_sprite)

    # horizontal movement collision method to check if the player has collided with a tile horizontally
    def horizontal_movement_collision(self):
        # get the player sprite
        player = self.player.sprite
        # set the collision rect to the player rect
        player.collision_rect.x += player.direction.x * player.speed
        # get the collidable sprites
        collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites()
        # loop through the collidable sprites and check if the player has collided with them
        for sprite in collidable_sprites:
            # check if the player has collided with the sprite
            if sprite.rect.colliderect(player.collision_rect):
                # check if the player is moving left or right
                if player.direction.x < 0:
                    player.collision_rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.collision_rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

    # vertical movement collision method to check if the player has collided with a tile vertically
    def vertical_movement_collision(self):
        # get the player sprite
        player = self.player.sprite
        # set the collision rect to the player rect
        player.apply_gravity()
        # get the collidable sprites
        collidable_sprites = self.terrain_sprites.sprites(
        ) + self.crate_sprites.sprites()

        # loop through the collidable sprites and check if the player has collided with them
        for sprite in collidable_sprites:
            # check if the player has collided with the sprite
            if sprite.rect.colliderect(player.collision_rect):
                # check if the player is moving up or down
                if player.direction.y > 0:
                    player.collision_rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.collision_rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

    # update method to update the game
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False

    # scroll_x method to scroll the world horizontally when the player reaches the edge of the screen horizontally

    def scroll_x(self):
        # get the player sprite
        player = self.player.sprite

        # get the player x position and direction
        player_x = player.rect.centerx

        # get the screen width
        direction_x = player.direction.x

        # check if the player is at the edge of the screen and scroll the world
        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0

        # check if the player is at the edge of the screen and scroll the world
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0

        # if the player is not at the edge of the screen then don't scroll the world
        else:
            self.world_shift = 0
            player.speed = 8

    # get player on the ground method to check if the player is on the ground
    def get_player_on_ground(self):
        # check if the player is on the ground
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    # create landing dust method to create the landing dust particles when the player lands
    def create_landing_dust(self):
        # create the landing dust particles when the player lands on the ground
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10, 15)
            else:
                offset = pygame.math.Vector2(-10, 15)

            # create the landing dust particle sprite and add it to the sprite group
            fall_dust_particle = ParticleEffect(
                self.player.sprite.rect.midbottom - offset, 'land')

            # add the dust particle to the dust sprite group
            self.dust_sprite.add(fall_dust_particle)

    # check death method to check if the player has died and if so then reset the level and the player position
    def check_death(self):
        if self.player.sprite.rect.top > screen_height:
            self.create_overworld(self.current_level, 0)

    # check win method to check of the player has won the level and if so then reset the level and the player position
    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            self.create_overworld(self.current_level, self.new_max_level)

    # check coin collision method to check if the player has collided with a coin and if so then add the coin value to the player score
    def check_coin_collisions(self):
        collided_coins = pygame.sprite.spritecollide(
            self.player.sprite, self.coin_sprites, True)
        if collided_coins:
            self.coin_sound.play()
            for coin in collided_coins:
                self.change_coins(coin.value)

    # check enemy collision method to check if the player has collided with an enemy and if so then check if the player is above the enemy and if so then kill the enemy and add the enemy value to the player score
    def check_enemy_collisions(self):
        enemy_collisions = pygame.sprite.spritecollide(
            self.player.sprite, self.enemy_sprites, False)

        # check if the player has collided with an enemy
        if enemy_collisions:
            # loop through the enemy collisions
            for enemy in enemy_collisions:
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom
                # check if the player is above the enemy and if so then kill the enemy and add the enemy value to the player score
                if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
                    self.stomp_sound.play()
                    self.player.sprite.direction.y = -15
                    explosion_sprite = ParticleEffect(
                        enemy.rect.center, 'explosion')
                    self.explosion_sprites.add(explosion_sprite)
                    enemy.kill()
                # if the player is not above the enemy then kill the player
                else:
                    self.player.sprite.get_damage()

    def run(self):
        # run the entire game / level

        # sky
        self.sky.draw(self.display_surface)

        # dust particles
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        # terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        # enemy
        self.enemy_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)
        self.explosion_sprites.update(self.world_shift)
        self.explosion_sprites.draw(self.display_surface)

        # crate
        self.crate_sprites.update(self.world_shift)
        self.crate_sprites.draw(self.display_surface)

        # grass
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)

        # coins
        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)

        # player sprites
        self.player.update()
        self.horizontal_movement_collision()

        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.create_landing_dust()

        self.scroll_x()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        self.check_death()
        self.check_win()

        self.check_coin_collisions()
        self.check_enemy_collisions()

        # water
        self.water.draw(self.display_surface, self.world_shift)
