import sys

import pygame

from enemy import Enemy
from particles import ParticleEffect
from player import Player
from settings import TILE_SIZE
from support import import_csv_layout, import_cut_graphics
from tiles import Tile, AnimatedTile
from ui import UI
from game_data import levels
from menu import Menu
from message import Message


class Level:
    def __init__(self, current_level, surface, create_menu, game_run):
        # general setup
        self.max_level = 0
        self.display_surface = surface
        self.current_level = current_level
        self.level_data = levels[current_level]
        self.new_max_level = self.level_data['unlock']
        self.create_menu = create_menu
        self.game_run = game_run

        # game status
        self.game_paused = False
        self.game_over = False
        self.win = False

        # sprite group setup
        self.visible_sprites = CameraGroup(self.level_data)
        self.obstacle_sprites = pygame.sprite.Group()
        self.visibility_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

        # user interface
        self.ui = UI()
        self.message = None
        self.menu = None

    def create_map(self):
        layouts = {
            'walls': import_csv_layout(self.level_data['walls']),
            'player': import_csv_layout(self.level_data['player']),
            'flowers': import_csv_layout(self.level_data['flowers']),
            'coins': import_csv_layout(self.level_data['coins']),
            'enemies': import_csv_layout(self.level_data['enemies'])
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILE_SIZE
                        y = row_index * TILE_SIZE

                        if style == 'enemies':
                            if col == '0':
                                self.enemy = Enemy((x, y), [self.visible_sprites], self.obstacle_sprites,
                                                   self.damage_player, self.trigger_particles)

                        if style == 'player':
                            if col == '0':
                                self.player = Player((x, y), [self.visible_sprites],self.obstacle_sprites)
                            if col == '1':
                                tile_surface = pygame.image.load('../graphics/character/ring.png').convert_alpha()
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

    def trigger_particles(self, pos):
        ParticleEffect(pos, [self.visible_sprites])

    def damage_player(self, damage):
        if self.player.vulnerable:
            self.player.health -= damage
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            ParticleEffect(self.player.rect.center, [self.visible_sprites])

    def check_paused(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_m]:
            self.pause_game()
            self.message = Message(self.display_surface, self.current_level, self.max_level, 'paused', self.pause_game,
                                   self.set_game_over, self.set_win, self.player.coins)

    def check_death(self):
        if self.player.health <= 0:
            self.game_paused = True
            self.message = Message(self.display_surface, self.current_level, self.max_level, 'game_over',
                                   self.pause_game, self.set_game_over, self.set_win, self.player.coins)

    def set_game_over(self):
        self.game_over = True

    def check_win(self):
        if self.player.player_win:
            self.game_paused = True
            self.message = Message(self.display_surface, self.current_level, self.max_level, 'win', self.pause_game,
                                   self.set_game_over, self.set_win, self.player.coins)

    def set_win(self):
        self.win = True

    def pause_game(self):
        self.game_paused = not self.game_paused

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)

        if self.win:
            self.menu = self.create_menu(self.current_level, self.new_max_level, 'start')
        if self.game_over:
            self.menu = self.create_menu(self.current_level, self.max_level, 'start')
        if self.game_paused:
            self.message.run()
        else:
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.visible_sprites.enemy_update(self.player)
            self.check_paused()
            self.check_win()
            self.check_death()


class CameraGroup(pygame.sprite.Group):
    def __init__(self, level_data):
        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # creating the floor
        self.floor_surface = pygame.image.load(level_data['floor']).convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)

        # for sprite in self.sprites() y-sort:
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if
                         hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for sprite in enemy_sprites:
            sprite.enemy_update(player)
