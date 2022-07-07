from csv import reader
from os import walk

import pygame

from settings import TILE_SIZE


def import_folder(path):
    """
    A support-method for reading the content of an image-directory with a given path and returning all the images as
    surface-list.

    Parameters
    ----------
    path : str
        path of the directory

    Returns
    ----------
    list : surface list of images
    """
    surface_list = []

    for _, __, image_files in walk(path):
        for image in image_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list


def import_csv_layout(path):
    """
    A support-method for reading the content csv-file and append the content row-wise to a str-list which is returned.

    Parameters
    ----------
    path : str
        path of the csv-file

    Returns
    ----------
    list : list of rows from csv-file
    """
    csv_map = []
    with open(path) as object_map:
        level = reader(object_map, delimiter=',')
        for row in level:
            csv_map.append(list(row))
    return csv_map


def import_cut_graphics(path):
    """
    A support-method providing compatibility with the tiled-editor. Image has to be cut in tiles according to the usage
    of the tiles in the editor. Surfaces with image-parts are returned in list.

    Parameters
    ----------
    path : str
        path of the csv-file

    Returns
    ----------
    list : surface list of image-parts
    """
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / TILE_SIZE)
    tile_num_y = int(surface.get_size()[1] / TILE_SIZE)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            new_surf = pygame.Surface((TILE_SIZE, TILE_SIZE), flags=pygame.SRCALPHA)
            new_surf.blit(surface, (0, 0), pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
            cut_tiles.append(new_surf)
    return cut_tiles
