import pygame
from settings import *
from game_data import levels, menu_dict


class Menu:
    def __init__(self, start_level, max_level, surface, menu_type, create_level, game_exit, pause_game):

        # general setup
        self.display_surface = surface
        self.max_level = max_level
        self.current_level = start_level
        self.create_level = create_level
        self.exit = game_exit
        self.pause_game = pause_game

        # menu creation
        self.button_nr = 0
        self.button_keys = list()
        self.title_font = pygame.font.Font(UI_font, UI_font_size)
        self.menu_type = menu_type
        self.height = self.display_surface.get_size()[1] * 0.5
        self.width = self.display_surface.get_size()[0] * 0.5
        self.menu_bg = None
        self.title_surf = None
        self.title_rect = None
        self.title_font = pygame.font.Font(UI_font, menu_font_size)
        self.font = pygame.font.Font(UI_font, UI_font_size)
        self.button_list = []
        self.inactive_button_list = []
        self.build_menu()  # calls create_menu

        # selection system
        self.selection_index = 0
        self.selection_time = None
        self.can_move = True

        # sound
        self.button_sound = pygame.mixer.Sound('../audio/button.wav')
        self.button_sound.set_volume(0.4)

    def build_menu(self):
        top = self.height // 2
        left = self.width // 2 + 15

        # general background
        self.bg_surface = pygame.image.load('../graphics/menu_bg.png').convert()
        self.bg_rect = self.bg_surface.get_rect(topleft=(0, 0))


        # background menu
        self.menu_bg = pygame.Rect(left, top, self.width, self.height)

        # determine number of buttons
        self.button_nr = len(menu_dict[self.menu_type])

        # set left for buttons
        left = left + (self.width * 0.5) - (self.width * 0.7 * 0.5)

        if self.menu_type == 'start':
            # title
            self.title_surf = self.title_font.render('Maze Light', False, TEXT_COLOR)
            self.title_rect = self.title_surf.get_rect(center=(self.width, top + 50))
            top += 20

            # create buttons
            for button, index in enumerate(range(self.button_nr)):
                # create each button
                text = menu_dict[self.menu_type][button]
                top += 65
                if button > self.max_level and button != self.button_nr - 1:
                    button = Button(left, top, self.width * 0.7, 50, index, self.font, text, self.menu_type, False)
                elif button == self.button_nr - 1:
                    button = Button(left, top, self.width * 0.7, 50, index, self.font, text, self.menu_type, True)
                else:
                    button = Button(left, top, self.width * 0.7, 50, index, self.font, text, self.menu_type, True)
                self.button_list.append(button)

    def input(self):
        keys = pygame.key.get_pressed()

        if self.can_move:
            if keys[pygame.K_RIGHT] and self.selection_index < self.button_nr - 1:
                self.selection_index += 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_LEFT] and self.selection_index >= 1:
                self.selection_index -= 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_UP] and self.selection_index >= 1:
                self.selection_index -= 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_DOWN] and self.selection_index < self.button_nr - 1:
                self.selection_index += 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()

            if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
                pygame.mixer.find_channel(True).play(self.button_sound)
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                self.button_list[self.selection_index].trigger(self.current_level, self.max_level, self.create_level,
                                                               self.exit,
                                                               self.pause_game)

    def selection_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 100:
                self.can_move = True

    def run(self):
        self.input()
        self.selection_cooldown()

        #display background
        self.display_surface.blit(self.bg_surface, self.bg_rect)

        # display menu background
        pygame.draw.rect(self.display_surface, UI_bg_color, self.menu_bg)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, self.menu_bg, 3)
        self.display_surface.blit(self.title_surf, self.title_rect)

        for index, button in enumerate(self.button_list):
            button.display(self.display_surface, self.selection_index, button.text)


class Button:
    def __init__(self, l, t, w, h, index, font, text, menu_type, active):
        self.rect = pygame.Rect(l, t, w, h)
        self.index = index
        self.font = font
        self.text = text
        self.menu_type = menu_type
        self.active = active

    def display_text(self, surface, text, selected):
        if self.active:
            color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR
        else:
            color = UI_BORDER_COLOR

        # text
        text_surf = self.font.render(text, False, color)
        text_rect = text_surf.get_rect(center=self.rect.center)

        # draw
        surface.blit(text_surf, text_rect)

    def trigger(self, current_level, max_level, create_level, exit_game, pause_game):
        selection = menu_dict[self.menu_type][self.index]

        # start state
        if self.menu_type == 'start':
            if selection != 'Exit' and self.active:
                create_level(self.index)
            elif selection == 'Exit':
                exit_game()

    def display(self, surface, selection_num, text):
        if self.active:
            if self.index == selection_num:
                pygame.draw.rect(surface, menu_color_selected, self.rect)
                pygame.draw.rect(surface, BORDER_COLOR_SELECTED, self.rect, 3)
            else:
                pygame.draw.rect(surface, UI_bg_color, self.rect)
                pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 3)

            self.display_text(surface, text, self.index == selection_num)
        else:
            pygame.draw.rect(surface, MENU_COLOR_INACTIVE, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 3)

            self.display_text(surface, text, self.index == selection_num)
