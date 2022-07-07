import pygame

from game_data import menu_dict
from settings import *


class Menu:
    """
    A class to display main menu with buttons for selectable levels and exit option. According to the unlock-level
    defined by the current level, levels are unlocked after winning.

    Parameters
    ----------
    start_level : int
        index of the current level
    max_level : int
        index of level to be unlocked in case of victory
    surface : pygame.Display
        surface to display menu
    create_level : def
        creates new level
    game_exit : def
        method to exit game

    Attributes
    ----------
    display_surface : pygame.Display
        surface to display menu
    max_level : int
        see Parameters
    current_level : int
        index of the current level
    create_level : def
        see Parameters
    exit : def
        see Parameters
    menu_type : str
        type of menu for button creation and dict search
    button_nr : int
        amount of buttons to be displayed
    title_font : pygame.font.Font
        message title font
    half_height : float
        half screen height
    half_width : float
        half screen width
    bg_image : pygame.Image
        background image
    bg_rect : pygame.Rect
        rect for background image
    menu_bg : pygame.Rect
        rect for menu background
    title_surf : pygame.Surface
        title font display-surface
    title_rect : pygame.Rect
        rect for title
    title_font : pygame.font.Font
        title font
    font : pygame.font.Font
        normal font
    button_list : list
        buttons to be displayed and are selectable
    inactive_button_list : list
        unselectable buttons
    build_menu() : function call
        sets up menu
    selection_index : int
        index of currently selected button
    selection_time : int
        time button was selected
    can_move : bool
        if True selection can be changed
    """
    def __init__(self, start_level, max_level, surface, create_level, game_exit):

        # general setup
        self.display_surface = surface
        self.max_level = max_level
        self.current_level = start_level
        self.create_level = create_level
        self.exit = game_exit

        # menu creation
        self.menu_type = 'start'
        self.button_nr = 0
        self.title_font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.half_height = self.display_surface.get_size()[1] * 0.5
        self.half_width = self.display_surface.get_size()[0] * 0.5
        self.bg_image = None
        self.bg_rect = None
        self.menu_bg = None
        self.title_surf = None
        self.title_rect = None
        self.title_font = pygame.font.Font(UI_FONT, MENU_FONT_SIZE)
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
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
        """
        A method to build an entire menu screen. Provides background image, menu background, titles and button-objects
        with text.
        """
        top = self.half_height // 2
        left = self.half_width // 2 + 15

        # background image
        self.bg_image = pygame.image.load('../graphics/menu_bg.png').convert()
        self.bg_rect = self.bg_image.get_rect(topleft=(0, 0))

        # background menu
        self.menu_bg = pygame.Rect(left, top, self.half_width, self.half_height)
        # buttons
        # determine number of buttons
        self.button_nr = len(menu_dict[self.menu_type])
        # set left for buttons
        left = left + (self.half_width * 0.5) - (self.half_width * 0.7 * 0.5)

        # title
        self.title_surf = self.title_font.render('Maze Light', False, TEXT_COLOR)
        self.title_rect = self.title_surf.get_rect(center=(self.half_width, top + 50))
        top += 20

        # create buttons
        for button, index in enumerate(range(self.button_nr)):
            # create each button
            text = menu_dict[self.menu_type][button]
            top += 65
            if button > self.max_level and button != self.button_nr - 1:
                button = Button(left, top, self.half_width * 0.7, 50, index, self.font, text, self.menu_type, False)
            elif button == self.button_nr - 1:
                button = Button(left, top, self.half_width * 0.7, 50, index, self.font, text, self.menu_type, True)
            else:
                button = Button(left, top, self.half_width * 0.7, 50, index, self.font, text, self.menu_type, True)
            self.button_list.append(button)

    def input(self):
        """
        A method to trigger actions in menu according to keyboard input. Buttons can be selected via selection index and
        movement timer and can be triggered to call connected trigger()-method.
        """
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
                self.button_list[self.selection_index].trigger(self.create_level, self.exit)

    def selection_cooldown(self):
        """
        Method measures time since last selection and compares with cooldown time. If enough time has passed, selection
        can continue since can_move is set True.
        """
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 100:
                self.can_move = True

    def run(self):
        """
        Method to display entire menu on screen surface and check and update according to keyboard input.
        """
        self.input()
        self.selection_cooldown()

        # display background
        self.display_surface.blit(self.bg_image, self.bg_rect)

        # display menu background
        pygame.draw.rect(self.display_surface, UI_BACKGROUND_COLOR, self.menu_bg)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, self.menu_bg, 3)
        self.display_surface.blit(self.title_surf, self.title_rect)

        for index, button in enumerate(self.button_list):
            button.display(self.display_surface, self.selection_index, button.text)


class Button:
    """
    A class to display main menu with buttons for selectable levels and exit option. According to the unlock-level
    defined by the current level, levels are unlocked after winning.

    Parameters
    ----------
    left : int
        left position of button
    top : int
        top position of button
    width : int
        width of button
    height : int
        height of button
    index : int
        index of button
    font : pygame.font.Font
        font for button text
    text : str
        text on button
    menu_type : str
        type of menu for button function
    active : bool
        if True button can be triggered

    Attributes
    ----------
    menu_type : str
        see Parameters
    rect : pygame.Rect
        displaying button in rect
    index : int
        see Parameters
    font : pygame.font.Font
        see Parameters
    text : str
        see Parameters
    active : bool
        see Parameters
    """
    def __init__(self, left, top, width, height, index, font, text, menu_type, active):
        self.menu_type = menu_type
        self.rect = pygame.Rect(left, top, width, height)
        self.index = index
        self.font = font
        self.text = text
        self.active = active

    def display_text(self, surface, text, selected):
        """
        Method to display text on button.

        Parameters
        ----------
        surface : pygame.Display
            surface to display text on
        text : str
            text on button
        selected : bool
            True if button is currently selected (affects text color)
        """
        if self.active:
            color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR
        else:
            color = UI_BORDER_COLOR

        # text
        text_surf = self.font.render(text, False, color)
        text_rect = text_surf.get_rect(center=self.rect.center)

        # draw
        surface.blit(text_surf, text_rect)

    def trigger(self, create_level, exit_game):
        """
        Method to trigger function according to button pressed. Is able to create level or leave the game.

        Parameters
        ----------
        create_level : def
            method to set up selected level
        exit_game : def
            method to exit the game
        """
        selection = menu_dict[self.menu_type][self.index]

        # select level to play
        if selection != 'Exit' and self.active:
            create_level(self.index)
        # exit
        elif selection == 'Exit':
            exit_game()

    def display(self, surface, selection_num, text):
        """
        Method to display button in color of current state of selection. If active is False, button is non-clickable and
        displayed in distinguished colors.

        Parameters
        ----------
        surface : pygame.Display
            surface to display text on
        selection_num : int
            index of the currently selected button
        text : str
            displayed text
        """
        if self.active:
            if self.index == selection_num:
                pygame.draw.rect(surface, MENU_COLOR_SELECTED, self.rect)
                pygame.draw.rect(surface, BORDER_COLOR_SELECTED, self.rect, 3)
            else:
                pygame.draw.rect(surface, UI_BACKGROUND_COLOR, self.rect)
                pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 3)

            self.display_text(surface, text, self.index == selection_num)
        else:
            pygame.draw.rect(surface, MENU_COLOR_INACTIVE, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 3)

            self.display_text(surface, text, self.index == selection_num)
