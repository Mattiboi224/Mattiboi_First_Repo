# ------------------ CONFIG ------------------
WIDTH, HEIGHT = 1024, 704
MENU_WIDTH = 192
UNIT_MENU_WIDTH = 128
UNIT_MENU_HEIGHT = 128
TILE = 32

# GRID HEIGHT = 22
# GRID WIDTH = 26
GRID_W, GRID_H = (WIDTH - MENU_WIDTH) // TILE, HEIGHT // TILE
MENU_TILE = MENU_WIDTH // TILE

# Menu Settings
MENU_BG = (50, 50, 50)
BTN_COLOR = (80, 80, 80)
BTN_HOVER = (120, 120, 120)
TEXT_COLOR = (230, 230, 230)

BTN_HEIGHT = 60
PADDING = 20

UNIT_PROP_HEIGHT = 20

FPS = 60

PLAYER_TEAM = 0
NUM_AI = 2             # number of AI opponents
AI_TEAMS = list(range(1, 1 + NUM_AI))

INITIAL_MONEY = 200
INITIAL_FUEL = 0
INITIAL_GOLD = 0
SELL_PERCENTAGE = 0.5

# Costs
COST_WORKER = 50
COST_SOLDIER = 60
COST_BARRACKS = 75
COST_TANK = 150
COST_TANK_FACTORY = 100
COST_BASE = 100
COST_AMMO_TRUCK = 100

# Build times (in seconds)
BUILD_WORKER_TIME = 3.0
BUILD_SOLDIER_TIME = 5.0
BUILD_TANK_TIME = 10.0
BUILD_AMMO_TRUCK_TIME = 7.0

# Unit stats
SOLDIER_HP = 80
SOLDIER_ATK = 20
SOLDIER_RANGE = 2 * TILE
SOLDIER_SPEED = 90  # px/s
SOLDIER_AMMO = 10
SOLDIER_ARMOUR = 2
SOLDIER_SHOTS = 1

TANK_HP = 150
TANK_ATK = 30
TANK_RANGE = 3 * TILE
TANK_SPEED = 50  # px/s
TANK_AMMO = 5
TANK_ARMOUR = 5
TANK_SHOTS = 2

AMMO_TRUCK_HP = 100
AMMO_TRUCK_ATK = 10
AMMO_TRUCK_RANGE = 2 * TILE
AMMO_TRUCK_SPEED = 30  # px/s
AMMO_TRUCK_AMMO = 5
AMMO_TRUCK_ARMOUR = 0
AMMO_TRUCK_SHOTS = 1
AMMO_TRUCK_CARGO = 50 


UNIT_STATS = {
    "Barracks": {"cost": COST_BARRACKS, "kind": "barracks"},
    "Soldier":  {"cost": COST_SOLDIER,  "kind": "soldier"},
    "Tank":     {"cost": COST_TANK,     "kind": "tank"},
    "Ammo Truck": {"cost": COST_AMMO_TRUCK, "kind": "ammo_truck"},
    "Base":     {"cost": COST_BASE,     "kind": "base"},
    "Tank Factory":     {"cost": COST_TANK_FACTORY,     "kind": "tank_factory"},
}

# Building stats
BASE_HP = 500
BASE_ARMOUR = 5

BARRACKS_HP = 250
BARRACKS_ARMOUR = 3

TANK_FACTORY_HP = 300
TANK_FACTORY_ARMOUR = 4

# Resource Supply Time
MINERAL_SUPPLY_TIME = 3.0

# Resource harvest
HARVEST_PER_TRIP = 25
GOLD_HARVEST_PER_TRIP = 1
ORE_HARVEST_TIME = 3.0
GEM_HARVEST_TIME = 2.0
ORE_RESOURCE_HEALTH = 200
GEM_RESOURCE_HEALTH = 400
GOLD_HARVEST_TIME = 10.0
GOLD_RESOURCE_HEALTH = 5

# Tile types
T_GRASS = 0
T_WALL = 1
T_RESOURCE = 2
T_PLAYER_LOC = 3
T_FUEL = 4
T_GOLD = 5
T_BLANK = 6

# Image Location
#pg.image.load('assets/tank.png').convert_alpha()
BASE_IMAGE = 'assets/buildings/base.png'
BARRACKS_IMAGE = 'assets/buildings/barracks.png'
WORKER_IMAGE = 'assets/units/worker.png'
SOLDIER_IMAGE = 'assets/units/soldier.png'
TANK_FACTORY_IMAGE = 'assets/buildings/tank_factory.png'
TANK_IMAGE = 'assets/units/tank.png'
GOLD_MINER_IMAGE = 'assets/units/gold_miner.png'
AMMO_TRUCK_IMAGE = 'assets/units/ammo_truck.png'

# Game Map Location
GAME_MAP = 'game_map.png'

# Resource Map
RESOURCE_MAP = 'resource_map.png'

TILE_COLORS = {
    #T_GRASS: (40, 110, 40),
    T_GRASS: (34, 177, 76),
    #T_WALL: (70, 70, 70),
    T_WALL: (127, 127, 127),
    #T_RESOURCE: (120, 85, 30),
    T_RESOURCE: (0, 0, 0),
    T_PLAYER_LOC: (237, 28, 36),
    T_FUEL: (181, 230, 29),
    T_GOLD: (255, 242, 0),
    T_BLANK: (255, 255, 255)
}

TEAM_COLORS = {
    0: (80, 160, 255),   # blue
    1: (255, 80, 80),    # red
    2: (255, 200, 80),   # yellow
    3: (160, 255, 120),  # green
    4: (200, 120, 255),  # purple
}

# Convert This Colour to Team Colour
# Tanks
TANK_OLD = (74, 98, 48)

# Ammo Truck
AMMO_TRUCK_OLD = (74, 104, 40)

# Soldier
SOLDIER_OLD = (52, 68, 32)