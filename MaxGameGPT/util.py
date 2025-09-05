import Config as C
import heapq
import math

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
    return 0 <= tx < C.GRID_W and 0 <= ty < C.GRID_H - 1 # Adding Boundary

# ------------------ PATHFINDING ------------------
def astar(grid, start, goal, passable=lambda t: t != C.T_WALL):
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
    dirs = [(1,0),(-1,0),(0,1),(0,-1)]
    while open_set:
        _, cur = heapq.heappop(open_set)
        if cur == goal:
            # reconstruct
            path = []
            while cur:
                path.append(cur)
                cur = came[cur]
            path.reverse()
            return path
        cx, cy = cur
        for dx, dy in dirs:
            nx, ny = cx + dx, cy + dy
            if not in_bounds(nx, ny): continue
            if not passable(grid[ny][nx]): continue
            nd = g[cur] + 1
            if (nx, ny) not in g or nd < g[(nx, ny)]:
                g[(nx, ny)] = nd
                came[(nx, ny)] = cur
                h = abs(nx-gx) + abs(ny-gy)
                heapq.heappush(open_set, (nd + h, (nx, ny)))
    return []