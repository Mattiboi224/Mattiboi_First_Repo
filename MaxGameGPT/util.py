import Config as C
import heapq
import math
from PIL import Image

# ------------------ UTILS ------------------
def clamp(v, lo, hi):
    return max(lo, min(hi, v))

def dist(a, b):
    return math.hypot(a[0]-b[0], a[1]-b[1])

def tile_center(tx, ty):
    return tx * C.TILE + C.TILE//2, ty * C.TILE + C.TILE//2

def to_grid(pos):
    x, y = pos
    return int(x // C.TILE), int(y // C.TILE)

def in_bounds(tx, ty):
    return 0 <= tx < C.MAP_WIDTH and 0 <= ty < C.MAP_HEIGHT  # Adding Boundary

def is_occupied(tile_map, gx, gy):
        for w in range(len(tile_map)):
            for h in tile_map[w]:
                if h.pos() == (gx, gy):
                    if h.occupied == False:
                        return False
                    else:
                        return True

def locations_in_range(opp_range, unit):
    unit_x, unit_y = unit.pos_grid()

    opp_range = opp_range / C.TILE

    all_data_points = []

    for w in range(C.MAP_WIDTH):
        for h in range(C.MAP_HEIGHT):
            all_data_points.append((w,h))

    inside_points = []

    for (x,y) in all_data_points:
        if (x - unit_x) ** 2 + (y - unit_y) ** 2 <= opp_range ** 2:
            inside_points.append((x,y))

    return inside_points

def convert_image_to_team(image_used, team_number, unit_type):
    image = Image.open(image_used).convert("RGBA")
    pixels = list(image.getdata())

    if unit_type == "soldier":
        old = C.SOLDIER_OLD
    elif unit_type == "tank":
        old = C.TANK_OLD
    elif unit_type == "ammo_truck":
        old = C.AMMO_TRUCK_OLD
    elif unit_type == "barracks":
        old = C.BARRACKS_OLD
    elif unit_type == "tank_factory":
        old = C.TANK_FACTORY_OLD
    elif unit_type == "base":
        old = C.BASE_OLD
    elif unit_type == "construction":
        old = C.CONSTRUCTION_OLD
    elif unit_type == "storage_unit":
        old = C.STORAGE_UNIT_OLD
    elif unit_type == "fuel_tank":
        old = C.FUEL_TANK_OLD
    elif unit_type == "gold_vault":
        old = C.GOLD_VAULT_OLD    

    new = C.TEAM_COLORS[team_number]
    bg_colour = (0, 0, 0, 255)    

    updated = [
        (0, 0, 0, 0) if p == bg_colour                 # transparent if background
        else new if p[:3] == old[:3]                    # recoloured if team colour
        else p                                          # unchanged otherwise
        for p in pixels
    ]

    out = Image.new("RGBA", image.size)
    out.putdata(updated)                    # Fix 2: write the updated pixels into out
    return out

# ------------------ PATHFINDING ------------------
def astar(grid, start, goal, occupied_tiles=set(), passable=lambda t: t != C.T_WALL and t != C.T_WATER):
    sx, sy = start
    gx, gy = goal
    if not in_bounds(gx, gy) or not passable(grid[gy][gx]):
        return []
    if start == goal:
        return [start]

    open_set = []
    heapq.heappush(open_set, (0, start))
    came = {start: None}
    g = {start: 0}
    dirs = [(1,0),(-1,0),(0,1),(0,-1),   # cardinal
            (1,1),(1,-1),(-1,1),(-1,-1)]  # diagonal

    while open_set:
        _, cur = heapq.heappop(open_set)
        if cur == goal:
            path = []
            while cur:
                path.append(cur)
                cur = came[cur]
            path.reverse()
            return path

        cx, cy = cur
        for dx, dy in dirs:
            nx, ny = cx + dx, cy + dy

            if not in_bounds(nx, ny):
                continue

            # 🧱 static obstacle check
            if not passable(grid[ny][nx]):
                continue

            # 🚶 dynamic obstacle check
            if (nx, ny) in occupied_tiles:
                continue

            # 📐 prevent clipping through wall corners on diagonals
            if dx != 0 and dy != 0:
                if not passable(grid[cy][nx]) or not passable(grid[ny][cx]):
                    continue

            nd = g[cur] + (1.414 if dx != 0 and dy != 0 else 1)
            if (nx, ny) not in g or nd < g[(nx, ny)]:
                g[(nx, ny)] = nd
                came[(nx, ny)] = cur
                dx_h, dy_h = abs(nx - gx), abs(ny - gy)
                h = 1.414 * min(dx_h, dy_h) + abs(dx_h - dy_h)
                heapq.heappush(open_set, (nd + h, (nx, ny)))

    return []