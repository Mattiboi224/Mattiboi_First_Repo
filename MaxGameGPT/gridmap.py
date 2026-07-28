import util as m
import random
import pygame
import Config as C
from tiles import Tiles
from PIL import Image
from collections import Counter

# ------------------ GRID/MAP ------------------
class GridMap:
    def __init__(self):

        # Map or No Map
        RESOURCE_MAP = False

        # Make your own maps
        # image = Image.open(C.GAME_MAP)

        # map_width, map_height = image.size

        self.w = C.MAP_WIDTH
        self.h = C.MAP_HEIGHT
        self.tiles = [[C.T_GRASS for _ in range(self.w)] for _ in range(self.h)]
        self.resource_tiles = [[C.T_GRASS for _ in range(self.w)] for _ in range(self.h)]
        self.resource_amounts = [[C.T_GRASS for _ in range(self.w)] for _ in range(self.h)]

        # scatter some walls/resources
        #for _ in range(150):
        #    x = random.randrange(self.w)
        #    y = random.randrange(self.h)
        #    self.tiles[y][x] = random.choice([C.T_GRASS, C.T_GRASS, C.T_GRASS, C.T_WALL, C.T_RESOURCE])
        
        # Get Game Map
        pixels = list(C.image.getdata())
        rgb_pixel = [t[:3] for t in pixels]
        self.spawns = []
        
        for i in range(self.h):
            for j in range(self.w):
                for key, value in C.TILE_COLORS.items():
                    if value == rgb_pixel[j + i * self.w]:

                        # If Spawn, Note it and change it back grass
                        if key == 3:
                        #    key = 1
                            self.spawns.append((j,i))
                            key = 0
                        self.tiles[i][j] = key

        if RESOURCE_MAP == True:
            # Get Resource Map
            image = Image.open(C.RESOURCE_MAP)
            pixels = list(image.getdata())
            rgb_pixel = [t[:3] for t in pixels]

            for i in range(self.h):
                for j in range(self.w):

                    for key, value in C.TILE_COLORS.items():
                        if value == rgb_pixel[j + i * self.w]:
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
        
        else:
            # Random Resource Spawn
            RESOURCE_DENSITY = 0.12  # % of tiles that get a resource
            RESOURCE_TYPES = [2, 4, 5]  # weight these however you like
            RESOURCE_WEIGHTS = [1, 1, 1]

            for i in range(self.h):
                for j in range(self.w):

                    if (j, i) in self.spawns:
                        # Spawn tiles always get a guaranteed resource
                        key = 2
                        resource_amount = 15

                    elif (j - 1, i - 1) in self.spawns:
                        # Giving Starting Fuel
                        key = 4
                        resource_amount = 6

                    elif random.random() < RESOURCE_DENSITY:
                        key = random.choices(RESOURCE_TYPES, weights=RESOURCE_WEIGHTS, k=1)[0]

                        if key in (2, 4):
                            resource_amount = random.randint(1, 12)
                        elif key == 5:
                            resource_amount = random.randint(1, 4)

                    else:
                        key = 6
                        resource_amount = 0

                    self.resource_tiles[i][j] = key
                    self.resource_amounts[i][j] = resource_amount

        self.count = 0

    def toggle_at(self, tx, ty, ttype):
        if m.in_bounds(tx, ty):
            self.tiles[ty][tx] = ttype

    def passable(self, tx, ty):
        return m.in_bounds(tx, ty) and self.tiles[ty][tx] != C.T_WALL and self.tiles[ty][tx] != C.T_WATER

    def iter_tiles(self):
        """Yield every Tiles object in the map, row by row."""
        for row in self.tiles:  # assuming self.tiles is a 2D list
            for tile in row:
                yield tile

    def draw(self, surf, camera_x, camera_y):
        screen_w, screen_h = surf.get_size()

        x_start = max(0, camera_x // C.TILE)
        x_end = min(self.w, (camera_x + screen_w - C.MENU_WIDTH - C.UNIT_MENU_WIDTH) // C.TILE + 1)
        y_start = max(0, camera_y // C.TILE)
        y_end = min(self.h, (camera_y + screen_h - C.BOTTOM_MENU_HEIGHT + 1) // C.TILE + 1)

        for y in range(y_start, y_end):
            for x in range(x_start, x_end):
                c = C.TILE_COLORS[self.tiles[y][x]]
                pygame.draw.rect(
                    surf, c,
                    (x * C.TILE - camera_x + C.UNIT_MENU_WIDTH, y * C.TILE - camera_y, C.TILE - 1, C.TILE - 1)
            )

    def draw_resources(self, surf, font, camera_x, camera_y):
        
        screen_w, screen_h = surf.get_size()

        x_start = max(0, camera_x // C.TILE)
        x_end = min(self.w, (camera_x + screen_w - C.MENU_WIDTH - C.UNIT_MENU_WIDTH) // C.TILE + 1)
        y_start = max(0, camera_y // C.TILE)
        y_end = min(self.h, (camera_y + screen_h - C.BOTTOM_MENU_HEIGHT + 1) // C.TILE + 1)


        for y in range(y_start, y_end):
            for x in range(x_start, x_end):

                c = C.TILE_COLORS[self.resource_tiles[y][x]]
                pygame.draw.circle(surf, c, ((x + 0.5)*C.TILE - camera_x + C.UNIT_MENU_WIDTH, (y + 0.5)*C.TILE - camera_y), C.TILE // 2 - 5, 1)
                resource_text = font.render(str(self.resource_amounts[y][x]), True, c)
                surf.blit(resource_text, ((x + 0.4)*C.TILE - camera_x + C.UNIT_MENU_WIDTH, (y + 0.4)*C.TILE - camera_y))

    def assign_tiles(self):
        assigned_tiles = self.tiles

        transposed = [[row[i] for row in assigned_tiles] for i in range(len(assigned_tiles[0]))]
        self.transposed_resources_tiles = [[row[i] for row in self.resource_tiles] for i in range(len(self.resource_tiles[0]))]
        self.transposed_resources_amounts = [[row[i] for row in self.resource_amounts] for i in range(len(self.resource_amounts[0]))]

        tile_map = [[0 for _ in range(self.h)] for _ in range(self.w)]

        for i in range(self.w):
            for j in range(self.h):
                if (i, j) in self.spawns:
                    resource_amount = 15
                else:
                    resource_amount = self.transposed_resources_amounts[i][j]
                tile_map[i][j] = Tiles(i, j, transposed[i][j], self.transposed_resources_tiles[i][j], resource_amount)
        
        self.tile_map = tile_map

        return tile_map
    
    def to_dict(self):
        sparse = []
        for y, row in enumerate(self.tile_map):
            for x, tile in enumerate(row):
                if tile is not None:
                    d = tile.to_dict()
                    d["x"], d["y"] = x, y
                    sparse.append(d)
        return {"w": self.w, "h": self.h, "tiles": sparse}


    #land_type: int
    #resource_type: str
    #resource_amount: int

    @classmethod
    def from_dict(cls, d):
        gm = cls()
        gm.w = d["w"]
        gm.h = d["h"]
        gm.tile_map = [[None for _ in range(gm.w)] for _ in range(gm.h)]
        for td in d["tiles"]:
            x, y = td["x"], td["y"]
            gm.tile_map[y][x] = Tiles.from_dict(td)
        return gm
    
        #     # Split fields into init-accepted vs init=False
        # init_fields = {f.name for f in fields(cls) if f.init}
        # non_init_fields = [f.name for f in fields(cls) if not f.init]

        # # Build the object using only what __init__ accepts
        # filtered = {k: v for k, v in d.items() if k in init_fields}
        # obj = cls(**filtered)

        # # Restore whatever __post_init__ would've computed, using saved values instead
        # for name in non_init_fields:
        #     if name in d:
        #         setattr(obj, name, d[name])
