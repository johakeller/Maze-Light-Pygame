import pygame

from settings import *
from support import import_folder


class Tile(pygame.sprite.Sprite):
    """
    A class to create a sprite with certain dimensions as a tile from an image, is required since tiled-editor was used
    to create the map. Defines position of the tile on the screen.

    Parameters
    ----------
    pos, groups, sprite_type, surface
    pos : (x,y)
        determines position of the sprite
    groups : list
        determines the sprite groups the sprite belongs to
    sprite_type : str
        type of sprite for identification
    surface: pygame.Surface
        sized surface for tile

    Attributes
    ----------
    sprite_type : str
        see Parameters
    image : pygame.Surface
        sized surface for tile
    rect : pygame.Rect
        determines position of surface
    hitbox : pygame.Rect
        inflated Rect for environment interaction
    """

    def __init__(self, pos, groups, sprite_type, surface=pygame.Surface((TILE_SIZE, TILE_SIZE))):
        super().__init__(groups)
        offset_x = pos[0] + (TILE_SIZE / 2)
        offset_y = pos[1] + (TILE_SIZE / 2)
        self.sprite_type = sprite_type
        self.image = surface
        self.rect = self.image.get_rect(center=(offset_x, offset_y))
        self.hitbox = self.rect.inflate(0, -10)


class AnimatedTile(Tile):
    """
    A class to create a sprite with an animation. Defines position of the tile on the screen.

    Parameters
    ----------
    pos, groups, sprite_type, surface
    pos : (x,y)
        determines position of the player-sprite
    groups : list
        determines the sprite groups the player belongs to
    sprite_type : str
        type of sprite for identification
    surface: pygame.Surface
        sized surface for tile

    Attributes
    ----------
    animations : list
        images from folder to be displayed
    frame_index : int
        index of the image to be displayed
    image : pygame.Surface
        self.rect = self.image.get_rect(center=(offset_x, offset_y))
        self.hitbox = self.rect.inflate(0, -10)
    image : pygame.Surface
        surface form animations list with index frame_index
    """

    def __init__(self, pos, groups, sprite_type, surface, path):
        super().__init__(pos, groups, sprite_type, surface)
        self.animations = import_folder(path)
        self.frame_index = 0
        self.image = self.animations[self.frame_index]

    def animate(self):
        """
        Method to display tile animation, loops over the content of animations list.
        """
        self.frame_index += 0.05
        if int(self.frame_index) == len(self.animations):
            self.frame_index = 0
        self.image = self.animations[int(self.frame_index)]

    def update(self):
        """
        Method to update animated tile. Calls animate().
        """
        self.animate()
