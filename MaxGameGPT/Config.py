import PIL.Image as Image

# ------------------ CONFIG ------------------
# Screen Width and Height
WIDTH, HEIGHT = 1024, 704
MENU_WIDTH = 192

OPTIONS_MENU_HEIGHT = 30
UNIT_MENU_WIDTH = 128
UNIT_MENU_HEIGHT = 128
BOTTOM_MENU_HEIGHT = 32
TILE = 32

# Use Manual or Generated Map
AUTO_GENERATE_MAP = True

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
PADDING = 15

UNIT_PROP_HEIGHT = 20

PLAYER_TEAM = 0
NUM_AI = 2             # number of AI opponents
AI_TEAMS = list(range(1, 1 + NUM_AI))
NO_OF_SPAWNS = NUM_AI + 1  # number of spawn points (including player)

INITIAL_MONEY = 200
INITIAL_FUEL = 0
INITIAL_GOLD = 0
SELL_PERCENTAGE = 0.5

# Tile types
T_GRASS = 0
T_WALL = 1
T_RESOURCE = 2
T_PLAYER_LOC = 3
T_FUEL = 4
T_GOLD = 5
T_BLANK = 6
T_WATER = 7
T_BRIDGE = 8
T_WATER_PLATFORM = 9

# Movement rules
MOVE_GROUND = "ground"
MOVE_AMPHIBIOUS = "amphibious"
MOVE_WATER = "water"

PASSABLE_RULES = {
    MOVE_GROUND:      lambda t: t == T_BRIDGE or t == T_WATER_PLATFORM or (t != T_WALL and t != T_WATER),
    MOVE_AMPHIBIOUS:  lambda t: t != T_WALL,  # water is fine, walls aren't
    MOVE_WATER:      lambda t: t == T_WATER or t == T_BRIDGE,
}

# Costs
COST_WORKER = 50
COST_SOLDIER = 60
COST_BARRACKS = 75
COST_TANK = 150
COST_GUNBOAT = 150
COST_TANK_FACTORY = 100
COST_SHIPYARD = 100
COST_BASE = 100
COST_AMMO_TRUCK = 50
COST_FUEL_TRUCK = 50
COST_GOLD_TRUCK = 50
COST_STORAGE_UNIT = 50
COST_FUEL_TANK = 50
COST_GOLD_VAULT = 50
COST_CONSTRUCTOR = 10
COST_POWER_PLANT = 10
COST_MISSILE_CRAWLER = 150
COST_GUN_TURRET = 50
COST_POWER_STATION = 50
COST_SURVEYOR = 10
COST_ROAD = 5
COST_BRIDGE = 5
COST_WATER_PLATFORM = 5
COST_CONCRETE_BLOCK = 5
COST_REPAIR_UNIT = 25
COST_BULLDOZER = 25
COST_LAND_MINE = 10

# Image Locations
BASE_FOLDER = "assets"

def entity_image_path(kind, category):
    return f"{BASE_FOLDER}/{category}/{kind}.png"

#https://www.maxr.org/docs.php?id=17

# Current Entities
#'Soldier', 'Tank', 'Ammo Truck', 'Construction', 'Base', 'Barracks', 'Tank Factory', 'Storage Unit', 'Fuel Tank', 'Gold Vault'

# Missing Entities 
# Infanty Units # 23
# Infiltrator

# Ground Supply Units # 24
# Armoured Personnel Carrier, Mine Layer, Engineer, Scanner

# Ground Warfare Units # 25
# Rocket Launcher, Missile Crawler, Mobile Anti Aircraft, Scout

# Sea Warfare Units # 26
# Corvette, Escort, Gunboat, Missile Cruiser, Submarine

# Air Warfare Units # 27
# Ground Attack Plane, Fighter

# Sea Supply Units # 28
# Cargo Ship, Sea Mine Layer, Sea Transport

# Air Supply Units # 29
# Air Transport, AWAC

# Connecting Structures # 32
# Water Platform, Connector

