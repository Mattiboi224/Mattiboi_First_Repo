import random
import time
import turtle as Turtle
from collections import Counter
from dataclasses import dataclass, field
from enum import IntEnum
 
 
# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
 
class Tile(IntEnum):
    MOUNTAIN = -1
    WATER = -2
 
 
# ---------------------------------------------------------------------------
# Configuration dataclass — change game settings here
# ---------------------------------------------------------------------------
 
@dataclass
class Config:
    grid_width: int = 10
    grid_height: int = 10
    cell_size: int = 59          # pixels
    mountain_count: int = 7      # impassable terrain
    water_count: int = 4         # passable for attacks
 
 
# ---------------------------------------------------------------------------
# Game-state dataclass — replaces the large tuple passing pattern
# ---------------------------------------------------------------------------
 
@dataclass
class GameState:
    cfg: Config
    play_mat: list = field(default_factory=list)   # current owner of each cell
    loc_mat: list = field(default_factory=list)    # original cell ID (never changes)
    colour_mat: list = field(default_factory=list) # RGB colour per cell
    flat_mat: list = field(default_factory=list)   # 1-D view of play_mat
    countries: list = field(default_factory=list)  # list of surviving country IDs
    move: int = 0
    winning_countries: list = field(default_factory=lambda: [0])
    winning_territories: int = 0
 
 
# ---------------------------------------------------------------------------
# Display helpers (Turtle)
# ---------------------------------------------------------------------------
 
def setup_map_screen(cfg: Config) -> None:
    """Initialise the Turtle window and draw the grid."""
    x_margin = cfg.cell_size * 2.5
    y_margin = cfg.cell_size // 2
    window_w = cfg.grid_width  * cfg.cell_size + int(x_margin * 2)
    window_h = cfg.grid_height * cfg.cell_size + y_margin * 2
 
    Turtle.setup(window_w, window_h)
    Turtle.bgcolor('light grey')
    Turtle.tracer(False)
    Turtle.penup()
    Turtle.color('slate grey')
    Turtle.width(2)
 
    left   = -(cfg.grid_width  * cfg.cell_size) // 2
    bottom = -(cfg.grid_height * cfg.cell_size) // 2
 
    # Horizontal lines
    Turtle.setheading(0)
    for row in range(cfg.grid_height + 1):
        Turtle.penup()
        Turtle.goto(left, bottom + row * cfg.cell_size)
        Turtle.pendown()
        Turtle.forward(cfg.grid_width * cfg.cell_size)
 
    # Vertical lines
    Turtle.setheading(90)
    for col in range(cfg.grid_width + 1):
        Turtle.penup()
        Turtle.goto(left + col * cfg.cell_size, bottom)
        Turtle.pendown()
        Turtle.forward(cfg.grid_height * cfg.cell_size)
 
    Turtle.penup()
    Turtle.tracer(True)
 
 
