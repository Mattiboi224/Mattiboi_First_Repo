# ------------------ CONFIG ------------------
WIDTH, HEIGHT = 1024, 704
TILE = 32
GRID_W, GRID_H = WIDTH // TILE, HEIGHT // TILE

FPS = 60

PLAYER_TEAM = 0
NUM_AI = 1             # number of AI opponents
AI_TEAMS = list(range(1, 1 + NUM_AI))

INITIAL_MONEY = 0

# Costs
COST_WORKER = 50
COST_SOLDIER = 60
COST_BARRACKS = 75
COST_TANK = 100
COST_TANK_FACTORY = 100

# Build times (in seconds)
BUILD_WORKER_TIME = 3.0
BUILD_SOLDIER_TIME = 5.0
BUILD_TANK_TIME = 10.0

# Unit stats
WORKER_HP = 45
WORKER_ATK = 4
WORKER_RANGE = 1.0 * TILE
WORKER_SPEED = 80  # px/s

SOLDIER_HP = 80
SOLDIER_ATK = 10
SOLDIER_RANGE = 1.2 * TILE
SOLDIER_SPEED = 90  # px/s

TANK_HP = 200
TANK_ATK = 50
TANK_RANGE = 3 * TILE
TANK_SPEED = 50  # px/s

# Building stats
BASE_HP = 500
BARRACKS_HP = 250
TANK_FACTORY_HP = 300

# Resource harvest
HARVEST_PER_TRIP = 25
HARVEST_TIME = 3.0
RESOURCE_HEALTH = 200

# Tile types
T_GRASS = 0
T_WALL = 1
T_RESOURCE = 2

# Image Location
#pg.image.load('assets/tank.png').convert_alpha()
BASE_IMAGE = 'assets/buildings/base.png'
BARRACKS_IMAGE = 'assets/buildings/barracks.png'
WORKER_IMAGE = 'assets/units/worker.png'
SOLDIER_IMAGE = 'assets/units/soldier.png'
TANK_FACTORY_IMAGE = 'assets/buildings/tank_factory.png'
TANK_IMAGE = 'assets/units/tank.png'


TILE_COLORS = {
    T_GRASS: (40, 110, 40),
    T_WALL: (70, 70, 70),
    T_RESOURCE: (120, 85, 30),
}

TEAM_COLORS = {
    0: (80, 160, 255),   # blue
    1: (255, 80, 80),    # red
    2: (255, 200, 80),   # yellow
    3: (160, 255, 120),  # green
    4: (200, 120, 255),  # purple
}