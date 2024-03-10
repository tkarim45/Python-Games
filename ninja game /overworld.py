import pygame
from game_data import levels
from support import import_folder
from decoration import Sky


class Node(pygame.sprite.Sprite):
    # This class is used to create the nodes that the player can travel to in the overworld. It is also used to create the paths that connect the nodes. The nodes are created in the overworld class. The paths are created in the draw_paths method of the overworld class.
    def __init__(self, pos, status, icon_speed, path):
        super().__init__()

        # This line of code is used to set the frames attribute to the list of images in the folder that is passed to the class.
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        # This line of code is used to set the status attribute to the status that is passed to the class. The status
        if status == 'available':
            self.status = 'available'
        else:
            self.status = 'locked'

        # This line of code is used to set the rect attribute of the node. The rect attribute is used to check for collisions and to draw the node to the screen.
        self.rect = self.image.get_rect(center=pos)

        # This line of code is used to set the detection zone attribute of the node. The detection zone is used to check if the player is close enough to the node to travel to it.
        self.detection_zone = pygame.Rect(
            self.rect.centerx-(icon_speed/2), self.rect.centery-(icon_speed/2), icon_speed, icon_speed)

    # This method is used to animate the node. It is called in the update method of the overworld class.
    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    #  This method is used to update the node. It is called in the main game loop.
    def update(self):
        # This line of code is used to check if the status of the node is available. If it is, the node is animated. If it is not, the node is tinted black.
        if self.status == 'available':
            self.animate()
        # This line of code is used to check if the status of the node is locked. If it is, the node is tinted black.
        elif self.status == 'locked':
            # This line of code is used to create a copy of the node image. The copy is used to tint the node black.
            tint_surf = self.image.copy()
            tint_surf.fill('black', None, pygame.BLEND_RGBA_MULT)
            self.image.blit(tint_surf, (0, 0))


class Icon(pygame.sprite.Sprite):
    # This class is used to create the icon that the player uses to travel to the nodes in the overworld. It is also used to create the hat that the player wears when they have completed all of the levels in the overworld.
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        # This line of code is used to load the icon image and set the image attribute to the image. The image is then scaled to the correct size. The rect attribute is then set to the rect of the image.
        self.image = pygame.image.load(
            'graphics/overworld/hat.png').convert_alpha()

        # This line of code is used to scale the image to the correct size.
        self.image = pygame.transform.scale(self.image, (80, 80))

        # This line of code is used to set the rect attribute to the rect of the image.
        self.rect = self.image.get_rect(center=pos)

    # This method is used to update the icon. It is called in the main game loop.
    def update(self):
        self.rect.center = self.pos