def colour_square(cell_id: int, colour_source_id: int, state: GameState) -> None:
    """Fill a single grid cell with the colour of colour_source_id."""
    cfg = state.cfg
    cx, cy = find_location(colour_source_id, state.loc_mat, cfg)
    x,  y  = find_location(cell_id,          state.loc_mat, cfg)
 
    x_centre = -(cfg.cell_size * cfg.grid_width  // 2 + cfg.cell_size // 2) + (x + 1) * cfg.cell_size
    y_centre  =  (cfg.cell_size * cfg.grid_height // 2 - cfg.cell_size // 2) - (y * cfg.cell_size)
 
    r, g, b = state.colour_mat[cy][cx]
 
    Turtle.colormode(255)
    Turtle.tracer(False)
    Turtle.goto(x_centre - cfg.cell_size // 2, y_centre - cfg.cell_size // 2)
    Turtle.pendown()
    Turtle.width(1)
    Turtle.pencolor('black')
    Turtle.fillcolor(r, g, b)
    Turtle.begin_fill()
    for heading in (90, 0, 270, 180):
        Turtle.setheading(heading)
        Turtle.forward(cfg.cell_size)
    Turtle.end_fill()
    Turtle.penup()
 
    cell_value = state.play_mat[y][x]
    if cell_value == Tile.MOUNTAIN:
        for dx, dy in [(0, 0), (0.25, 0.25), (-0.25, 0.25), (0.25, -0.25), (-0.25, -0.25)]:
            draw_tree(x_centre + dx * cfg.cell_size, y_centre + dy * cfg.cell_size, cfg)
    elif cell_value == Tile.WATER:
        for dy_offset in (0, 0.25, -0.25):
            draw_wavy_line(x_centre, y_centre + dy_offset * cfg.cell_size, cfg)
 
    Turtle.tracer(True)
 
 
def draw_tree(x: float, y: float, cfg: Config) -> None:
    """Draw a small tree icon centred at (x, y)."""
    cs = cfg.cell_size
    Turtle.goto(x, y)
    Turtle.pendown()
    Turtle.width(3)
    Turtle.pencolor('brown')
    Turtle.setheading(90)
    Turtle.forward(cs // 10)
    Turtle.penup()
 
    for side in (180, 0):
        Turtle.goto(x, y + cs // 10)
        Turtle.setheading(side)
        Turtle.forward(cs // 18)
        Turtle.setheading(90)
        Turtle.forward(cs // 14)
        Turtle.dot(cs // 6, 'green')
 
    Turtle.goto(x, y + cs // 10 + cs // 10)
    Turtle.dot(cs // 6, 'green')
 
 
def draw_wavy_line(x: float, y: float, cfg: Config, curves: int = 4, radius_divisor: int = 20) -> None:
    """Draw a wavy white line to represent water."""
    cs = cfg.cell_size
    Turtle.pencolor('white')
    Turtle.width(2)
    Turtle.goto(x - cs // 3, y)
    Turtle.pendown()
    for _ in range(curves):
        Turtle.setheading(45)
        Turtle.circle(cs // -radius_divisor, extent=90)
        Turtle.circle(cs //  radius_divisor, extent=90)
    Turtle.penup()
 
 
# ---------------------------------------------------------------------------
# Grid helpers
# ---------------------------------------------------------------------------
 
def find_location(cell_id: int, loc_mat: list, cfg: Config):
    """Return (col, row) for the given cell_id in loc_mat."""
    for row in range(cfg.grid_height):
        if cell_id in loc_mat[row]:
            return loc_mat[row].index(cell_id), row
    raise ValueError(f'cell_id {cell_id} not found in loc_mat')
 
 
def get_neighbour(y: int, x: int, direction: int, cfg: Config):
    """
    Return (ny, nx) for the neighbour in the given direction with wrap-around.
    direction: 1=up, 2=down, 3=left, 4=right
    """
    if direction == 1:
        return (cfg.grid_height - 1 if y == 0 else y - 1), x
    if direction == 2:
        return (0 if y == cfg.grid_height - 1 else y + 1), x
    if direction == 3:
        return y, (cfg.grid_width - 1 if x == 0 else x - 1)
    if direction == 4:
        return y, (0 if x == cfg.grid_width - 1 else x + 1)
    raise ValueError(f'Unknown direction {direction}')
 
 
# ---------------------------------------------------------------------------
# Game setup
# ---------------------------------------------------------------------------
 
def build_game_state(cfg: Config) -> GameState:
    """Construct the initial GameState: matrices, mountain/water placement."""
    total = cfg.grid_width * cfg.grid_height
    state = GameState(cfg=cfg)
 
    # Build loc_mat and play_mat (initially every cell owns itself)
    row_loc, row_play, row_colour = [], [], []
    for n in range(1, total + 1):
        row_loc.append(n)
        row_play.append(n)
        row_colour.append((
            random.randrange(0, 256),
            random.randrange(0, 256),
            random.randrange(0, 256),
        ))
        if n % cfg.grid_width == 0:
            state.loc_mat.append(row_loc)
            state.play_mat.append(row_play)
            state.colour_mat.append(row_colour)
            row_loc, row_play, row_colour = [], [], []
 
    placed = set()
 
    # Place mountains
    for _ in range(cfg.mountain_count):
        cell = _random_unused_cell(total, placed)
        placed.add(cell)
        x, y = find_location(cell, state.loc_mat, cfg)
        state.play_mat[y][x] = Tile.MOUNTAIN
        state.colour_mat[y][x] = (150, 75, 0)
 
    # Place water tiles (not on mountains)
    for _ in range(cfg.water_count):
        cell = _random_unused_cell(total, placed)
        placed.add(cell)
        x, y = find_location(cell, state.loc_mat, cfg)
        state.play_mat[y][x] = Tile.WATER
        state.colour_mat[y][x] = (0, 0, 255)
 
    # Build flat list and countries list
    state.flat_mat = [state.play_mat[r][c]
                      for r in range(cfg.grid_height)
                      for c in range(cfg.grid_width)]
    state.countries = [v for v in state.flat_mat if v not in (Tile.MOUNTAIN, Tile.WATER)]
 
    return state
 
 
def _random_unused_cell(total: int, used: set) -> int:
    """Return a random cell ID not already in used."""
    while True:
        cell = random.randrange(1, total)
        if cell not in used:
            return cell
 
 
# ---------------------------------------------------------------------------
# Turn logic
# ---------------------------------------------------------------------------
 
def pick_attacker(state: GameState):
    """
    Randomly pick a non-terrain cell that has at least one attackable neighbour.
    Returns (country_id, col, row).
    """
    cfg = state.cfg
    max_attempts = cfg.grid_width * cfg.grid_height * 100
    for _ in range(max_attempts):
        cell = random.randrange(1, cfg.grid_width * cfg.grid_height)
        x, y = find_location(cell, state.loc_mat, cfg)
        if state.play_mat[y][x] in (Tile.MOUNTAIN, Tile.WATER):
            continue
        if can_attack(x, y, state):
            return state.play_mat[y][x], x, y
    raise RuntimeError('No valid attacker found — game may be stuck.')
 
 
def can_attack(x: int, y: int, state: GameState) -> bool:
    """
    Return True if the cell at (x, y) can reach a different (non-mountain) country,
    potentially by crossing water tiles.
    """
    cfg = state.cfg
    attacker_id = state.play_mat[y][x]
    frontier = [(y, x)]
    visited = {(y, x)}
    water_hops = 0
 
    while frontier:
        cy, cx = frontier.pop()
        cell_val = state.play_mat[cy][cx]
        is_water = (cell_val == Tile.WATER)
 
        if is_water:
            water_hops += 1
            if water_hops > cfg.water_count:
                continue
 
        for direction in range(1, 5):
            ny, nx = get_neighbour(cy, cx, direction, cfg)
            if (ny, nx) in visited:
                continue
            visited.add((ny, nx))
            neighbour_val = state.play_mat[ny][nx]
            if neighbour_val == Tile.MOUNTAIN:
                continue
            if neighbour_val == Tile.WATER:
                frontier.append((ny, nx))
            elif neighbour_val != attacker_id:
                return True
    return False
 
 
# ---------------------------------------------------------------------------
# Combat
# ---------------------------------------------------------------------------
 
def resolve_combat(attacker_id: int, x: int, y: int, state: GameState) -> None:
    """
    Attempt one attack from (x, y). Picks a random direction; steps over water.
    Updates play_mat, flat_mat, colour_mat, and countries in place.
    """
    cfg = state.cfg
    attacker_frontier = [(y, x)]
    visited_water = set()
    max_loops = cfg.grid_width * cfg.grid_height * 4
 
    for _ in range(max_loops):
        for pos in attacker_frontier:
            cy, cx = pos
            direction = random.randint(1, 4)
            ny, nx = get_neighbour(cy, cx, direction, cfg)
            neighbour_val = state.play_mat[ny][nx]
 
            # Skip self and mountains
            if neighbour_val == attacker_id or neighbour_val == Tile.MOUNTAIN:
                continue
 
            # Hop over water
            if neighbour_val == Tile.WATER:
                key = (ny, nx)
                if key not in visited_water:
                    visited_water.add(key)
                    attacker_frontier.append((ny, nx))
                continue
 
            # Valid target found — resolve the attack
            defender_id = neighbour_val
            _apply_attack(attacker_id, defender_id, ny, nx, x, y, state)
            return
 
 
def _apply_attack(attacker_id: int, defender_id: int,
                  def_y: int, def_x: int,
                  src_y: int, src_x: int,
                  state: GameState) -> None:
    """Apply the result of one successful attack."""
    cfg = state.cfg
    loc_mat = state.loc_mat
    capital_id = loc_mat[def_y][def_x]
    defeated_capital = (capital_id == defender_id)
 
    if defeated_capital:
        # Defender loses all territories
        territories_lost = 0
        for r in range(cfg.grid_height):
            for c in range(cfg.grid_width):
                if state.play_mat[r][c] == defender_id:
                    state.play_mat[r][c] = attacker_id
                    territories_lost += 1
                    colour_square(loc_mat[r][c], attacker_id, state)
        for k, v in enumerate(state.flat_mat):
            if v == defender_id:
                state.flat_mat[k] = attacker_id
        if defender_id in state.countries:
            state.countries.remove(defender_id)
        _print_fight('Defeated Base', defender_id, attacker_id,
                     capital_id, loc_mat[src_y][src_x],
                     state.move, territories_lost, len(state.countries))
    else:
        # Defender loses only this tile
        state.play_mat[def_y][def_x] = attacker_id
        colour_square(loc_mat[def_y][def_x], attacker_id, state)
        flat_index = def_y * cfg.grid_width + def_x
        state.flat_mat[flat_index] = attacker_id
        _print_fight('Attacked not defeated', defender_id, attacker_id,
                     loc_mat[def_y][def_x], loc_mat[src_y][src_x],
                     state.move, 1, len(state.countries))
 
 
# ---------------------------------------------------------------------------
# Win / leaderboard tracking
# ---------------------------------------------------------------------------
 
def check_for_winner(state: GameState) -> int:
    """Return the number of surviving 'capitals' (cells where owner == original ID)."""
    cfg = state.cfg
    count = 0
    for r in range(cfg.grid_height):
        for c in range(cfg.grid_width):
            if state.play_mat[r][c] == state.loc_mat[r][c]:
                count += 1
    return count
 
 
def update_leaderboard(state: GameState) -> None:
    """Print commentary whenever the leader changes, then update state."""
    counts = Counter(v for v in state.flat_mat if v not in (Tile.MOUNTAIN, Tile.WATER))
    if not counts:
        return
 
    top_count = counts.most_common(1)[0][1]
    new_leaders = [v for v, c in counts.most_common() if c == top_count]
    old_leaders = state.winning_countries
    old_territories = state.winning_territories
 
    _print_leading(new_leaders, top_count)
 
    if new_leaders == old_leaders and top_count == old_territories:
        print(f'{new_leaders} kept their lead')
    elif new_leaders == old_leaders:
        verb = 'extended' if top_count > old_territories else 'lost a bit of'
        print(f'{new_leaders} {verb} their lead')
    else:
        if len(new_leaders) == 1:
            print(f'{new_leaders[0]} became the leader')
        else:
            joined = [c for c in new_leaders if c not in old_leaders]
            suffix = 'leader' if len(old_leaders) == 1 else 'leaders'
            for c in joined:
                print(f'{c} joined the {suffix}')
 
    time.sleep(0.25)
    print()
    state.winning_countries = new_leaders
    state.winning_territories = top_count
 
 
def _print_leading(leaders: list, territories: int) -> None:
    if len(leaders) == 1 and territories > 1:
        print(f'{leaders[0]} is winning with {territories} territories')
    elif len(leaders) >= 2 and territories > 1:
        names = ', '.join(str(c) for c in leaders[:-1])
        print(f'{names} and {leaders[-1]} are winning with {territories} territories')
 
 
# ---------------------------------------------------------------------------
# Announcements
# ---------------------------------------------------------------------------
 
def _print_fight(event: str, defeated: int, attacker: int,
                 where: int, from_loc: int, move: int,
                 territories: int, countries_left: int) -> None:
    if event == 'Defeated Base':
        print(f'{attacker} attacked {defeated} from {from_loc}. '
              f'{defeated} lost its capital and was defeated in move {move}')
        if territories >= 2:
            print(f'They lost {territories} territories.')
    else:
        print(f'{attacker} attacked {defeated} in {where} from {from_loc} in move {move}')
 
    if countries_left > 1:
        print(f'There are {countries_left} countries left.')
 
 
# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
 
def main():
    cfg = Config()
    state = build_game_state(cfg)
 
    setup_map_screen(cfg)
 
    # Draw initial board
    for r in range(cfg.grid_height):
        for c in range(cfg.grid_width):
            cell_id = state.loc_mat[r][c]
            colour_square(cell_id, cell_id, state)
 
    # Game loop — continues until only 1 country remains
    while len(state.countries) > 1:
        state.move += 1
 
        attacker_id, ax, ay = pick_attacker(state)
        resolve_combat(attacker_id, ax, ay, state)
        update_leaderboard(state)
 
        if check_for_winner(state) == 1:
            print(f'Game Over. {attacker_id} won in move {state.move}')
            break
 
 
main()
 