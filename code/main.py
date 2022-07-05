import pygame, sys

from menu import Menu
from settings import *
from level import Level
from game_data import level_0


class Game:
    def __init__(self):
        # menu
        self.level = None
        self.max_level = 0
        self.menu = Menu(0, self.max_level, screen, 'start', self.create_level, sys.exit, self.pause_game)
        self.status = 'menu'

    def pause_game(self):
        self.level.game_paused = not self.level.game_paused

    def create_menu(self, current_level, new_max_level, menu_type):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.menu = Menu(current_level, self.max_level, screen, menu_type, self.create_level, sys.exit, self.pause_game)
        self.menu.can_move = False
        self.menu.selection_time = pygame.time.get_ticks()
        self.status = 'menu'

    def create_level(self, current_level):
        self.level = Level(current_level, screen, self.create_menu, self.run)
        self.status = 'level'

    def run(self):
        if self.status == 'menu':
            self.menu.run()
        else:
            self.level.run()


# pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Maze Light')
clock = pygame.time.Clock()
game = Game()


def run():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill('black')
        game.run()

        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    run()
