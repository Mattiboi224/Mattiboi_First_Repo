from player import Player
import Config as C
import random

# Map is a matrix
# Then each row is the row in which you can go
# Total Length is about 50

player_list = []

total_teams = 1 + C.NO_OF_AI_PLAYERS

# Create the Teams
for i in range(total_teams):
    if i == C.PLAYER_TEAM:
        player_list.append(Player(i, True))
    else:
        player_list.append(Player(i, False))

# Create the map
grid_map = []

for i in range(C.MAP_LENGTH):
    j = random.randint(0,1)

    if i <= C.STARTING_LENGTH:
        j = 2
    blank_list = ["" for _ in range(j + 2)]
    grid_map.append(blank_list)


# Determine starting positions
for i in range(len(player_list * 2)):

    # First Round Randomly pick the ride
    if i <= len(player_list):
        choose_the_rider = random.choice([0,1])

    if i >= len(player_list):
        i -= len(player_list)
        if not player_list[i].climber_loc:
            choose_the_rider = player_list[i].CLIMBER

        else:
            choose_the_rider = player_list[i].SPRINTER

    building = True
    while building:
        starting_row = random.randint(0,C.STARTING_LENGTH)
        start_position_on_row = random.randint(0, len(grid_map[starting_row]) - 1)

        if not grid_map[starting_row][start_position_on_row]:
            grid_map[starting_row][start_position_on_row] = player_list[i].colour
            building = False

    if choose_the_rider == player_list[i].CLIMBER:
        player_list[i].climber_loc = [starting_row, start_position_on_row]
    else:
        player_list[i].sprinter_loc = [starting_row, start_position_on_row]

running = True
#while running:
for i in range(10):
    
    rider_locs = []
    for i in player_list:

        rider_locs.append([i.climber_locs, 'Climber', i.team])
        rider_locs.append([i.sprinter_loc, 'Sprinter', i.team])

        

