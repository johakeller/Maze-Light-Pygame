import pygame

from settings import *


class UI:
    """
    A class to display the user interface including coin-score, health-bar and a light raduis of the player.

    Attributes
    ----------
    display_surface : pygame.Display
        surface to display level
    font : pygame.font.Font
        type of font
    health_bar_rect : pygame.Rect
        displays health-bar
    darkness_image : pygame.Image
        cover screen beyond the visible_radius of the player in black
    darkness_rect : pygame.Rect
         make darkness_image scale able
    """

    def __init__(self):
        # general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # bar setup
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)

        # display darkness
        self.darkness_image = pygame.image.load('../graphics/terrain/visibility.png').convert_alpha()
        self.darkness_rect = self.darkness_image.get_rect()[2:4]

    def show_radius(self, player_radius, light):
        """
        Method to adjusts display of darkness to the visible_radius of the player if light is on or fill screen black if
        light is off.

        Attributes
        ----------
        player_radius : int
            radius in which player can be seen by enemies and the player can see
        """
        # light is on: transform darkness by player.visible_factor
        if light:
            darkness_surf = pygame.transform.scale(self.darkness_image, (
                int(self.darkness_rect[0] * player_radius), int(self.darkness_rect[1]) * player_radius))
            darkness_rect = darkness_surf.get_rect(center=SCREEN_CENTER)
            self.display_surface.blit(darkness_surf, darkness_rect)
        # light is off:
        else:
            pygame.draw.rect(self.display_surface, 'black', (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    def show_bar(self, current_health, max_health, bg_rect, color):
        """
        Method to show health bar with current state of health.

        Parameters
        ----------
        current_health : int
            current health of the player
        max_health : int
            maximum amount of health of player
        bg_rect : pygame.Rect
            background rect to draw health-bar on
        color : (r,g,b)
            color for health bar
        """
        # draw background
        pygame.draw.rect(self.display_surface, UI_BACKGROUND_COLOR, bg_rect)

        # convert statistics to pixel
        ratio = current_health / max_health
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # drawing the bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def show_coins(self, coins):
        """
        Method to show collected coins by player.

        Parameters
        ----------
        coins : int
            collected coin value
        """
        coin = pygame.image.load('../graphics/coins/gold/0.png').convert_alpha()
        coin_rect = coin.get_rect(topleft=(260, 5))
        self.display_surface.blit(coin, coin_rect)

        text_surf = self.font.render(str(int(coins)), False, TEXT_COLOR)
        text_rect = text_surf.get_rect(topleft=(320, 12))
        pygame.draw.rect(self.display_surface, UI_BACKGROUND_COLOR, text_rect.inflate(25, 10))
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(25, 10), 3)
        self.display_surface.blit(text_surf, text_rect)

    def display(self, player):
        """
        A Method to display and update user interface in level class. Calls show_radius(), show_bar() and show_coins().
        """
        self.show_radius(player.visible_factor, player.light_on)
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_BAR_COLOR)
        self.show_coins(player.coins)
