import pygame
from support import import_folder
from settings import horizontal_tile_numer
import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface=pygame.Surface((TILE_SIZE, TILE_SIZE))):
        super().__init__(groups)
        offset_x = pos[0] + (TILE_SIZE / 2)
        offset_y = pos[1] + (TILE_SIZE / 2)
        self.sprite_type = sprite_type
        self.image = surface
        self.rect = self.image.get_rect(center=(offset_x, offset_y))
        self.hitbox = self.rect.inflate(0, -10)

class AnimatedTile(Tile):
    def __init__(self, pos, groups, sprite_type, surface, path):
        super().__init__(pos, groups, sprite_type, surface)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

    def animate(self):
        self.frame_index += 0.05
        if int(self.frame_index) == len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()



