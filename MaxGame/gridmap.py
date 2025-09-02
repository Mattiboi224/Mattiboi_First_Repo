import pygame
import Constants as c
from tiles import Tiles

class GridMap:
    def __init__(self, screen_width, screen_height):
        self.w = screen_width
        self.h = screen_height

    def draw(self, surf):
        for y in range(self.h):
            for x in range(self.w):
                pygame.draw.rect(surf, c.C_GRASS, (x*c.x_pixel_size, y*c.y_pixel_size, c.x_pixel_size - 1, c.y_pixel_size - 1))

    def assign_tiles(self):

        tiles_list = []

        for i in range(0, c.no_of_grid_height):
            for j in range (0, c.no_of_grid_width):
                x_centre = i * c.x_pixel_size + c.x_pixel_size / 2
                y_centre = j * c.y_pixel_size + c.y_pixel_size / 2

                tiles_list.append(Tiles(x_centre, y_centre, "land", i + 1, j + 1))

        return tiles_list
        