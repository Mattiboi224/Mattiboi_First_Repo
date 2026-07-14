import PIL.Image as Image

# ------------------ CONFIG ------------------
# Screen Width and Height
WIDTH, HEIGHT = 1024, 704
MENU_WIDTH = 192

UNIT_MENU_WIDTH = 128
UNIT_MENU_HEIGHT = 128
BOTTOM_MENU_HEIGHT = 32
TILE = 32

SCREEN_WIDTH = WIDTH - MENU_WIDTH - UNIT_MENU_WIDTH
SCREEN_HEIGHT = HEIGHT - BOTTOM_MENU_HEIGHT

# Screen Grid Width and Height
# GRID HEIGHT = 22
# GRID WIDTH = 22
GRID_W, GRID_H = (WIDTH - MENU_WIDTH - UNIT_MENU_WIDTH) // TILE, (HEIGHT - BOTTOM_MENU_HEIGHT) // TILE
MENU_TILE = MENU_WIDTH // TILE

# Camera Settings
CAMERA_SPEED = 5
CAMERA_X, CAMERA_Y = 0, 0
FPS = 60

# Menu Settings
MENU_BG = (50, 50, 50)
BTN_COLOR = (80, 80, 80)
BTN_HOVER = (120, 120, 120)
TEXT_COLOR = (230, 230, 230)

# Left Menu Settings
UNIT_MENU_BG = (245, 236, 106)
BTN_HEIGHT = 60
PADDING = 20

UNIT_PROP_HEIGHT = 20

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
COST_STORAGE_UNIT = 50
COST_FUEL_TANK = 50
COST_GOLD_VAULT = 50

# Image Locations
BASE_FOLDER = "assets"

def entity_image_path(kind, category):
    return f"{BASE_FOLDER}/{category}/{kind}.png"

ENTITY_STATS = {
    # Unit Stats
    "Soldier": {
        "Name": "Soldier",
        "kind": "soldier",
        "category": "unit",
        "building_unit": "barracks",
        "cost": COST_SOLDIER,
        "hp": 80,
        "atk": 20,
        "range": 2 * TILE,
        "speed": 90,   # px/s
        "ammo": 10,
        "armour": 2,
        "shots": 1,
        "build_time": 5.0,
        "colour_to_be_converted": (52, 68, 32),
    },
    "Tank": {
        "Name": "Tank",
        "kind": "tank",
        "category": "unit",
        "building_unit": "tank_factory",
        "cost": COST_TANK,
        "hp": 150,
        "atk": 30,
        "range": 3 * TILE,
        "speed": 50,   # px/s
        "ammo": 5,
        "armour": 5,
        "shots": 2,
        "build_time": 10.0,
        "colour_to_be_converted": (74, 98, 48),
    },
    "Ammo Truck": {
        "Name": "Ammo Truck",
        "kind": "ammo_truck",
        "category": "unit",
        "building_unit": "tank_factory",
        "cost": COST_AMMO_TRUCK,
        "hp": 100,
        "atk": 10,
        "range": 2 * TILE,
        "speed": 30,   # px/s
        "ammo": 5,
        "armour": 0,
        "shots": 1,
        "cargo": 50,
        "build_time": 7.0,
        "colour_to_be_converted": (74, 104, 40),
    },
    
    # Building stats
    "Construction": {
        "Name": "Construction",
        "kind": "construction",
        "category": "building",
        "colour_to_be_converted": (239, 228, 176),
    },
    "Base": {
        "Name": "Base",
        "kind": "base",
        "category": "building",
        "cost": COST_BASE,
        "hp": 500,
        "armour": 5,
        "build_time": 10.0,
        "colour_to_be_converted": (98, 80, 52),
        "storage_amount": 500,
        "resource_storage_type": "Minerals"
    },
    "Barracks": {
        "Name": "Barracks",
        "kind": "barracks",
        "category": "building",
        "cost": COST_BARRACKS,
        "hp": 250,
        "armour": 3,
        "build_time": 5.0,
        "colour_to_be_converted": (104, 114, 78),
    },
    "Tank Factory": {
        "Name": "Tank Factory",
        "kind": "tank_factory",
        "category": "building",
        "cost": COST_TANK_FACTORY,
        "hp": 300,
        "armour": 4,
        "build_time": 6.0,
        "colour_to_be_converted": (74, 84, 58),
    },
    "Storage Unit": {
        "Name": "Storage Unit",
        "kind": "storage_unit",
        "category": "building",
        "cost": COST_STORAGE_UNIT,
        "hp": 100,
        "armour": 2,
        "build_time": 2.0,
        "colour_to_be_converted": (40, 38, 32),
        "storage_amount": 50,
        "resource_storage_type": "Minerals"
    },
    "Fuel Tank": {
        "Name": "Fuel Tank",
        "kind": "fuel_tank",
        "category": "building",
        "cost": COST_FUEL_TANK,
        "hp": 100,
        "armour": 2,
        "build_time": 2.0,
        "colour_to_be_converted": (30, 30, 28),
        "storage_amount": 50,
        "resource_storage_type": "Fuel"
    },
    "Gold Vault": {
        "Name": "Gold Vault",
        "kind": "gold_vault",
        "category": "building",
        "cost": COST_GOLD_VAULT,
        "hp": 100,
        "armour": 2,
        "build_time": 2.0,
        "colour_to_be_converted": (35, 33, 30),
        "storage_amount": 50,
        "resource_storage_type": "Gold"
    },
}

for name, stats in ENTITY_STATS.items():
    stats["image"] = entity_image_path(stats["kind"], stats["category"])

# Resource Supply Time
MINERAL_SUPPLY_TIME = 3.0
FUEL_SUPPLY_TIME = 3.0
GOLD_SUPPLY_TIME = 3.0

# Tile types
T_GRASS = 0
T_WALL = 1
T_RESOURCE = 2
T_PLAYER_LOC = 3
T_FUEL = 4
T_GOLD = 5
T_BLANK = 6
T_WATER = 7

# Game Map Location
GAME_MAP = 'game_map.png'

# Resource Map
RESOURCE_MAP = 'resource_map.png'

# Adding Image
image = Image.open(GAME_MAP)
MAP_WIDTH, MAP_HEIGHT = image.size


TILE_COLORS = {
    #T_GRASS: (40, 110, 40),
    T_GRASS: (34, 177, 76),
    #T_WALL: (70, 70, 70),
    T_WALL: (195, 195, 195),
    #T_RESOURCE: (120, 85, 30),
    T_RESOURCE: (0, 0, 0),
    T_PLAYER_LOC: (237, 28, 36),
    T_FUEL: (181, 230, 29),
    T_GOLD: (255, 242, 0),
    T_BLANK: (255, 255, 255),
    T_WATER: (63, 72, 204)
}

TEAM_COLORS = {
    0: (80, 160, 255),   # blue
    1: (255, 80, 80),    # red
    2: (255, 200, 80),   # yellow
    3: (160, 255, 120),  # green
    4: (200, 120, 255),  # purple
    5: (255, 120, 200),  # pink
    6: (0, 0, 0)        # black
}
