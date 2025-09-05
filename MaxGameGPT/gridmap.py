import util as m
import random
import pygame
import Config as C
from tiles import Tiles
from PIL import Image
from collections import Counter

# ------------------ GRID/MAP ------------------
class GridMap:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.tiles = [[C.T_GRASS for _ in range(w)] for _ in range(h)]
        #print(w)
        #print(h)
        # scatter some walls/resources
        #for _ in range(150):
        #    x = random.randrange(w)
        #    y = random.randrange(h)
        #    self.tiles[y][x] = random.choice([C.T_GRASS, C.T_GRASS, C.T_GRASS, C.T_WALL, C.T_RESOURCE])

        # Make your own maps
        image = Image.open(C.GAME_MAP)
        pixels = list(image.getdata())
        rgb_pixel = [t[:3] for t in pixels]
        self.spawns = []
        
        for i in range(h):
            for j in range(w):
                for key, value in C.TILE_COLORS.items():
                    if value == rgb_pixel[j + (i - 1) * w]:
                        if key == 3:
                        #    key = 1
                            self.spawns.append((j,i))
                            key = 1
                        self.tiles[i][j] = key
        #print(self.tiles)
        #print(self.spawns)

    def toggle_at(self, tx, ty, ttype):
        if m.in_bounds(tx, ty):
            self.tiles[ty][tx] = ttype

    def passable(self, tx, ty):
        return m.in_bounds(tx, ty) and self.tiles[ty][tx] != C.T_WALL

    def draw(self, surf):
        for y in range(self.h):
            for x in range(self.w):
                c = C.TILE_COLORS[self.tiles[y][x]]
                pygame.draw.rect(surf, c, (x*C.TILE, y*C.TILE, C.TILE-1, C.TILE-1))

    def assign_tiles(self):
        assigned_tiles = self.tiles

        transposed = [[row[i] for row in assigned_tiles] for i in range(len(assigned_tiles[0]))]

        tile_map = [[0 for _ in range(self.h)] for _ in range(self.w)]

        #print(tile_map[22][0])


        for i in range(self.w):
            for j in range(self.h):
                tile_map[i][j] = Tiles(i, j, transposed[i][j])

        return tile_map