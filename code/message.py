import sys

import pygame

from menu import Button, Menu
from settings import *


class Message(Menu):
    """
    A class to display a message menu for notification in case of winning, game over and game paused with score and
    continue-button. Inherits from Menu.

    Parameters
    ----------
    surface : pygame.Display
        surface to display message
    current_level : int
        index of the current level
    max_level : int
        index of level to be unlocked in case of victory
    menu_type : str
        type of menu for button creation and dict search
    pause_game : def
        method from level to pause/ unpause game
    set_game_over : def
        method from level to set the game_over state True
    set_win : def
        method from level to set the win state True
    coins : int
        current amount of coins collected by the player

    Attributes
    ----------
    set_game_over : def
        see Parameters
    set_win : def
        see Parameters
    pause_game : def
        see Parameters
    coins : int
        see Parameters
    menu_type : str
        see Parameters
    button : Button
        continue button
    score_surf : pygame.Surface
        display coins score
    score_rect : pygame.Rect
        rect for score_surf
    self.build_message() : method call
        sets up message-object
    """

    def __init__(self, surface, current_level, max_level, menu_type, pause_game, set_game_over, set_win, coins):
        super().__init__(current_level, max_level, surface, None, sys.exit)

        # general setup
        self.set_game_over = set_game_over
        self.set_win = set_win
        self.pause_game = pause_game
        self.coins = coins

        # menu creation
        self.menu_type = menu_type
        self.button = None
        self.score_surf = None
        self.score_rect = None
        self.build_message()  # calls build message

        # sound
        self.button_sound = pygame.mixer.Sound('../audio/button.wav')
        self.button_sound.set_volume(0.4)

    def build_message(self):
        """
        A method to build a message object, the appearance and content of the message is defined by the menu_type.
        game over and win display score. All messages have a continue button to resume game or go back to main menu.
        """
        # general background
        top = self.half_height // 2
        left = self.half_width // 2 + 15
        self.menu_bg = pygame.Rect(left, top, self.half_width, self.half_height)

        # set left for buttons
        left = left + (self.half_width * 0.5) - (self.half_width * 0.7 * 0.5)

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
        self.button = Button(left, top + 200, self.half_width * 0.7, 50, 0, self.font, 'Continue', self.menu_type, True)

    def trigger(self):
        """
        Method to trigger continue button. Calls different methods according to game state.
        """
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
        """
        A method to fetch keyboard input and call the trigger()-method if continue-button is pressed.
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
            pygame.mixer.find_channel(True).play(self.button_sound)
            self.can_move = False
            self.selection_time = pygame.time.get_ticks()
            self.trigger()

    def run(self):
        """
        Method to display entire message on screen.
        """
        self.input()
        self.selection_cooldown()

        # display background
        pygame.draw.rect(self.display_surface, UI_BACKGROUND_COLOR, self.menu_bg)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, self.menu_bg, 3)
        self.display_surface.blit(self.title_surf, self.title_rect)

        # display score
        if self.score_surf:
            self.display_surface.blit(self.score_surf, self.score_rect)

        # display continue-button
        self.button.display(self.display_surface, self.selection_index, self.button.text)
