"""
Hybrid random map generator: Perlin noise base + cellular automata smoothing.
Outputs a color-keyed PNG (and/or a raw pixel array) ready to feed into
a GridMap loader.

Requires: pip install opensimplex numpy pillow
"""

import random
import numpy as np
from PIL import Image
from opensimplex import OpenSimplex
import Config as C

# ---- Config ----------------------------------------------------------

SIZE = C.SIZE          # map is SIZE x SIZE tiles
CELL = C.CELL           # pixels per tile in the output PNG (set to 1 for a
                    # literal 1px-per-tile map file)
NUM_SPAWNS = C.NO_OF_SPAWNS
MIN_SPAWN_DIST = C.MIN_SPAWN_DIST
EDGE_MARGIN = C.EDGE_MARGIN     # min tiles from map border a spawn can be placed

NOISE_SCALE = 22.0      # bigger = smoother/larger landmasses
NOISE_OCTAVES = 3
NOISE_PERSISTENCE = 0.55
NOISE_LACUNARITY = 2.0
WATER_THRESHOLD = -0.02 # lower = less water

SMOOTH_PASSES = 2        # cellular automata cleanup passes

# Colour key -- match these to your engine's loader
WATER = (58, 102, 173)
GRASS = (86, 152, 62)
SPAWN = (219, 62, 54)


# ---- Generation --------------------------------------------------------

def generate_water_mask(seed: int) -> np.ndarray:
    """Simplex noise thresholded into a boolean water/land mask.

    OpenSimplex has no built-in octaves/persistence support like the
    old `noise` library did, so octaves are summed manually here to
    get the same layered "fractal noise" look.
    """
    gen = OpenSimplex(seed=seed)
    mask = np.zeros((SIZE, SIZE), dtype=bool)
    for y in range(SIZE):
        for x in range(SIZE):
            amplitude = 1.0
            frequency = 1.0
            total = 0.0
            max_amplitude = 0.0
            for _ in range(NOISE_OCTAVES):
                total += gen.noise2(
                    x / NOISE_SCALE * frequency,
                    y / NOISE_SCALE * frequency,
                ) * amplitude
                max_amplitude += amplitude
                amplitude *= NOISE_PERSISTENCE
                frequency *= NOISE_LACUNARITY
            n = total / max_amplitude  # normalize back to roughly [-1, 1]
            mask[y, x] = n < WATER_THRESHOLD
    return mask


def smooth_mask(mask: np.ndarray, passes: int = SMOOTH_PASSES) -> np.ndarray:
    """Cellular-automata majority smoothing to remove stray speckle
    and clean up jagged coastlines left by raw noise thresholding."""
    for _ in range(passes):
        new_mask = mask.copy()
        for y in range(SIZE):
            for x in range(SIZE):
                water_neighbors = 0
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        if dy == 0 and dx == 0:
                            continue
                        yy, xx = y + dy, x + dx
                        if 0 <= yy < SIZE and 0 <= xx < SIZE:
                            water_neighbors += mask[yy, xx]
                # slightly asymmetric threshold: water tiles need fewer
                # water neighbors to survive than land tiles need to flip
                if mask[y, x]:
                    new_mask[y, x] = water_neighbors >= 5
                else:
                    new_mask[y, x] = water_neighbors >= 6
        mask = new_mask
    return mask


def place_spawns(is_grass: np.ndarray, water_mask: np.ndarray,
                  n: int = NUM_SPAWNS,
                  min_dist: int = MIN_SPAWN_DIST,
                  edge_margin: int = EDGE_MARGIN) -> list[tuple[int, int]]:
    """Greedily pick spawn tiles on grass that are mutually far apart,
    at least `edge_margin` tiles from the map border, and not touching
    water (checked over the 8 surrounding neighbors)."""

    def touches_water(y: int, x: int) -> bool:
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                yy, xx = y + dy, x + dx
                if 0 <= yy < SIZE and 0 <= xx < SIZE and water_mask[yy, xx]:
                    return True
        return False

    candidates = [
        (y, x) for y, x in zip(*np.where(is_grass))
        if edge_margin <= y < SIZE - edge_margin
        and edge_margin <= x < SIZE - edge_margin
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


def generate_map(seed: int | None = None) -> tuple[np.ndarray, list[tuple[int, int]]]:
    """Returns (SIZE x SIZE x 3 uint8 array, list of spawn (y, x) tiles)."""
    if seed is None:
        seed = random.randint(0, 999_999)
    random.seed(seed)

    water_mask = generate_water_mask(seed)
    water_mask = smooth_mask(water_mask)
    is_grass = ~water_mask

    arr = np.zeros((SIZE, SIZE, 3), dtype='uint8')
    arr[water_mask] = WATER
    arr[is_grass] = GRASS

    spawns = place_spawns(is_grass, water_mask)
    for (y, x) in spawns:
        arr[y, x] = SPAWN

    return arr, spawns


def save_png(arr: np.ndarray, path: str, cell: int = CELL) -> None:
    img = Image.fromarray(arr, 'RGB')
    if cell != 1:
        img = img.resize((SIZE * cell, SIZE * cell), Image.NEAREST)
    img.save(path)


if __name__ == "__main__":
    tile_array, spawn_points = generate_map(seed=None)
    save_png(tile_array, "hybrid_map.png")
    print(f"Generated {SIZE}x{SIZE} map with spawns at: {spawn_points}")

    # If you want to skip the disk round-trip entirely and feed straight
    # into your GridMap loader, just pass `tile_array` (or a 1px-per-tile
    # version via save_png(..., cell=1)) directly to whatever function
    # currently loads your PNG.