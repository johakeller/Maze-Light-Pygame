import sys

import pygame
from settings import *
from menu import Button, Menu


class Message(Menu):
    def __init__(self, surface, current_level, max_level, menu_type, pause_game, set_game_over, set_win, coins):
        super().__init__(current_level, max_level, surface, menu_type, None, sys.exit, pause_game)

        # general setup
        self.set_game_over = set_game_over
        self.set_win = set_win
        self.coins = coins

        # menu creation
        self.button = None
        self.score_surf = None
        self.score_rect = None
        self.build_message()  # calls build message

    def build_message(self):
        text = None

        # general background
        top = self.height // 2
        left = self.width // 2 + 15
        self.menu_bg = pygame.Rect(left, top, self.width, self.height)

        # set left for buttons
        left = left + (self.width * 0.5) - (self.width * 0.7 * 0.5)

        if self.menu_type == 'game_over':
            # title
            self.title_surf = self.title_font.render('Game Over', False, TEXT_COLOR)

            # score
            self.score_surf = self.font.render(f'Coins: {self.coins}', False, TEXT_COLOR)
            self.score_rect = self.score_surf.get_rect(center=(self.menu_bg.center[0], top + 130))

        elif self.menu_type == 'win':
            # title
            self.title_surf = self.title_font.render('Level Accomplished', False, TEXT_COLOR)

            # score
            self.score_surf = self.font.render(f'Coins: {self.coins}', False, TEXT_COLOR)
            self.score_rect = self.score_surf.get_rect(center=(self.menu_bg.center[0], top + 130))

        elif self.menu_type == 'paused':
            # title
            self.title_surf = self.title_font.render('Game Paused', False, TEXT_COLOR)

        self.title_rect = self.title_surf.get_rect(center=(self.menu_bg.center[0], top + 50))
        self.button = Button(left, top + 200, self.width * 0.7, 50, 0, self.font, 'Continue', self.menu_type, True)

    def trigger(self):
        # paused state
        if self.menu_type == 'paused':
            self.pause_game()

        # win state
        if self.menu_type == 'win':
            self.set_win()

        # game over state
        if self.menu_type == 'game_over':
            self.set_game_over()

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
            self.can_move = False
            self.selection_time = pygame.time.get_ticks()
            self.trigger()

    def run(self):
        self.input()
        self.selection_cooldown()

        # display background
        pygame.draw.rect(self.display_surface, UI_bg_color, self.menu_bg)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, self.menu_bg, 3)
        self.display_surface.blit(self.title_surf, self.title_rect)

        # display score
        if self.score_surf:
            self.display_surface.blit(self.score_surf, self.score_rect)

        # display button
        self.button.display(self.display_surface, self.selection_index, self.button.text)

