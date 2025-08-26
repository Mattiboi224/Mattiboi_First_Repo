import util as m
import random
import pygame
import Config as C

# ------------------ GRID/MAP ------------------
class GridMap:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.tiles = [[C.T_GRASS for _ in range(w)] for _ in range(h)]
        # scatter some walls/resources
        for _ in range(150):
            x = random.randrange(w)
            y = random.randrange(h)
            self.tiles[y][x] = random.choice([C.T_GRASS, C.T_GRASS, C.T_GRASS, C.T_WALL, C.T_RESOURCE])

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

    def resource_tile_properties(self):
        if Game.grid.tiles[y][x] == C.T_RESOURCE:
            self.resource_value = C.RESOURCE_HEALTH