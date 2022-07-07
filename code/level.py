import pygame

from game_data import levels
from message import Message
from particles import ParticleEffect
from player import Player
from settings import TILE_SIZE
from souleater import Souleater
from support import import_csv_layout, import_cut_graphics
from tiles import Tile, AnimatedTile
from ui import UI


class Level:
    """
    A class to run the current level, includes methods to set up the level and bundles functionalities for central
    gameplay control like position of objects as player, enemies and environment, menus and win, pause or game over.

    Parameters
    ----------
    current_level : int
        number of the currently running level
    surface : pygame.Display
        surface to display level
    create_menu : def
        method to create new menu

    Attributes
    ----------
    max_level : int
        maximum unlocked level
    display_surface : pygame.Display
        surface to display level
    current_level : int
        index of the currently running level
    level_data : dict
        entry for each level with csv path for level set up and additional information
    new_max_level : int
        index of level to be unlocked after winning the current level
    create_menu : def
        method to create and display menu-object
    game_paused : bool
        True if game is paused
    game_over : bool
        True if player health equals 0
    win : bool
        True if player hitbox collides with goal-sprite
    souleater : Souleater
        instance of souleater-object (enemy)
    player : Player
        instance of player-object
    visible_sprites : CameraGroup
        modified sprite.Group for display of tiles with player-movement-offset
    obstacle_sprites : pygame.sprite.Group
        group of sprites for collision detection
    create_map() : method call
        place sprites on display surface
    ui : UI
        user-interface-object gives access to user interface
    message : Message
        game interruption message
    menu : Menu
        to display main menu
    """
    def __init__(self, current_level, surface, create_menu):
        # general setup
        self.max_level = 0
        self.display_surface = surface
        self.current_level = current_level
        self.level_data = levels[current_level]
        self.new_max_level = self.level_data['unlock']
        self.create_menu = create_menu

        # game status
        self.game_paused = False
        self.game_over = False
        self.win = False

        # sprite set up
        self.souleater = None
        self.player = None
        self.visible_sprites = CameraGroup(self.level_data)
        self.obstacle_sprites = pygame.sprite.Group()
        self.create_map()

        # user interface
        self.ui = UI()
        self.message = None
        self.menu = None

        # sound
        self.game_over_sound = pygame.mixer.Sound('../audio/game_over.wav')
        self.game_over_sound.set_volume(0.4)
        self.win_sound = pygame.mixer.Sound('../audio/win.wav')
        self.win_sound.set_volume(0.4)
        self.enemy_attack_sound = pygame.mixer.Sound('../audio/souleater_attack.wav')
        self.enemy_attack_sound.set_volume(0.4)
        self.button_sound = pygame.mixer.Sound('../audio/button.wav')
        self.button_sound.set_volume(0.4)

    def create_map(self):
        """
        Method to import csv layouts by calling method import_csv_layout() from support.py and creating map by
        placing sprites and objects accordingly to the csv_layout. Loops through each entry in dict layouts and
        creates map according to csv-entry-values.
        """
        layouts = {
            'walls': import_csv_layout(self.level_data['walls']),
            'player': import_csv_layout(self.level_data['player']),
            'flowers': import_csv_layout(self.level_data['flowers']),
            'coins': import_csv_layout(self.level_data['coins']),
            'enemies': import_csv_layout(self.level_data['enemies'])
        }

        for style, layout in layouts.items():
            # loop over each row in csv layout
            for row_index, row in enumerate(layout):
                # loop over each value in row
                for col_index, col in enumerate(row):
                    if col != '-1':
                        # determine position on display surface
                        x = col_index * TILE_SIZE
                        y = row_index * TILE_SIZE

                        # enemies
                        if style == 'enemies':
                            if col == '0':
                                self.souleater = Souleater((x, y), [self.visible_sprites], self.obstacle_sprites,
                                                           self.damage_player)

                        if style == 'player':
                            if col == '0':
                                self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites)
                            if col == '1':
                                tile_surface = pygame.image.load('../graphics/player/ring.png').convert_alpha()
                                Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'goal', tile_surface)

                        if style == 'walls':
                            terrain_tile_list = import_cut_graphics('../graphics/terrain/wall_tiles.png')
                            tile_surface = terrain_tile_list[int(col)]  # read id
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'static', tile_surface)

                        if style == 'flowers':
                            tile_surface = pygame.image.load('../graphics/flowers/1.png').convert_alpha()
                            AnimatedTile((x, y), [self.visible_sprites, self.obstacle_sprites], 'flower', tile_surface,
                                         '../graphics/flowers')

                        if style == 'coins':
                            if col == '0':
                                tile_surface = pygame.image.load('../graphics/coins/gold/0.png').convert_alpha()
                                AnimatedTile((x, y), [self.visible_sprites, self.obstacle_sprites], 'gold',
                                             tile_surface, '../graphics/coins/gold')
                            else:
                                tile_surface = pygame.image.load('../graphics/coins/silver/0.png').convert_alpha()
                                AnimatedTile((x, y), [self.visible_sprites, self.obstacle_sprites], 'silver',
                                             tile_surface, '../graphics/coins/silver')

    def damage_player(self, damage):
        """
        Method to inflict damage on the player object. Called when enemy is attacking player and player can be
        attacked. Provides access to player health attributes via global player-object. After attack player
        hurt_time is set, so next attack has to wait for timer to finish.
        """
        if self.player.vulnerable:
            pygame.mixer.find_channel(True).play(self.enemy_attack_sound)
            self.player.health -= damage
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            ParticleEffect(self.player.rect.center, [self.visible_sprites])

    def check_paused(self):
        """
        Method to inflict damage on the player object. Called when enemy is attacking player and player can be attacked.
        Provides access to player health attributes via global player-object. After attack player hurt_time is set, so
        next attack has to wait for timer to finish.
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_m]:
            self.button_sound.play()
            self.game_paused = not self.game_paused
            self.message = Message(self.display_surface, self.current_level, self.max_level, 'paused', self.pause_game,
                                   self.set_game_over, self.set_win, self.player.coins)

    def check_death(self):
        """
        Method to check game over state, if health of player is smaller equals 0, game is paused and game over
        message is created
        """
        if self.player.health <= 0:
            pygame.mixer.find_channel(True).play(self.game_over_sound)
            self.game_paused = True
            self.message = Message(self.display_surface, self.current_level, self.max_level, 'game_over',
                                   self.pause_game, self.set_game_over, self.set_win, self.player.coins)

    def set_game_over(self):
        """
        Setter-method for game_over
        """
        self.game_over = True

    def check_win(self):
        """
        Method to check win state in player (if he reached the goal), if True, game is paused and win message is
        created.
        """
        if self.player.player_win:
            pygame.mixer.find_channel(True).play(self.win_sound)
            self.game_paused = True
            self.message = Message(self.display_surface, self.current_level, self.max_level, 'win', self.pause_game,
                                   self.set_game_over, self.set_win, self.player.coins)

    def set_win(self):
        """
        Setter-method for win
        """
        self.win = True

    def pause_game(self):
        """
        Switch-method for game_paused, if called changes game_paused to the current opposite.
        """
        self.game_paused = not self.game_paused

    def run(self):
        """
        Run-method for level. Displays current position of each object and user interface. Checks for win state,
        game_over state and paused state to display either message or return to main menu if game has ended. If not
        updates all level elements and checks whether to run messages for win, game_over or paused.
        """
        self.visible_sprites.camera_draw(self.player)
        self.ui.display(self.player)

        if self.win:
            self.menu = self.create_menu(self.current_level, self.new_max_level)
        if self.game_over:
            self.menu = self.create_menu(self.current_level, self.max_level)
        if self.game_paused:
            self.message.run()
        else:
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.check_paused()
            self.check_win()
            self.check_death()


class CameraGroup(pygame.sprite.Group):
    """
    A class derived from pygame.sprite.Group to display all sprites in the group with the offset from the current player
    movement to the display surface to provide a camera function, that moves along with the player, maintaining the
    player in the center.

    Parameters
    ----------
    level_data : dict
        entry for each level with csv path for level set up and additional information like path to floor image

    Attributes
    ----------
    display_surface : pygame.Display
        surface to display CameraGroup-objects
    half_width : int
        x position of center of screen
    half_height : int
        y position of center of screen
    offset : (x,y)
        offset vector from player.rect.center to center of screen
    floor_surface : pygame.Image
        floor image
    floor_rect : pygame.Rect
        floor rect
    """
    def __init__(self, level_data):
        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # floor
        self.floor_surface = pygame.image.load(level_data['floor']).convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    def camera_draw(self, player):
        """
        A class derived from pygame.sprite.Group to display all sprites in the group with the offset from the current
        player movement to the display surface to provide a camera function, that moves along with the player,
        maintaining the player in the center. Sprites a sorted by their y-value before display to make lower sprites
        appear in front of higher sprites.

        Parameters
        ----------
        player : Player
            player-object
        """
        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)

        # sort sprites by y-value before display:
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        """
        Help-method to update the enemy sprites separately after all the visible sprites have been updated to make
        enemies be able to react on player behaviour.
        """
        enemy_sprites = [sprite for sprite in self.sprites() if
                         hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'souleater']
        for sprite in enemy_sprites:
            sprite.enemy_update(player)
