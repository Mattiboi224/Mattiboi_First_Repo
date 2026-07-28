import math

WIDTH, HEIGHT = 1024, 704

RIGHT_MARGIN = 30
SPEED = 5
TILE = 60

CLIMBER_DECK = [3, 4, 5, 6, 7] 
SPRINTER_DECK = [2, 3, 4, 5, 9]

PLAYER_TEAM = 0

NO_OF_AI_PLAYERS = 5

STRAIGHT_PIECE = 6
BENDS = 12

MAP_LENGTH = 7 * STRAIGHT_PIECE + 2 * BENDS 

STARTING_LENGTH = 5
FINISH_LINE = MAP_LENGTH - 5

TEAM_COLORS = {
    0: (80, 160, 255),   # blue
    1: (255, 80, 80),    # red
    2: (255, 200, 80),   # yellow
    3: (160, 255, 120),  # green
    4: (200, 120, 255),  # purple
    5: (255, 120, 200),  # pink
    6: (0, 0, 0)        # black
}

# Image Locations
BASE_FOLDER = "assets"

# Map Drawing Information
ORIGIN_X, ORIGIN_Y = 30, 30
# Define colors
main_colour = (255, 0, 0)
starting_colour = (0, 255, 0)
ending_colour = (0, 0, 255)
border_colour = (255, 255, 255)

tiles_per_row = math.floor((WIDTH - ORIGIN_X - TILE - RIGHT_MARGIN) / TILE)

RIDER_CONFIG = {
    "Climber": {
        "Name": "Climber",
        "image": f"{BASE_FOLDER}/climber.png",
        "colour_to_be_converted": (40, 40, 45),
    },
    "Sprinter": {
        "Name": "Sprinter",
        "image": f"{BASE_FOLDER}/sprinter.png",
        "colour_to_be_converted": (180, 40, 40),
    }
}