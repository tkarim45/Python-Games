import pygame


class UI:
    """

    Class for the user interface. 
    This includes the health bar, coins, and other UI elements. 
    UI elements are drawn on the screen in the main game loop.

    """

    def __init__(self, surface):
        """
        initialize UI elements and set their positions on the screen 

        """

        # setup
        self.display_surface = surface

        # load health bar image and set health bar position
        self.health_bar = pygame.image.load(
            'graphics/ui/health_bar.png').convert_alpha()
        self.health_bar_topleft = (54, 39)
        self.bar_max_width = 152
        self.bar_height = 4

        # load coin icon and font for coin amount text
        self.coin = pygame.image.load('graphics/ui/coin.png').convert_alpha()
        self.coin_rect = self.coin.get_rect(topleft=(50, 61))
        self.font = pygame.font.Font('graphics/ui/ARCADEPI.ttf', 30)

    def show_health(self, current, full):
        """
        draw health bar and health bar fill on screen

        """

        # draw health bar
        self.display_surface.blit(self.health_bar, (20, 10))

        # draw health bar fill
        current_health_ratio = current / full
        current_bar_width = self.bar_max_width * current_health_ratio
        health_bar_rect = pygame.Rect(
            self.health_bar_topleft, (current_bar_width, self.bar_height))

        # draw health bar fill color based on health ratio
        pygame.draw.rect(self.display_surface, '#dc4949', health_bar_rect)

    def show_coins(self, amount):
        """
        draw coin icon and coin amount text on screen     

        """

        # draw coin icon and amount
        self.display_surface.blit(self.coin, self.coin_rect)

        # draw coin amount text
        coin_amount_surf = self.font.render(str(amount), False, '#33323d')
        coin_amount_rect = coin_amount_surf.get_rect(
            midleft=(self.coin_rect.right + 4, self.coin_rect.centery))

        # draw coin amount text on screen
        self.display_surface.blit(coin_amount_surf, coin_amount_rect)

        
        
