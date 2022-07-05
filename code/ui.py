import pygame
from settings import *


class UI:
    def __init__(self):
        # general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_font, UI_font_size)

        # bar setup
        self.health_bar_rect = pygame.Rect(10, 10, health_bar_width, bar_height)

    def show_radius(self, player_radius, light):
        # creating the invisibility setup
        if light:
            self.invisible_image = pygame.image.load('../graphics/terrain/visibility.png').convert_alpha()
            self.invisible_rect = self.invisible_image.get_rect()[2:4]
            self.invisibe_surf = pygame.transform.scale(self.invisible_image, (
            int(self.invisible_rect[0] * player_radius), int(self.invisible_rect[1]) * player_radius))
            self.inv_rect = self.invisibe_surf.get_rect(center=screen_center)
            self.display_surface.blit(self.invisibe_surf, self.inv_rect)
        else:
            pygame.draw.rect(self.display_surface, 'black', (0,0, screen_width, screen_height))

    def show_bar(self, current, max_amount, bg_rect, color):
        # draw bg
        pygame.draw.rect(self.display_surface, UI_bg_color, bg_rect)

        # convert stat to pixel
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # drawing the bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def show_coins(self, coins):
        coin = pygame.image.load('../graphics/coins/gold/0.png').convert_alpha()
        coin_rect = coin.get_rect(topleft=(260, 5))
        self.display_surface.blit(coin, coin_rect)

        text_surf = self.font.render(str(int(coins)), False, TEXT_COLOR)
        text_rect = text_surf.get_rect(topleft=(320, 12))
        pygame.draw.rect(self.display_surface, UI_bg_color, text_rect.inflate(25, 10))
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(25, 10), 3)
        self.display_surface.blit(text_surf, text_rect)

    def display(self, player):
        self.show_radius(player.visible_factor, player.light_on)
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, health_color)
        self.show_coins(player.coins)