# Mines # 33
# Sea Mine

# Defensive Buildings # 34
# Radar, Anti Aircraft, Artillery, Missile Launcher

# Factory Buildings # 35
# Light Vehicle Plant, Air Units Plant, Shipyard

# Supply Buildings # 36
# Completed

# Depots # 37
# Landing Pad, Barracks, Depot, Hanger, Dock

# Research and Colonisation Buildings # 38
# Habitat, Research Centre, Gold Refinery

ENTITY_STATS = {
    # Unit Stats
    "Soldier": {
        "Name": "Soldier",
        "kind": "soldier",
        "radius": TILE // 2,
        "category": "unit",
        "builds_from": "barracks",
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
        "attacking_unit": True,
        "movement_type": MOVE_GROUND,
        "rubble_value": 4,
    },
    "Tank": {
        "Name": "Tank",
        "kind": "tank",
        "radius": TILE // 2,
        "category": "unit",
        "builds_from": "tank_factory",
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
        "attacking_unit": True,
        "movement_type": MOVE_GROUND,
        "rubble_value": 10,
    },
    "Missile Crawler": {
        "Name": "Missile Crawler",
        "kind": "missile_crawler",
        "radius": TILE // 2,
        "category": "unit",
        "builds_from": "tank_factory",
        "cost": COST_MISSILE_CRAWLER,
        "hp": 50,
        "atk": 60,
        "range": 7 * TILE,
        "speed": 30,   # px/s
        "ammo": 5,
        "armour": 2,
        "shots": 1,
        "build_time": 10.0,
        "colour_to_be_converted": (200, 170, 40),
        "attacking_unit": True,
        "movement_type": MOVE_GROUND,
        "rubble_value": 10,
    },
    "Ammo Truck": {
        "Name": "Ammo Truck",
        "kind": "ammo_truck",
        "radius": TILE // 2,
        "category": "unit",
        "builds_from": "tank_factory",
        "cost": COST_AMMO_TRUCK,
        "hp": 100,
        "range": 2 * TILE,
        "speed": 40,   # px/s
        "armour": 0,
        "cargo": 50,
        "build_time": 6.0,
        "colour_to_be_converted": (74, 104, 40),
        "transfer_unit": True,
        "movement_type": MOVE_GROUND,
        "rubble_value": 15,
    },
    "Fuel Truck": {
        "Name": "Fuel Truck",
        "kind": "fuel_truck",
        "radius": TILE // 2,
        "category": "unit",
        "builds_from": "tank_factory",
        "cost": COST_FUEL_TRUCK,
        "hp": 100,
        "range": 2 * TILE,
        "speed": 40,   # px/s
        "armour": 0,
        "cargo": 50,
        "build_time": 6.0,
        "colour_to_be_converted": (168, 170, 165),
        "transfer_unit": True,
        "movement_type": MOVE_GROUND,
        "rubble_value": 6,
    },
    "Gold Truck": {
        "Name": "Gold Truck",
        "kind": "gold_truck",
        "radius": TILE // 2,
        "category": "unit",
        "builds_from": "tank_factory",
        "cost": COST_GOLD_TRUCK,
        "hp": 100,
        "range": 2 * TILE,
        "speed": 40,   # px/s
        "armour": 0,
        "cargo": 50,
        "build_time": 6.0,
        "colour_to_be_converted": (80, 77, 70),
        "transfer_unit": True,
        "movement_type": MOVE_GROUND,
        "rubble_value": 6,
    },
    "Repair Unit": {
        "Name": "Repair Unit",
        "kind": "repair_unit",
        "radius": TILE // 2,
        "category": "unit",
        "builds_from": "tank_factory",
        "cost": COST_REPAIR_UNIT,
        "hp": 100,
        "range": 2 * TILE,
        "speed": 30,   # px/s
        "armour": 0,
        "cargo": 50,
        "build_time": 7.0,
        "colour_to_be_converted": (200, 120, 40),
        "transfer_unit": True,
        "movement_type": MOVE_GROUND,
        "repair_unit": True,
        "rubble_value": 10,
    },
    "Bulldozer": {
        "Name": "Bulldozer",
        "kind": "bulldozer",
        "radius": TILE // 2,
        "category": "unit",
        "builds_from": "tank_factory",
        "cost": COST_BULLDOZER,
        "hp": 100,
        "range": 2 * TILE,
        "speed": 30,   # px/s
        "armour": 0,
        "cargo": 50,
        "build_time": 7.0,
        "colour_to_be_converted": (210, 165, 40),
        "transfer_unit": True,
        "movement_type": MOVE_GROUND,
        "rubble_value": 10,
        "clearing": False,
        "clear_rate": 5
    },
    "Constructor": {
        "Name": "Constructor",
        "kind": "constructor",
        "radius": TILE // 2,
        "category": "unit",
        "builds_from": "tank_factory",
        "cost": COST_CONSTRUCTOR,
        "hp": 100,
        "speed": 30,   # px/s
        "armour": 0,
        "cargo": 50,
        "build_time": 7.0,
        "colour_to_be_converted": (200, 170, 40),
        "building_unit": True,
        "transfer_unit": True,
        "movement_type": MOVE_AMPHIBIOUS,
        "rubble_value": 10,
    },
    "Surveyor": {
        "Name": "Surveyor",
        "kind": "surveyor",
        "radius": TILE // 2,
        "category": "unit",
        "builds_from": "tank_factory",
        "cost": COST_SURVEYOR,
        "hp": 10,
        "speed": 60,   # px/s
        "armour": 0,
        "build_time": 1.0,
        "colour_to_be_converted": (200, 170, 40),
        "movement_type": MOVE_AMPHIBIOUS,
        "rubble_value": 6,
    },
    "Gunboat": {
        "Name": "Gunboat",
        "kind": "gunboat",
        "radius": TILE // 2,
        "category": "unit",
        "builds_from": "shipyard",
        "cost": COST_GUNBOAT,
        "hp": 150,
        "atk": 30,
        "range": 3 * TILE,
        "speed": 50,   # px/s
        "ammo": 5,
        "armour": 5,
        "shots": 2,
        "build_time": 10.0,
        "colour_to_be_converted": (74, 98, 48),
        "attacking_unit": True,
        "movement_type": MOVE_WATER,
        "rubble_value": 10,
    },

    # Building stats
    "Construction": {
        "Name": "Construction",
        "kind": "construction",
        "category": "building",
        "colour_to_be_converted": (239, 228, 176),
    },
    "Big Construction": {
        "Name": "Big Construction",
        "kind": "big_construction",
        "category": "building",
        "colour_to_be_converted": (168, 138, 82),
    },
    "Base": {
        "Name": "Base",
        "kind": "base",
        "radius": TILE,
        "category": "building",
        "cost": COST_BASE,
        "hp": 500,
        "armour": 5,
        "build_time": 10.0,
        "colour_to_be_converted": (96, 68, 42),
        "storage_amount": 500,
        "resource_storage_type": "Minerals",
        "power_given": 1,
        "rubble_value": 20,
        "valid_terrain": {T_GRASS, T_WATER_PLATFORM},
        #"power_required": True, # Will add back in when we can transfer power completely to plant
    },
    "Barracks": {
        "Name": "Barracks",
        "kind": "barracks",
        "radius": TILE // 2,
        "category": "building",
        "cost": COST_BARRACKS,
        "hp": 250,
        "armour": 3,
        "build_time": 5.0,
        "colour_to_be_converted": (104, 114, 78),
        "power_used": 1,
        "power_required": True,
        "rubble_value": 5,
        "valid_terrain": {T_GRASS, T_WATER_PLATFORM},
    },
    "Tank Factory": {
        "Name": "Tank Factory",
        "kind": "tank_factory",
        "radius": TILE // 2,
        "category": "building",
        "cost": COST_TANK_FACTORY,
        "hp": 300,
        "armour": 4,
        "build_time": 6.0,
        "colour_to_be_converted": (74, 84, 58),
        "power_used": 2,
        "power_required": True,
        "rubble_value": 20,
        "valid_terrain": {T_GRASS, T_WATER_PLATFORM},
    },
    "Shipyard": {
        "Name": "Shipyard",
        "kind": "shipyard",
        "radius": TILE,
        "category": "building",
        "cost": COST_SHIPYARD,
        "hp": 300,
        "armour": 4,
        "build_time": 6.0,
        "colour_to_be_converted": (70, 72, 74),
        "power_used": 2,
        "power_required": True,
        "rubble_value": 20,
        "valid_terrain": {T_WATER},
    },
    "Storage Unit": {
        "Name": "Storage Unit",
        "kind": "storage_unit",
        "radius": TILE // 2,
        "category": "building",
        "cost": COST_STORAGE_UNIT,
        "hp": 100,
        "armour": 2,
        "build_time": 2.0,
        "colour_to_be_converted": (40, 38, 32),
        "storage_amount": 50,
        "resource_storage_type": "Minerals",
        "rubble_value": 15,
        "valid_terrain": {T_GRASS, T_WATER_PLATFORM},
        
    },
    "Fuel Tank": {
        "Name": "Fuel Tank",
        "kind": "fuel_tank",
        "radius": TILE // 2,
        "category": "building",
        "cost": COST_FUEL_TANK,
        "hp": 100,
        "armour": 2,
        "build_time": 2.0,
        "colour_to_be_converted": (30, 30, 28),
        "storage_amount": 50,
        "resource_storage_type": "Fuel",
        "rubble_value": 15,
        "valid_terrain": {T_GRASS, T_WATER_PLATFORM},
    },
    "Gold Vault": {
        "Name": "Gold Vault",
        "kind": "gold_vault",
        "radius": TILE // 2,
        "category": "building",
        "cost": COST_GOLD_VAULT,
        "hp": 100,
        "armour": 2,
        "build_time": 2.0,
        "colour_to_be_converted": (35, 33, 30),
        "storage_amount": 50,
        "resource_storage_type": "Gold",
        "rubble_value": 15,
        "valid_terrain": {T_GRASS, T_WATER_PLATFORM},
    },
    "Power Plant": {
        "Name": "Power Plant",
        "kind": "power_plant",
        "radius": TILE // 2,
        "category": "building",
        "cost": COST_POWER_PLANT,
        "hp": 100,
        "armour": 2,
        "build_time": 3.0,
        "colour_to_be_converted": (200, 170, 40),
        "power_given": 10,
        "power_supply": True,
        "depletion_time": 3.0,
        "resource_used": 1,
        "rubble_value": 7,
        "valid_terrain": {T_GRASS, T_WATER_PLATFORM},
    },
    "Gun Turret": {
        "Name": "Gun Turret",
        "kind": "gun_turret",
        "radius": TILE // 2,
        "category": "building",
        "cost": COST_GUN_TURRET,
        "hp": 100,
        "armour": 5,
        "build_time": 3.0,
        "colour_to_be_converted": (200, 170, 40),
        "attacking_building": True,
        "atk": 20,
        "range": 2 * TILE,
        "ammo": 10,
        "shots": 1,
        "rubble_value": 7,
        "valid_terrain": {T_GRASS, T_WATER_PLATFORM},
    },
    "Power Station": {
        "Name": "Power Station",
        "kind": "power_station",
        "radius": TILE,
        "category": "building",
        "cost": COST_POWER_STATION,
        "hp": 100,
        "armour": 2,
        "build_time": 3.0,
        "colour_to_be_converted": (200, 170, 40),
        "power_given": 20,
        "power_supply": True,
        "depletion_time": 3.0,
        "resource_used": 5,
        "rubble_value": 7,
        "valid_terrain": {T_GRASS, T_WATER_PLATFORM},
    },
    "Road": {
        "Name": "Road",
        "kind": "road",
        "radius": TILE // 2,
        "category": "building",
        "cost": COST_ROAD,
        "hp": 10,
        "armour": 0,
        "build_time": 0.1,
        "colour_to_be_converted": (200, 170, 40),
        "rubble_value": 2,
        "valid_terrain": {T_GRASS},
    },
    "Concrete Block": {
        "Name": "Concrete Block",
        "kind": "concrete_block",
        "radius": TILE // 2,
        "category": "building",
        "cost": COST_CONCRETE_BLOCK,
        "hp": 100,
        "armour": 0,
        "build_time": 0.1,
        "colour_to_be_converted": (150, 148, 142),
        "rubble_value": 2,
        "valid_terrain": {T_GRASS},
    },
    "Bridge": {
        "Name": "Bridge",
        "kind": "bridge",
        "radius": TILE // 2,
        "category": "building",
        "cost": COST_BRIDGE,
        "hp": 100,
        "armour": 0,
        "build_time": 0.1,
        "colour_to_be_converted": (127, 127, 127),
        "rubble_value": 2,
        "valid_terrain": {T_WATER},
    },
    "Water Platform": {
        "Name": "Water Platform",
        "kind": "water_platform",
        "radius": TILE // 2,
        "category": "building",
        "cost": COST_WATER_PLATFORM,
        "hp": 100,
        "armour": 0,
        "build_time": 0.1,
        "colour_to_be_converted": (200, 170, 40),
        "rubble_value": 2,
        "valid_terrain": {T_WATER},
    },
    "Land Mine": {
        "Name": "Land Mine",
        "kind": "land_mine",
        "radius": TILE // 2,
        "category": "building",
        "cost": COST_LAND_MINE,
        "hp": 100,
        "armour": 0,
        "build_time": 0.1,
        "colour_to_be_converted": (255, 242, 0),
        "rubble_value": 2,
        "damage": 100,
        "explosive": True,
        "hidden": True,
        "blast_radius": 2.0 * TILE,
        "trigger_radius": 1.0 * TILE,
        "valid_terrain": {T_GRASS},
    },
    # Building stats
    "Rubble": {
        "Name": "Rubble",
        "kind": "rubble",
        "category": "common",
        "colour_to_be_converted": (239, 228, 176),
    },
    # Building stats
    "Big Rubble": {
        "Name": "Big Rubble",
        "kind": "big_rubble",
        "category": "common",
        "colour_to_be_converted": (239, 228, 176),
    },
}

