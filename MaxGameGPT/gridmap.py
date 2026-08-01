
import util as m
import random
import pygame
import Config as C
from tiles import Tiles
from PIL import Image
from collections import Counter
from opensimplex import OpenSimplex
import numpy as np

# ------------------ GRID/MAP ------------------
class GridMap:
    def __init__(self):

        # Map or No Map
        RESOURCE_MAP = False

        # Make your own maps
        # image = Image.open(C.GAME_MAP)

        # map_width, map_height = image.size

        if C.AUTO_GENERATE_MAP:
            tile_array, spawn_points = self.generate_map(seed=None)
            self.save_png(tile_array, C.GENERATED_MAP)
            print(f"Generated {C.SIZE}x{C.SIZE} map with spawns at: {spawn_points}")
            image = Image.open(C.MAP_PATH)
            MAP_WIDTH, MAP_HEIGHT = image.size

        else:
            image = Image.open(C.MAP_PATH)
            MAP_WIDTH, MAP_HEIGHT = image.size

        self.w = MAP_WIDTH
        self.h = MAP_HEIGHT
        self.tiles = [[C.T_GRASS for _ in range(self.w)] for _ in range(self.h)]
        self.resource_tiles = [[C.T_GRASS for _ in range(self.w)] for _ in range(self.h)]
        self.resource_amounts = [[C.T_GRASS for _ in range(self.w)] for _ in range(self.h)]

        
        # Get Game Map
        pixels = list(image.getdata())        
        rgb_pixel = [t[:3] for t in pixels]
        self.spawns = []
        
        for i in range(self.h):
            for j in range(self.w):
                for key, value in C.TILE_COLORS.items():
                    if value == rgb_pixel[j + i * self.w]:

                        # If Spawn, Note it and change it back grass
                        if key == C.T_PLAYER_LOC:
                        #    key = 1
                            self.spawns.append((j,i))
                            key = C.T_GRASS
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
                            if key == C.T_WATER:
                                resource_amount = 0
                            
                            elif key in (C.T_RESOURCE, C.T_FUEL) and (j, i) not in self.spawns:
                                resource_amount = random.randint(1, 8)
                            elif key in (C.T_RESOURCE, C.T_FUEL) and (j, i) in self.spawns:
                                resource_amount = 15
                            elif key == C.T_GOLD and (j, i) not in self.spawns:
                                resource_amount = random.randint(1, 4)
                            
                            self.resource_tiles[i][j] = key
                            self.resource_amounts[i][j] = resource_amount
        
        else:
            # Random Resource Spawn
            RESOURCE_DENSITY = 0.12  # % of tiles that get a resource
            RESOURCE_TYPES = [C.T_RESOURCE, C.T_FUEL, C.T_GOLD]  # weight these however you like
            RESOURCE_WEIGHTS = [1, 1, 1]

            for i in range(self.h):
                for j in range(self.w):

                    if (j, i) in self.spawns:
                        # Spawn tiles always get a guaranteed resource
                        key = C.T_RESOURCE
                        resource_amount = 15

                    elif (j - 1, i - 1) in self.spawns:
                        # Giving Starting Fuel
                        key = C.T_FUEL
                        resource_amount = 6

                    elif random.random() < RESOURCE_DENSITY:
                        key = random.choices(RESOURCE_TYPES, weights=RESOURCE_WEIGHTS, k=1)[0]

                        if key in (C.T_RESOURCE, C.T_FUEL):
                            resource_amount = random.randint(1, 12)
                        elif key == C.T_GOLD:
                            resource_amount = random.randint(1, 4)

                    else:
                        key = C.T_BLANK
                        resource_amount = 0

                    self.resource_tiles[i][j] = key
                    self.resource_amounts[i][j] = resource_amount

        self.count = 0

    @property
    def get_tile(self):
        return self.x, self.y

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
    

    def generate_water_mask(self, seed: int) -> np.ndarray:
        """Simplex noise thresholded into a boolean water/land mask.

        OpenSimplex has no built-in octaves/persistence support like the
        old `noise` library did, so octaves are summed manually here to
        get the same layered "fractal noise" look.
        """
        gen = OpenSimplex(seed=seed)
        mask = np.zeros((C.SIZE, C.SIZE), dtype=bool)
        for y in range(C.SIZE):
            for x in range(C.SIZE):
                amplitude = 1.0
                frequency = 1.0
                total = 0.0
                max_amplitude = 0.0
                for _ in range(C.NOISE_OCTAVES):
                    total += gen.noise2(
                        x / C.NOISE_SCALE * frequency,
                        y / C.NOISE_SCALE * frequency,
                    ) * amplitude
                    max_amplitude += amplitude
                    amplitude *= C.NOISE_PERSISTENCE
                    frequency *= C.NOISE_LACUNARITY
                n = total / max_amplitude  # normalize back to roughly [-1, 1]
                mask[y, x] = n < C.WATER_THRESHOLD
        return mask


    def smooth_mask(self, mask: np.ndarray, passes: int = C.SMOOTH_PASSES) -> np.ndarray:
        """Cellular-automata majority smoothing to remove stray speckle
        and clean up jagged coastlines left by raw noise thresholding."""
        for _ in range(passes):
            new_mask = mask.copy()
            for y in range(C.SIZE):
                for x in range(C.SIZE):
                    water_neighbors = 0
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            if dy == 0 and dx == 0:
                                continue
                            yy, xx = y + dy, x + dx
                            if 0 <= yy < C.SIZE and 0 <= xx < C.SIZE:
                                water_neighbors += mask[yy, xx]
                    # slightly asymmetric threshold: water tiles need fewer
                    # water neighbors to survive than land tiles need to flip
                    if mask[y, x]:
                        new_mask[y, x] = water_neighbors >= 5
                    else:
                        new_mask[y, x] = water_neighbors >= 6
            mask = new_mask
        return mask


    def place_spawns(self, is_grass: np.ndarray, water_mask: np.ndarray,
                    n: int = C.NO_OF_SPAWNS,
                    min_dist: int = C.MIN_SPAWN_DIST,
                    edge_margin: int = C.EDGE_MARGIN) -> list[tuple[int, int]]:
        """Greedily pick spawn tiles on grass that are mutually far apart,
        at least `edge_margin` tiles from the map border, and not touching
        water (checked over the 8 surrounding neighbors)."""

        def touches_water(y: int, x: int) -> bool:
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    yy, xx = y + dy, x + dx
                    if 0 <= yy < C.SIZE and 0 <= xx < C.SIZE and water_mask[yy, xx]:
                        return True
            return False

        candidates = [
            (y, x) for y, x in zip(*np.where(is_grass))
            if edge_margin <= y < C.SIZE - edge_margin
            and edge_margin <= x < C.SIZE - edge_margin
            and not touches_water(y, x)
        ]
        random.shuffle(candidates)

        spawns: list[tuple[int, int]] = []
        for p in candidates:
            if all((p[0] - s[0]) ** 2 + (p[1] - s[1]) ** 2 >= min_dist ** 2
                for s in spawns):
                spawns.append(p)
            if len(spawns) >= n:
                break

        # Fallback: if the map is too cramped/watery to fit `n` spawns at
        # min_dist apart, relax the distance requirement rather than
        # silently returning fewer spawns than requested.
        if len(spawns) < n and candidates:
            spawns = []
            relaxed_dist = min_dist
            while len(spawns) < n and relaxed_dist > 0:
                spawns = []
                for p in candidates:
                    if all((p[0] - s[0]) ** 2 + (p[1] - s[1]) ** 2 >= relaxed_dist ** 2
                        for s in spawns):
                        spawns.append(p)
                    if len(spawns) >= n:
                        break
                relaxed_dist -= 2

        return spawns


    def generate_map(self, seed: int | None = None) -> tuple[np.ndarray, list[tuple[int, int]]]:
        """Returns (SIZE x SIZE x 3 uint8 array, list of spawn (y, x) tiles)."""
        if seed is None:
            seed = random.randint(0, 999_999)
        random.seed(seed)

        water_mask = self.generate_water_mask(seed)
        water_mask = self.smooth_mask(water_mask)
        is_grass = ~water_mask

        arr = np.zeros((C.SIZE, C.SIZE, 3), dtype='uint8')
        arr[water_mask] = C.TILE_COLORS[C.T_WATER]
        arr[is_grass] = C.TILE_COLORS[C.T_GRASS]

        spawns = self.place_spawns(is_grass, water_mask)
        for (y, x) in spawns:
            arr[y, x] = C.TILE_COLORS[C.T_PLAYER_LOC]

        return arr, spawns


    def save_png(self, arr: np.ndarray, path: str, cell: int = C.CELL) -> None:
        img = Image.fromarray(arr, 'RGB')
        if cell != 1:
            img = img.resize((C.SIZE * cell, C.SIZE * cell), Image.NEAREST)
        img.save(path)