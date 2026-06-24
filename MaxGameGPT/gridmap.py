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
        self.resource_tiles = [[C.T_GRASS for _ in range(w)] for _ in range(h)]
        self.resource_amounts = [[C.T_GRASS for _ in range(w)] for _ in range(h)]
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
                    if value == rgb_pixel[j + i * w]:

                        # If Spawn, Note it and change it back grass
                        if key == 3:
                        #    key = 1
                            self.spawns.append((j,i))
                            key = 0
                        self.tiles[i][j] = key

        image = Image.open(C.RESOURCE_MAP)
        pixels = list(image.getdata())
        rgb_pixel = [t[:3] for t in pixels]

        for i in range(h):
            for j in range(w):

                for key, value in C.TILE_COLORS.items():
                    if value == rgb_pixel[j + i * w]:
                        if key == 6:
                            resource_amount = 0
                        
                        elif key in (2, 4) and (j, i) not in self.spawns:
                            resource_amount = random.randint(1, 8)
                        elif key in (2, 4) and (j, i) in self.spawns:
                            resource_amount = 15
                        elif key == 5 and (j, i) not in self.spawns:
                            resource_amount = random.randint(1, 4)
                        
                        self.resource_tiles[i][j] = key
                        self.resource_amounts[i][j] = resource_amount

        self.count = 0

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

    def draw_resources(self, surf, font, resource_mode):
        for y in range(self.h):
            for x in range(self.w):

                if resource_mode:
                    
                    if x == 2 and y == 2 and self.count == 0:
                        #print(self.resource_tiles[2][2])
                        #print(self.resource_amounts[2][2])
                        self.count += 1

                    if x == 2 and y == 3 and self.count == 1:
                        self.count += 1


                    c = C.TILE_COLORS[self.resource_tiles[y][x]]
                    pygame.draw.circle(surf, c, ((x + 0.5)*C.TILE, (y + 0.5)*C.TILE), C.TILE // 2 - 5, 1)
                    resource_text = font.render(str(self.resource_amounts[y][x]), True, c)
                    surf.blit(resource_text, ((x + 0.4)*C.TILE, (y + 0.4)*C.TILE))

    def assign_tiles(self):
        assigned_tiles = self.tiles

        transposed = [[row[i] for row in assigned_tiles] for i in range(len(assigned_tiles[0]))]
        self.transposed_resources_tiles = [[row[i] for row in self.resource_tiles] for i in range(len(self.resource_tiles[0]))]
        self.transposed_resources_amounts = [[row[i] for row in self.resource_amounts] for i in range(len(self.resource_amounts[0]))]

        tile_map = [[0 for _ in range(self.h)] for _ in range(self.w)]

        #print(tile_map[22][0])


        for i in range(self.w):
            for j in range(self.h):
                if (i, j) in self.spawns:
                    resource_amount = 15
                else:
                    resource_amount = self.transposed_resources_amounts[i][j]
                tile_map[i][j] = Tiles(i, j, transposed[i][j], self.transposed_resources_tiles[i][j], resource_amount)

        return tile_map