for name, stats in ENTITY_STATS.items():
    stats["image"] = entity_image_path(stats["kind"], stats["category"])

# Resource Supply Time
MINERAL_SUPPLY_TIME = 3.0
FUEL_SUPPLY_TIME = 3.0
GOLD_SUPPLY_TIME = 3.0

# Resource Map
RESOURCE_MAP = 'resource_map.png'

# Game Map Location
MANUAL_MAP = 'game_map.png'

# Generated Map
GENERATED_MAP = 'hybrid_map.png'
SIZE = 32
CELL = 1
NOISE_SCALE = 22.0      # bigger = smoother/larger landmasses
NOISE_OCTAVES = 3
NOISE_PERSISTENCE = 0.55
NOISE_LACUNARITY = 2.0
WATER_THRESHOLD = -0.02 # lower = less water
EDGE_MARGIN = 1     # min tiles from map border a spawn can be placed

SMOOTH_PASSES = 2        # cellular automata cleanup passes

MIN_SPAWN_DIST = 15

if AUTO_GENERATE_MAP:
    MAP_PATH = GENERATED_MAP
else:
    MAP_PATH = MANUAL_MAP

# Adding Image
image = Image.open(MAP_PATH)
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


MINI_MAP_COLOURS = {
    0: (100, 200, 255),   # blue
    1: (255, 80, 80),    # red
    2: (255, 200, 80),   # yellow
    3: (160, 255, 120),  # green
    4: (200, 120, 255),  # purple
    5: (255, 120, 200),  # pink
    6: (0, 0, 0)        # black
}