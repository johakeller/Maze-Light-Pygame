import sys

import pygame

from level import Level
from menu import Menu
from settings import *


class Game:
    """
    A class to initialize the game 'Maze Light'. Provides methods to create the main menu and the levels.

    Attributes
    ----------
    level : Level
        instance currently running level
    max_level : int
        maximum level to be unlocked next
    menu : Menu
        instance of currently running main menu
    status : str
         allows to switch between level and menu
    """

    def __init__(self):
        # menu
        self.level = None
        self.max_level = 0
        self.menu = Menu(0, self.max_level, screen, self.create_level, sys.exit)
        self.status = 'menu'

    def create_menu(self, current_level, new_max_level):
        """
        A method to set up the main menu and run it. Displays all playable levels and exit option.

        Parameters
        ----------
        current_level : int
            index of current level
        new_max_level : int
            index of new level to be unlocked after succeeding in the current level
        """
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.menu = Menu(current_level, self.max_level, screen, self.create_level, sys.exit)
        self.menu.can_move = False
        self.menu.selection_time = pygame.time.get_ticks()
        self.status = 'menu'

    def create_level(self, current_level):
        """
        A method to set up the current level and run it.

        Parameters
        ----------
        current_level : int
            index of the level to run
        """
        self.level = Level(current_level, screen, self.create_menu)
        self.status = 'level'

    def run_game(self):
        """
        Method to start the game.
        """
        if self.status == 'menu':
            self.menu.run()
        else:
            self.level.run()


# pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Maze Light')
clock = pygame.time.Clock()
game = Game()


def run():
    """
    Method provides basic pygame set up und calls run_game() to initialize the game.
    """
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill('black')
        game.run_game()

        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    run()