class Overworld:
    # This class is used to create the overworld. It is also used to manage the overworld.
    def __init__(self, start_level, max_level, surface, create_level):

        # setup
        self.display_surface = surface
        self.max_level = max_level
        self.current_level = start_level
        self.create_level = create_level

        # movement logic
        self.moving = False
        self.move_direction = pygame.math.Vector2(0, 0)
        self.speed = 8

        # sprites
        self.setup_nodes()
        self.setup_icon()
        self.sky = Sky(8, 'overworld')

        # time
        self.start_time = pygame.time.get_ticks()
        self.allow_input = False
        self.timer_length = 300

    # This method is used to update the overworld. It is called in the main game loop.
    def setup_nodes(self):
        # This line of code is used to create a group of nodes. The nodes are created using the node class. The nodes are added to the group.
        self.nodes = pygame.sprite.Group()

        # This line of code is used to create a node for each level in the levels dictionary. The nodes are added to the nodes group.
        for index, node_data in enumerate(levels.values()):
            # This line of code is used to check if the index of the node is less than or equal to the max level. If it is, the node is created as available. If it is not, the node is created as locked.
            if index <= self.max_level:
                node_sprite = Node(
                    node_data['node_pos'], 'available', self.speed, node_data['node_graphics'])
            else:
                node_sprite = Node(
                    node_data['node_pos'], 'locked', self.speed, node_data['node_graphics'])

            # This line of code is used to add the node to the nodes group.
            self.nodes.add(node_sprite)

    # This method is used to draw the overworld to the screen. It is called in the main game loop.
    def draw_paths(self):
        # This line of code is used to check if the max level is greater than 0. If it is, the paths are drawn. If it is not, the paths are not drawn.
        if self.max_level > 0:
            # This line of code is used to create a list of the positions of the nodes. The list is used to draw the paths between the nodes.
            points = [node['node_pos'] for index, node in enumerate(
                levels.values()) if index <= self.max_level]

            # This line of code is used to draw the paths between the nodes.
            pygame.draw.lines(self.display_surface,
                              '#a04f45', False, points, 6)

    # This method is used to draw the overworld to the screen. It is called in the main game loop.
    def setup_icon(self):
        # This line of code is used to create a group of icons. The icon is created using the icon class. The icon is added to the group.
        self.icon = pygame.sprite.GroupSingle()
        # This line of code is used to create an icon. The icon is added to the icon group.
        icon_sprite = Icon(self.nodes.sprites()[
                           self.current_level].rect.center)
        # This line of code is used to add the icon to the icon group.
        self.icon.add(icon_sprite)

    # This method is used to draw the overworld to the screen. It is called in the main game loop.
    def display_game_name(self):
        # This line of code is used to load the game name image and set the image attribute to the image. The image is then scaled to the correct size. The rect attribute is then set to the rect of the image.
        game_name = pygame.image.load(
            'graphics/overworld/game_name.png').convert_alpha()
        # This line of code is used to scale the image to the correct size.
        game_name = pygame.transform.scale(game_name, (450, 300))

        # This line of code is used to draw the game name to the screen.
        self.display_surface.blit(game_name, (360, -80))

    # This method is used to draw the overworld to the screen. It is called in the main game loop.
    def display_text_onscreen(self, message, x, y):
        self.font = pygame.font.Font('graphics/ui/ARCADEPI.ttf', 15)
        self.text = self.font.render(message, True, 'black')
        self.text_rect = self.text.get_rect(center=(x, y))
        self.display_surface.blit(
            self.text, (self.text_rect.x, self.text_rect.y))
        self.display_game_name()
        pygame.display.update()

    # input method to check if the player has pressed the right or left arrow keys
    def input(self):
        keys = pygame.key.get_pressed()

        # check if the player has pressed the right or left arrow keys
        if not self.moving and self.allow_input:
            if keys[pygame.K_RIGHT] and self.current_level < self.max_level:
                self.move_direction = self.get_movement_data('next')
                self.current_level += 1
                self.moving = True
            elif keys[pygame.K_LEFT] and self.current_level > 0:
                self.move_direction = self.get_movement_data('previous')
                self.current_level -= 1
                self.moving = True
            elif keys[pygame.K_SPACE]:
                self.create_level(self.current_level)

        # check if the level is 1 and if the player has pressed the space bar
        if self.current_level == 0 and keys[pygame.K_SPACE]:
            self.display_text_onscreen(
                "The Magic Scroll was stolen from the Village of TAHEETI. Rendering the Village defenseless.", 580, 300)
            self.display_text_onscreen(
                "A Young Brave Ninja Sets on a Quest to Return its Village Pride. The First Clue was", 580, 320)
            self.display_text_onscreen(
                "What has roots as nobody sees, Is taller than trees, Up, up it goes And yet never grows?", 580, 340)

            self.display_text_onscreen(
                "Tahichi no mura kara mahō no makimono ga nusuma reta. Mura o mubōbi ni suru.", 580, 500)
            self.display_text_onscreen(
                "Mura no hokori o torimodosu tame, wakaki yūsha ninja ga bōken ni deru.", 580, 520)
            self.display_text_onscreen(
                "Darenimo mienai ne o motte iru no wa ki yori mo takaku ue e ue e to nobite iku no ni sodatanai no?", 580, 540)

            pygame.time.delay(3000)

            # check if the level is 2 and if the player has pressed the space bar
        if self.current_level == 1 and keys[pygame.K_SPACE]:
            self.display_text_onscreen(
                "After Reaching the mountains. The Ninja found out the sword of AZRA which showed him", 580, 300)
            self.display_text_onscreen(
                "his path to finding the magic scroll. On the sword the following words were marked ", 580, 320)
            self.display_text_onscreen(
                "I am a path situated between high natural masses. Remove my first letter", 580, 340)
            self.display_text_onscreen(
                "& you have a path situated between man-made masses. ", 580, 360)

            self.display_text_onscreen(
                "Yama ni tsuita nochi. Ninja wa kare ni miseta Azura no ken o mitsuketa", 580, 500)
            self.display_text_onscreen(
                "Mahō no makimono o mitsukeru made no michinori. Ken ni wa tsugi no kotoba ga shirusa rete ita", 580, 520)
            self.display_text_onscreen(
                "Watashi wa takai shizen no katamari no ma ni ichi suru michidesu. Saisho no moji o sakujo", 580, 540)
            self.display_text_onscreen(
                "& Anata wa jinkō no katamari no ma ni aru michi o motte imasu.", 580, 560)

            pygame.time.delay(3000)

            # check if the level is 3 and if the player has pressed the space bar
        if self.current_level == 2 and keys[pygame.K_SPACE]:
            self.display_text_onscreen(
                "After reaching the Valley of death the young ninja raided the village and retrieved the ", 580, 300)
            self.display_text_onscreen(
                "Magic scroll and returned the pride of its village. ", 580, 320)

            self.display_text_onscreen(
                "Shi no tani ni tōtatsu shita nochi, wakai ninja wa mura o shūgeki shi,", 580, 500)
            self.display_text_onscreen(
                "Mahō no makimono de mura no hokori o torimodoshita. ", 580, 520)

            pygame.time.delay(3000)

    # This get movement data method is used to get the movement data of the player
    def get_movement_data(self, target):
        # get the start and end positions of the movement
        start = pygame.math.Vector2(
            self.nodes.sprites()[self.current_level].rect.center)

        # get the end position of the movement
        if target == 'next':
            end = pygame.math.Vector2(
                self.nodes.sprites()[self.current_level + 1].rect.center)
        else:
            end = pygame.math.Vector2(
                self.nodes.sprites()[self.current_level - 1].rect.center)

        return (end - start).normalize()

    #  update icon position method to move the icon
    def update_icon_pos(self):
        # check if the player is moving and if the player has pressed the space bar
        if self.moving and self.move_direction:
            # move the icon
            self.icon.sprite.pos += self.move_direction * self.speed
            target_node = self.nodes.sprites()[self.current_level]
            # check if the icon has reached the target node
            if target_node.detection_zone.collidepoint(self.icon.sprite.pos):
                self.moving = False
                # reset the move direction
                self.move_direction = pygame.math.Vector2(0, 0)

    # input timer function to prevent the player from spamming the space bar
    def input_timer(self):
        if not self.allow_input:
            # get the current time in milliseconds
            current_time = pygame.time.get_ticks()
            # check if the current time is greater than the start time + the timer length
            if current_time - self.start_time >= self.timer_length:
                self.allow_input = True

    # run method to run the game
    def run(self):
        self.input_timer()
        self.input()
        self.update_icon_pos()
        self.icon.update()
        self.nodes.update()

        self.sky.draw(self.display_surface)
        self.draw_paths()
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)
        self.display_game_name()
