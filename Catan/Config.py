import turtle


# Required Globals
global selected_team
global selecting_on_screen
global selecting_type
global road_check
global settlement_check
global city_check
global development_card_check
global built
global card_check
global trade_check

global knight_check
global monopoly_check
global road_building_check
global year_of_plenty_check

# Number of Players
NO_OF_PLAYER = 3

# Winning Points
NO_OF_VICTORY_WINNING_POINTS = 10

# Team Colours
TEAM_1_COLOUR = 'Red'
TEAM_2_COLOUR = 'Blue'
TEAM_3_COLOUR = 'Green'

# Pieces
TOTAL_ROAD_PIECES = 15
TOTAL_SETTLEMENT_PIECES = 5
TOTAL_CITY_PIECES = 4

# Resource Card
TOTAL_BRICK_CARD = 19
TOTAL_WOOD_CARD = 19
TOTAL_WHEAT_CARD = 19
TOTAL_STONE_CARD = 19
TOTAL_SHEEP_CARD = 19

# Development Card
TOTAL_KNIGHT_CARD = 14
TOTAL_VP_CARD = 5
TOTAL_MONOPOLY_CARD = 2
TOTAL_ROAD_BUILDING_CARD = 2
TOTAL_YEAR_OF_PLENTY_CARD = 2

# Build Development Deck
global DEVELOPMENT_CARD_DECK

DEVELOPMENT_CARD_DECK = ['Knight'] * TOTAL_KNIGHT_CARD + \
    ['VP'] * TOTAL_VP_CARD + ['Monopoly'] * TOTAL_MONOPOLY_CARD + \
        ['Road Building'] * TOTAL_ROAD_BUILDING_CARD + ['Year of Plenty'] * TOTAL_YEAR_OF_PLENTY_CARD

# Numbers
NUMBER = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12]

# Tile Counts
TOTAL_SAND = 1
TOTAL_WOOD = 4
TOTAL_BRICK = 3
TOTAL_WHEAT = 4
TOTAL_STONE = 3
TOTAL_SHEEP = 4

# Build Requirements
# ROAD
BUILD_ROAD_REQ_WOOD = 1
BUILD_ROAD_REQ_BRICK = 1

# SETTLEMENT
BUILD_SETTLEMENT_REQ_WOOD = 1
BUILD_SETTLEMENT_REQ_BRICK = 1
BUILD_SETTLEMENT_REQ_SHEEP = 1
BUILD_SETTLEMENT_REQ_WHEAT = 1

# CITY
BUILD_CITY_REQ_WHEAT = 2
BUILD_CITY_REQ_STONE = 3

# DEVELOPMENT CARD
BUILD_DEVELOPMENT_CARD_REQ_WHEAT = 1
BUILD_DEVELOPMENT_CARD_REQ_SHEEP = 1
BUILD_DEVELOPMENT_CARD_REQ_STONE = 1

# Sea ports
TOTAL_SEAPORTS = 9

# Seaport List
SEAPORT_LIST = ['Any','Any','Any','Any','Wood', 'Brick', 'Wheat', 'Stone', 'Sheep']

# Hexagon shape
side_length = 40
num_sides = 6
angle = 360.0 / num_sides

# Initialize the screen and main turtle
wn = turtle.Screen()
wn.setup(1200,900)
main_turtle = turtle.Turtle()
main_turtle.hideturtle()
board_turtle = turtle.Turtle()
board_turtle.hideturtle()
selection_turtle = turtle.Turtle()
selection_turtle.hideturtle()
number_turtle = turtle.Turtle()
number_turtle.hideturtle()
announcer_turtle = turtle.Turtle()
announcer_turtle.hideturtle()
dice_turtle = turtle.Turtle()
dice_turtle.hideturtle()
text_announcer_turtle = turtle.Turtle()
text_announcer_turtle.hideturtle()

# Putting Everything Up
main_turtle.up()
board_turtle.up()
number_turtle.up()
selection_turtle.up()
announcer_turtle.up()
text_announcer_turtle.up()