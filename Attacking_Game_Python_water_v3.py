import random
#import math
#import numpy as np
from collections import Counter
import turtle as Turtle
import time

# Define constant values used in the main program that sets up
# the drawing canvas.  Do not change any of these values unless
# instructed.
grid_width = 5
grid_height = 5
cell_size = 50 # pixels (default is 100)
x_margin = cell_size * 2.5 # pixels, the size of the margin left/right of the grid
y_margin = cell_size // 2 # pixels, the size of the margin below/above the grid
window_grid_height = grid_height * cell_size + y_margin * 2
window_grid_width = grid_width * cell_size + x_margin * 2
small_font = ('Arial', cell_size // 5, 'normal') # font for the coords
big_font = ('Arial', cell_size // 4, 'normal') # font for any other text
amount_of_mountain_tiles = 7 #impassable terrain
amount_of_water_tiles = 4 #can pass over it to attack another team

def main():
    # Setup the battlefield
    attack_range, number_of_countries, moves, \
            move, winning_countries_old, \
            winning_territories_old, all_squares_size = starting_conditions(amount_of_mountain_tiles, amount_of_water_tiles)
    countries_mat, Org_Countries_mat, Loc_Countries_mat, \
        Play_Countries_mat, Flat_Play_Mat, \
        Colour_Countries_mat = countries_setup(number_of_countries, \
                                                                    grid_width, amount_of_mountain_tiles, \
                                                                    all_squares_size, amount_of_water_tiles)

    setupmapscreen(label_spaces = False)

    for m in range(0,grid_height):
        for n in range(0,grid_width):
            colour_square(Loc_Countries_mat[m][n],Loc_Countries_mat[m][n],Loc_Countries_mat, Colour_Countries_mat, Play_Countries_mat)

    #while move < 15:
    while len(countries_mat) > 1:
        move += 1
        # Determine who's turn it is
        who_turn, x_location, \
            y_location = whos_turn_is_it(grid_width, grid_height, \
                                         Loc_Countries_mat, Play_Countries_mat)
        
        # See if it's valid and can attack someone
        different_countries = check_surrounds_for_differing_countries(Play_Countries_mat, \
                                                                     x_location, y_location, \
                                                                     grid_height, grid_width)
        
        #Check the location and position has at least 1 different country
        #around the position chosen
        #If it doesn't get another location until it does
        while different_countries != 'Can Attack':
            who_turn, x_location, \
                y_location = whos_turn_is_it(grid_width, grid_height, \
                                             Loc_Countries_mat, Play_Countries_mat)
            #print(Play_Countries_mat)
            #print(y_location)
            #print(x_location)
            different_countries = check_surrounds_for_differing_countries(Play_Countries_mat, \
                                                                         x_location, y_location, \
                                                                         grid_height, grid_width)
        
        Flat_Play_Mat, \
            Play_Countries_mat, \
            countries_mat = attacking_everyone(attack_range, \
                           Play_Countries_mat, x_location, y_location, \
                               grid_width, grid_height, Loc_Countries_mat, \
                               countries_mat, move, Flat_Play_Mat, Colour_Countries_mat)
    
        winning_countries, winning_territories = most_frequent(Flat_Play_Mat)
        
        winning_countries_old, \
            winning_territories_old = Lead_Change(winning_countries, \
                                                  winning_countries_old, \
                        winning_territories, winning_territories_old)
        
        #Check if Any "Capitals" remain
        capital_counter = check_for_winner(grid_width, grid_height, Play_Countries_mat, Loc_Countries_mat)
        
        #If Only 1 then game over
        if capital_counter == 1:
            print('Game Over. %d Won in move %d \n' % (who_turn, move))  
            break
        
        
    
    
#Starting Condition
def starting_conditions(amount_of_mountain_tiles, amount_of_water_tiles):
    attack_range = 1
    moves = 3
    number_of_countries = grid_width * grid_height - amount_of_mountain_tiles - amount_of_water_tiles
    all_squares_size = grid_width * grid_height
    move = 0 #Current Move
    winning_countries_old = [0]
    winning_territories = 0

    return attack_range, number_of_countries, moves, \
            move, winning_countries_old, winning_territories, \
            all_squares_size


#Set up the lists with all the countries
def countries_setup(number_of_countries, grid_width, amount_of_mountain_tiles, all_squares_size, amount_of_water_tiles):
    Org_Countries_mat = []
    countries_mat = []
    countries_grid_width = []
    countries_grid_width_2 = []
    countries_grid_width_3 = []
    Loc_Countries_mat = []
    Play_Countries_mat = []
    Colour_Countries_mat = []
    
    #### NUMBER OF COUNTRIES #Location #Owner
    for n in range(1,all_squares_size + 1):
        countries_mat.append(n)
        countries_grid_width.append(n)
        countries_grid_width_2.append(n)
        countries_grid_width_3.append((random.randrange(0,256),\
                                       random.randrange(0,256),\
                                       random.randrange(0,256)))
                #print(countries_mat)
        if n % grid_width == 0:
            # Location Matrix
            Loc_Countries_mat.append(countries_grid_width_2)
            countries_grid_width_2 = []
            
            # Playing Matrix Left
            Play_Countries_mat.append(countries_grid_width)
            countries_grid_width = []
            
            Colour_Countries_mat.append(countries_grid_width_3)
            countries_grid_width_3 = []
    
    
    # Tiles that are mountains
    if amount_of_mountain_tiles >= 1:
        mountains_tab = []
        for o in range(0,amount_of_mountain_tiles):
            while True:
                mountain_location = random.randrange(1, all_squares_size)
                if mountain_location in mountains_tab:
                    continue
                else:
                    break                
            mountains_tab.append(mountain_location)
            x_location, y_location = find_location(mountain_location, Loc_Countries_mat, grid_width, grid_height)
            # -1 = mountain
            Play_Countries_mat[y_location][x_location] = -1
            countries_mat[mountain_location - 1] = -1
            
            # Change the Square to Brown
            Colour_Countries_mat[y_location][x_location] = (150, 75, 0)
    #print(mountains_tab)
    #print(Play_Countries_mat)
    if amount_of_water_tiles >= 1:
        for w in range(1,amount_of_water_tiles + 1):
            while True:
                water_location = random.randrange(1, all_squares_size)
                if water_location in mountains_tab:
                    continue
                else:
                    break
            x_location, y_location = find_location(water_location, Loc_Countries_mat, grid_width, grid_height)
            Play_Countries_mat[y_location][x_location] = -2
            countries_mat[water_location - 1] = -2
            
            # Change the Square to Brown
            Colour_Countries_mat[y_location][x_location] = (0, 0, 255)           
    #print(Play_Countries_mat)
    
    # Flat Playing Matrix
    Flat_Play_Mat = countries_mat
    #print(Colour_Countries_mat)
    return countries_mat, Org_Countries_mat, Loc_Countries_mat, \
        Play_Countries_mat, Flat_Play_Mat, Colour_Countries_mat


#Who's Turn and What's There location
def whos_turn_is_it(grid_width, grid_height, Loc_Countries_mat, Play_Countries_mat):
    while True: 
        location = random.randrange(1, grid_width * grid_height)
        x_location, y_location = find_location(location, Loc_Countries_mat, \
                                           grid_width, grid_height)

        # Mountain and Water Can't Have a Turn
        if Play_Countries_mat[y_location][x_location] == -1:
            continue
        elif Play_Countries_mat[y_location][x_location] == -2:
            continue
        else:
            break
    #print(Play_Countries_mat)
    who_turn = Play_Countries_mat[y_location][x_location]
    return who_turn, x_location, y_location


#Find out the location of the random number
def find_location (location, Loc_Countries_mat, grid_width, grid_height):
    for i in range(0,grid_height):
      
      if location in Loc_Countries_mat[i]:
            x_location = Loc_Countries_mat[i].index(location)
            y_location = i
    return x_location, y_location


# Check if the location has a country it can attack
def check_surrounds_for_differing_countries(Play_Countries_mat, x_location, y_location, grid_height, grid_width):
    attackable_locations_mat = [[y_location, x_location]]
    # Check Grid because Bottom and Right Columns
    # Check if a country next to the location is attackable
    different_countries = 'Cannot Attack'
    loc_counter = 0
    for i in range(0, amount_of_water_tiles + 1):
        for att in range(loc_counter, len(attackable_locations_mat)):
            y_loc = attackable_locations_mat[att][0]
            x_loc = attackable_locations_mat[att][1]
            if x_loc != grid_width - 1 and y_loc != grid_height - 1:
                if (Play_Countries_mat[attackable_locations_mat[0][0]][attackable_locations_mat[0][1]] != Play_Countries_mat[y_loc + 1][x_loc] \
                and Play_Countries_mat[y_loc + 1][x_loc] != -1) \
                or (Play_Countries_mat[attackable_locations_mat[0][0]][attackable_locations_mat[0][1]] != Play_Countries_mat[y_loc - 1][x_loc] \
                and Play_Countries_mat[y_loc - 1][x_loc] != -1) \
                or (Play_Countries_mat[attackable_locations_mat[0][0]][attackable_locations_mat[0][1]] != Play_Countries_mat[y_loc][x_loc + 1] \
                and Play_Countries_mat[y_loc][x_loc + 1] != -1) \
                or (Play_Countries_mat[attackable_locations_mat[0][0]][attackable_locations_mat[0][1]] != Play_Countries_mat[y_loc][x_loc - 1] \
                and Play_Countries_mat[y_loc][x_loc - 1] != -1):
                    # If Next to Water
                    if Play_Countries_mat[y_loc + 1][x_loc] == -2:
                        attackable_locations_mat.append([y_loc + 1, x_loc])
                    elif Play_Countries_mat[y_loc - 1][x_loc] == -2:
                        attackable_locations_mat.append([y_loc - 1, x_loc])
                    elif Play_Countries_mat[y_loc][x_loc + 1] == -2:
                        attackable_locations_mat.append([y_loc, x_loc + 1])
                    elif Play_Countries_mat[y_loc][x_loc - 1] == -2:
                        attackable_locations_mat.append([y_loc, x_loc - 1])
                    else:
                        different_countries = 'Can Attack'
                        break
                else:
                    different_countries = 'Cannot Attack'
                loc_counter += 1
            elif x_loc == grid_width - 1:
                if (Play_Countries_mat[attackable_locations_mat[0][0]][attackable_locations_mat[0][1]] != Play_Countries_mat[y_loc + 1][x_loc] \
                and Play_Countries_mat[y_loc + 1][x_loc] != -1) \
                or (Play_Countries_mat[attackable_locations_mat[0][0]][attackable_locations_mat[0][1]] != Play_Countries_mat[y_loc - 1][x_loc] \
                and Play_Countries_mat[y_loc - 1][x_loc] != -1) \
                or (Play_Countries_mat[attackable_locations_mat[0][0]][attackable_locations_mat[0][1]] != Play_Countries_mat[y_loc][0] \
                and Play_Countries_mat[y_loc][0] != -1) \
                or (Play_Countries_mat[attackable_locations_mat[0][0]][attackable_locations_mat[0][1]] != Play_Countries_mat[y_loc][x_loc - 1] \
                and Play_Countries_mat[y_loc][x_loc - 1] != -1):    
                    # If Next to Water
                    if Play_Countries_mat[y_loc + 1][x_loc] == -2:
                        attackable_locations_mat.append([y_loc + 1, x_loc])
                    elif Play_Countries_mat[y_loc - 1][x_loc] == -2:
                        attackable_locations_mat.append([y_loc - 1, x_loc])
                    elif Play_Countries_mat[y_loc][0] == -2:
                        attackable_locations_mat.append([y_loc, 0])
                    elif Play_Countries_mat[y_loc][x_loc - 1] == -2:
                        attackable_locations_mat.append([y_loc, x_loc - 1])
                    else:
                        different_countries = 'Can Attack'
                        break
                else:
                    different_countries = 'Cannot Attack'
                loc_counter += 1
            elif y_loc == grid_height - 1:
                if (Play_Countries_mat[attackable_locations_mat[0][0]][attackable_locations_mat[0][1]] != Play_Countries_mat[0][x_loc] \
                and Play_Countries_mat[0][x_loc] != -1) \
                or (Play_Countries_mat[attackable_locations_mat[0][0]][attackable_locations_mat[0][1]] != Play_Countries_mat[y_loc - 1][x_loc] \
                and Play_Countries_mat[y_loc - 1][x_loc] != -1) \
                or (Play_Countries_mat[attackable_locations_mat[0][0]][attackable_locations_mat[0][1]] != Play_Countries_mat[y_loc][x_loc + 1] \
                and Play_Countries_mat[y_loc][x_loc + 1] != -1) \
                or (Play_Countries_mat[attackable_locations_mat[0][0]][attackable_locations_mat[0][1]] != Play_Countries_mat[y_loc][x_loc - 1] \
                and Play_Countries_mat[y_loc][x_loc - 1] != -1):
                    # If Next to Water
                    if Play_Countries_mat[0][x_loc] == -2:
                        attackable_locations_mat.append([0, x_loc])
                    elif Play_Countries_mat[y_loc - 1][x_loc] == -2:
                        attackable_locations_mat.append([y_loc - 1, x_loc])
                    elif Play_Countries_mat[y_loc][x_loc + 1] == -2:
                        attackable_locations_mat.append([y_loc, x_loc + 1])
                    elif Play_Countries_mat[y_loc][x_loc - 1] == -2:
                        attackable_locations_mat.append([y_loc, x_loc - 1])
                    else:                    
                        different_countries = 'Can Attack'
                        break
                else:
                    different_countries = 'Cannot Attack'
                loc_counter += 1
    #print(attackable_locations_mat)
    return different_countries


# Check if there's more than 1 "Capital"
def check_for_winner(grid_width, grid_height, Play_Countries_mat, Loc_Countries_mat):
    capital_counter = 0
    for i in range(grid_height):
        for j in range(grid_width):
            if Play_Countries_mat[i][j] == Loc_Countries_mat[i][j]:
                capital_counter += 1
    return capital_counter


# Attack and Change the Value of the team next to them
def attacking_everyone(attack_range, Play_Countries_mat, x_location, \
                       y_location, grid_width, grid_height, Loc_Countries_mat, \
                           countries_mat, move, Flat_Play_Mat, Colour_Countries_mat):
    attacker_mat = [[y_location, x_location]]
    
    #print(Loc_Countries_mat)
    #print(y_location)
    #print(x_location)
    # Ranged Attacks
    #how_far_to_attack = random.randint(1, attack_range)
    attacker = Play_Countries_mat[y_location][x_location]
    #att_counter = 0
    count = 0
    
    while count != 1:
        #print(attacker)
        #print(attacker_mat)
        #print(Loc_Countries_mat[y_location][x_location])
        for att in range(0, len(attacker_mat)):
            y_loc = attacker_mat[att][0]
            x_loc = attacker_mat[att][1]
            # if 1 up if 2 bottom 3 if left 4 if right
            direction = random.randint(1, 4)
            #print(direction)
            
            # Direction = 1 ... UP
            if direction == 1:
                # Can't attacker yourself or mountains
                if Play_Countries_mat[y_loc - 1][x_loc] == attacker or Play_Countries_mat[y_loc - 1][x_loc] == -1:
                    continue
                # If Water
                if Play_Countries_mat[y_loc - 1][x_loc] == -2:
                    if [y_loc - 1, x_loc] in attacker_mat:
                        continue
                    else:
                        attacker_mat.append([y_loc - 1, x_loc])
                        continue
                defender = Play_Countries_mat[y_loc - 1][x_loc]
                where_at = Loc_Countries_mat[y_loc - 1][x_loc]
                if Loc_Countries_mat[y_loc - 1][x_loc] == defender:
                    type_of_announcement = 'Defeated Base'
                        
                    # If Lose Capital Lose everything
                    Number_Of_Territories = 0
                    for i in range(grid_height):
                        for j in range(grid_width):
                            if Play_Countries_mat[i][j] == defender:
                                Play_Countries_mat[i][j] = attacker
                                Number_Of_Territories += 1     
                                colour_square(Loc_Countries_mat[i][j], attacker, Loc_Countries_mat, Colour_Countries_mat, Play_Countries_mat)
                                
                    for k in range(len(Flat_Play_Mat)):
                        if Flat_Play_Mat[k] == defender:
                            Flat_Play_Mat[k] = attacker
                          
                else:
                    type_of_announcement = 'Attacked not defeated'
                    Number_Of_Territories = 1
                    Play_Countries_mat[y_loc - 1][x_loc] = attacker
                    colour_square(Loc_Countries_mat[y_loc - 1][x_loc], attacker, Loc_Countries_mat, Colour_Countries_mat, Play_Countries_mat)
                if y_loc == 0:
                    Flat_Play_Mat[(grid_height - 1) + x_loc]
                else:
                    Flat_Play_Mat[(y_loc - 1) * grid_width + x_loc] = attacker 
                count = 1
                break
                
            # Direction = 2 ... DOWN
            elif direction == 2:
                # Not on the bottom
                if y_loc != grid_height - 1:
                    # Can't attacker yourself or mountains
                    if Play_Countries_mat[y_loc + 1][x_loc] == attacker or Play_Countries_mat[y_loc + 1][x_loc] == -1:
                        continue
                    # If Water
                    if Play_Countries_mat[y_loc + 1][x_loc] == -2:
                        if [y_loc + 1, x_loc] in attacker_mat:
                            continue
                        else:
                            attacker_mat.append([y_loc + 1, x_loc])
                            continue
                    defender = Play_Countries_mat[y_loc + 1][x_loc]
                    where_at = Loc_Countries_mat[y_loc + 1][x_loc]
                    if Loc_Countries_mat[y_loc + 1][x_loc] == defender:
                        type_of_announcement = 'Defeated Base'
                        
                        # If Lose Capital Lose everything
                        Number_Of_Territories = 0
                        for i in range(grid_height):
                            for j in range(grid_width):
                                if Play_Countries_mat[i][j] == defender:
                                    Play_Countries_mat[i][j] = attacker
                                    Number_Of_Territories += 1     
                                    colour_square(Loc_Countries_mat[i][j], attacker, Loc_Countries_mat, Colour_Countries_mat, Play_Countries_mat)
                                    
                        for k in range(len(Flat_Play_Mat)):
                            if Flat_Play_Mat[k] == defender:
                                Flat_Play_Mat[k] = attacker
                                  
                    else:
                        type_of_announcement = 'Attacked not defeated'
                        Number_Of_Territories = 1
                        Play_Countries_mat[y_loc + 1][x_loc] = attacker
                        colour_square(Loc_Countries_mat[y_loc + 1][x_loc], attacker, Loc_Countries_mat, Colour_Countries_mat, Play_Countries_mat)
                    Flat_Play_Mat[((y_loc + 1) * grid_width) + x_loc] = attacker 
                    count = 1     
                    break
                    
                else:
                    # Can't attacker yourself or mountains
                    if Play_Countries_mat[0][x_loc] == attacker or Play_Countries_mat[0][x_loc] == -1:
                        continue
                    # If Water
                    if Play_Countries_mat[0][x_loc] == -2:
                        if [0, x_loc] in attacker_mat:
                            continue
                        else:
                            attacker_mat.append([0, x_loc])
                            continue
                    defender = Play_Countries_mat[0][x_loc]
                    where_at = Loc_Countries_mat[0][x_loc]
                    if Loc_Countries_mat[0][x_loc] == defender:
                        type_of_announcement = 'Defeated Base'
                        
                        # If Lose Capital Lose everything
                        Number_Of_Territories = 0
                        for i in range(grid_height):
                            for j in range(grid_width):
                                if Play_Countries_mat[i][j] == defender:
                                    Play_Countries_mat[i][j] = attacker
                                    Number_Of_Territories += 1
                                    colour_square(Loc_Countries_mat[i][j], attacker, Loc_Countries_mat, Colour_Countries_mat, Play_Countries_mat)
    
                        for k in range(len(Flat_Play_Mat)):
                            if Flat_Play_Mat[k] == defender:
                                Flat_Play_Mat[k] = attacker
                                   
                    else:
                        type_of_announcement = 'Attacked not defeated'
                        Number_Of_Territories = 1
                        Play_Countries_mat[0][x_loc] = attacker
                        colour_square(Loc_Countries_mat[0][x_loc], attacker, Loc_Countries_mat, Colour_Countries_mat, Play_Countries_mat)
                    Flat_Play_Mat[x_loc] = attacker 
                count = 1
                break
                    
            # Direction = 3 ... LEFT
            elif direction == 3:
                # Can't attacker yourself can't attack mountains
                if Play_Countries_mat[y_loc][x_loc - 1] == attacker or Play_Countries_mat[y_loc][x_loc - 1] == -1:
                    continue
                # If Water
                if Play_Countries_mat[y_loc][x_loc - 1] == -2:
                    if [y_loc, x_loc - 1] in attacker_mat:
                        continue
                    else:
                        attacker_mat.append([y_loc, x_loc - 1])
                        continue                
                defender = Play_Countries_mat[y_loc][x_loc - 1]
                where_at = Loc_Countries_mat[y_loc][x_loc - 1]
                if Loc_Countries_mat[y_loc][x_loc - 1] == defender:
                    type_of_announcement = 'Defeated Base'
                        
                    # If Lose Capital Lose everything
                    Number_Of_Territories = 0
                    for i in range(grid_height):
                        for j in range(grid_width):
                            if Play_Countries_mat[i][j] == defender:
                                #print(Loc_Countries_mat)
                                Play_Countries_mat[i][j] = attacker
                                #print(Loc_Countries_mat)
                                Number_Of_Territories += 1
                                colour_square(Loc_Countries_mat[i][j], attacker, Loc_Countries_mat, Colour_Countries_mat, Play_Countries_mat)
    
                    for k in range(len(Flat_Play_Mat)):
                        if Flat_Play_Mat[k] == defender:
                            Flat_Play_Mat[k] = attacker                         
    
                else:
                    type_of_announcement = 'Attacked not defeated'
                    Number_Of_Territories = 1
                    Play_Countries_mat[y_loc][x_loc - 1] = attacker
                    colour_square(Loc_Countries_mat[y_loc][x_loc - 1], attacker, Loc_Countries_mat, Colour_Countries_mat,Play_Countries_mat)
                if x_loc == 0:
                    Flat_Play_Mat[(y_loc) * grid_width - 1]
                else:
                    Flat_Play_Mat[(y_loc * grid_width) + x_loc - 1] = attacker 
                count = 1
                break
                
            # Direction = 4 ... RIGHT  
            elif direction == 4:
                # Not on the right hand side
                if x_loc != grid_width - 1:
                    # Can't attacker yourself
                    if Play_Countries_mat[y_loc][x_loc + 1] == attacker or Play_Countries_mat[y_loc][x_loc + 1] == -1:
                        continue
                    # If Water
                    if Play_Countries_mat[y_loc][x_loc + 1] == -2:
                        if [y_loc, x_loc + 1] in attacker_mat:
                            continue
                        else:
                            attacker_mat.append([y_loc, x_loc + 1])
                            continue                    
                    defender = Play_Countries_mat[y_loc][x_loc + 1]
                    where_at = Loc_Countries_mat[y_loc][x_loc + 1]
                    if Loc_Countries_mat[y_loc][x_loc + 1] == defender:
                        type_of_announcement = 'Defeated Base'
                        
                        # If Lose Capital Lose everything
                        Number_Of_Territories = 0
                        for i in range(grid_height):
                            for j in range(grid_width):
                                if Play_Countries_mat[i][j] == defender:
                                    Play_Countries_mat[i][j] = attacker
                                    Number_Of_Territories += 1
                                    colour_square(Loc_Countries_mat[i][j], attacker, Loc_Countries_mat, Colour_Countries_mat, Play_Countries_mat)
                                    
                        for k in range(len(Flat_Play_Mat)):
                            if Flat_Play_Mat[k] == defender:
                                Flat_Play_Mat[k] = attacker
                    else:
                        type_of_announcement = 'Attacked not defeated'
                        Number_Of_Territories = 1
                        Play_Countries_mat[y_loc][x_loc + 1] = attacker
                        colour_square(Loc_Countries_mat[y_loc][x_loc + 1], attacker, Loc_Countries_mat, Colour_Countries_mat, Play_Countries_mat)
                    Flat_Play_Mat[(y_loc * grid_width) + (x_loc + 1 + 1) - 1] = attacker 
                    
                else:
                    # Can't attacker yourself
                    if Play_Countries_mat[y_loc][0] == attacker:
                        continue
                    # If Water
                    if Play_Countries_mat[y_loc][0] == -2:
                        if [y_loc, 0] in attacker_mat:
                            continue
                        else:
                            attacker_mat.append([y_loc, 0])
                            continue
                    defender = Play_Countries_mat[y_loc][0]
                    where_at = Loc_Countries_mat[y_loc][0]
                    if Loc_Countries_mat[y_loc][0] == defender:
                        type_of_announcement = 'Defeated Base'
                        
                        # If Lose Capital Lose everything
                        Number_Of_Territories = 0
                        for i in range(grid_height):
                            for j in range(grid_width):
                                if Play_Countries_mat[i][j] == defender:
                                    Play_Countries_mat[i][j] = attacker  
                                    Number_Of_Territories += 1
                                    colour_square(Loc_Countries_mat[i][j], attacker, Loc_Countries_mat, Colour_Countries_mat, Play_Countries_mat)
                        for k in range(len(Flat_Play_Mat)):
                            if Flat_Play_Mat[k] == defender:
                                Flat_Play_Mat[k] = attacker
                    else:
                        type_of_announcement = 'Attacked not defeated'
                        Number_Of_Territories = 1
                        Play_Countries_mat[y_loc][0] = attacker
                        colour_square(Loc_Countries_mat[y_loc][0], attacker, Loc_Countries_mat, Colour_Countries_mat, Play_Countries_mat)
                    Flat_Play_Mat[(y_loc + 1) * grid_width - 1] = attacker 
                count = 1 
                break
    #print(Play_Countries_mat)
    #print(Loc_Countries_mat)
    # What countries are left
    countries_mat = []
    for i in range(grid_height):
        for j in range(grid_width):
            if Play_Countries_mat[i][j] == -1:
                continue
            if Play_Countries_mat[i][j] == -2:
                continue
            if Play_Countries_mat[i][j] not in countries_mat:
                countries_mat.append(Play_Countries_mat[i][j])
    #print(countries_mat)
    #print(Loc_Countries_mat)
    #print(Flat_Play_Mat)
    from_location = Loc_Countries_mat[y_location][x_location]
    Fight_Announcement(type_of_announcement, defender, attacker, where_at, \
                      from_location, move, Number_Of_Territories, len(countries_mat))

    return Flat_Play_Mat, Play_Countries_mat, countries_mat


def Fight_Announcement(type_of_announcement, Defeated, Attacked_By, \
                 Where_At, From, Move_Number, Number_Of_Territories, Countries_Left):
    if type_of_announcement == 'Defeated Base':
        print('%d attacked %d from %d. %d lost its capital and was defeated in move %d' \
            % (Attacked_By, Defeated, From, Defeated, Move_Number))        
    
        if Number_Of_Territories >= 2:
            print('They lost %d territories.' % (Number_Of_Territories))   
    if type_of_announcement == 'Attacked not defeated':
        print('%d attacked %d in %d from %d in move %d' \
            % (Attacked_By, Defeated, Where_At, \
            From, Move_Number))
    
    #if Move_Number % 10:
    if Countries_Left > 1:
        print('There are ' + str(Countries_Left) + ' countries left.')
    
    #
    #    print('Game Over. %d Won in move %d \n' % (Attacked_By, Move_Number))


def most_frequent(Lst):
    #print(Lst)
    #while -1 in Lst:
    #    Lst.remove(-1)
    #print(Lst)
    counts = Counter(Lst)
    #print(counts)
    winning_territories = counts.most_common(1)[0][1]
    #print(max_count)
    winning_countries = [value for value, count in counts.most_common() if count == winning_territories]
    #print(out)
    
    return winning_countries, winning_territories


def Lead_Change(winning_countries, winning_countries_old, \
                winning_territories, winning_territories_old):
    #print(winning_countries[0])
    # If Lead Change
    if winning_countries == winning_countries_old and winning_territories == winning_territories_old:
        winning_commentary(winning_countries, winning_territories)
        print(str(winning_countries) + ' kept their lead')

    elif winning_countries == winning_countries_old and winning_territories != winning_territories_old:
        winning_commentary(winning_countries, winning_territories)
        if winning_territories_old < winning_territories:
            print(str(winning_countries) + ' extended their lead')
        elif winning_territories_old > winning_territories:
            print(str(winning_countries) + ' lost a bit of their lead')
            
    elif winning_countries != winning_countries_old and winning_territories == winning_territories_old:
        winning_commentary(winning_countries, winning_territories)
        if len(winning_countries) == 1:
            print(str(winning_countries[0]) + ' became the leader')
        elif len(winning_countries) > 1: 
            for elem in range(0, len(winning_countries)):
                if winning_countries[elem] in winning_countries_old:
                    continue
                else:
                    if len(winning_countries_old) == 1:
                        print(str(winning_countries[elem]) + ' joined the leader')
                    else:
                        print(str(winning_countries[elem]) + ' joined the leaders')
                    
    elif winning_countries != winning_countries_old and winning_territories != winning_territories_old:  
        winning_commentary(winning_countries, winning_territories)
        if len(winning_countries) == 1:
            print(str(winning_countries[0]) + ' became the leader')
        elif len(winning_countries) > 1: 
            for elem in range(0, len(winning_countries)):
                if winning_countries[elem] in winning_countries_old:
                    continue
                else:
                    if len(winning_countries_old) == 1:
                        print(str(winning_countries[elem]) + ' joined the leader')
                    else:
                        print(str(winning_countries[elem]) + ' joined the leaders')
    time.sleep(0.25)
#    print(winning_countries_old)
    print()
    winning_countries_old = winning_countries
    winning_territories_old = winning_territories
    return winning_countries_old, winning_territories_old


def winning_commentary(winning_countries, winning_territories):
#    print(winning_countries)
#    print(winning_territories)
    if len(winning_countries) == 1 and winning_territories > 1:
        print('%d is winning with %d territories' % (winning_countries[0], winning_territories))
    
    #elif len(winning_countries) == 2 and winning_territories > 1:
    #    print('%d and %d are winning with %d territories' \
    #          % (winning_countries[0], winning_countries[1], winning_territories))
    
    elif len(winning_countries) >= 2 and winning_territories > 1:
        print_statement = ''
        for p in range(0,len(winning_countries)):
            if winning_countries[p] == winning_countries[0]:
                print_statement += str(winning_countries[p])
            
            elif winning_countries[p] == winning_countries[-1]:
                print_statement += ' and ' + str(winning_countries[p]) + \
                    ' are winning with ' + str(winning_territories) + ' territories'
            
            else:
                print_statement += ', ' + str(winning_countries[p])
                
        print(print_statement)

def setupmapscreen(bg_colour = 'light grey',
                          line_colour = 'slate grey',
                          draw_grid = True,
                          label_spaces = True): # NO! DON'T CHANGE THIS!
    
    # Set up the drawing canvas with enough space for the grid and
    # spaces on either side
    Turtle.setup(window_grid_width, window_grid_height)
    Turtle.bgcolor(bg_colour)

    # Draw as quickly as possible
    Turtle.tracer(False)

    # Get ready to draw the grid
    Turtle.penup()
    Turtle.color(line_colour)
    Turtle.width(2)

    # Determine the left-bottom coords of the grid
    left_edge = -(grid_width * cell_size) // 2 
    bottom_edge = -(grid_height * cell_size) // 2

    # Optionally draw the grid
    if draw_grid:

        # Draw the horizontal grid lines
        Turtle.setheading(0) # face east
        for line_no in range(0, grid_height + 1):
            Turtle.penup()
            Turtle.goto(left_edge, bottom_edge + line_no * cell_size)
            Turtle.pendown()
            Turtle.forward(grid_width * cell_size)
            #print(pos())
            
        # Draw the vertical grid lines
        Turtle.setheading(90) # face north
        for line_no in range(0, grid_width + 1):
            Turtle.penup()
            Turtle.goto(left_edge + line_no * cell_size, bottom_edge)
            Turtle.pendown()
            Turtle.forward(grid_height * cell_size)
            #print(pos())
    #print(pos())
    Turtle.penup()
    Turtle.tracer(True)


        
def colour_square(location_of_square, to_what_colour, Loc_Countries_mat, Colour_Countries_mat, Play_Countries_mat):

    x_colour_location, y_colour_location = find_location(to_what_colour, Loc_Countries_mat, grid_width, grid_height)
    x_location, y_location = find_location(location_of_square, Loc_Countries_mat, grid_width, grid_height)
    

    #print(y_location)
    #print(x_location)
    Turtle.colormode(255)
    # Y Centre of square
    y_centre_of_square = (cell_size * grid_height // 2 - cell_size // 2) - (y_location * cell_size)
    
    # X Centre of Square
    x_centre_of_square = -(cell_size * grid_width // 2 + cell_size // 2) + (x_location + 1) * cell_size

    Turtle.tracer(False)
    
    #print(Colour_Countries_mat)
    # Start at Bottom Left
    Turtle.goto(x_centre_of_square - (cell_size // 2), y_centre_of_square - (cell_size // 2))
    #if Play_Countries_mat[y_location][x_location] == -2:
        #Turtle.tracer(True)
        #print(pos())
    Turtle.pendown()
    Turtle.width(1)
    Turtle.pencolor("black")
    Turtle.fillcolor(Colour_Countries_mat[y_colour_location][x_colour_location][0],\
              Colour_Countries_mat[y_colour_location][x_colour_location][1],\
              Colour_Countries_mat[y_colour_location][x_colour_location][2])
    Turtle.begin_fill()
    
    #Draw Border
    Turtle.setheading(90)
    Turtle.forward(cell_size)
    Turtle.setheading(0)
    Turtle.forward(cell_size)
    Turtle.setheading(270)
    Turtle.forward(cell_size)
    Turtle.setheading(180)
    Turtle.forward(cell_size)
    
    #Fill it
    Turtle.end_fill()
    Turtle.penup()
    
    # Is Mountain
    if Play_Countries_mat[y_location][x_location] == -1:
        draw_tree(x_centre_of_square, y_centre_of_square)
        draw_tree(x_centre_of_square + cell_size * 1/4, y_centre_of_square + cell_size * 1/4)
        draw_tree(x_centre_of_square - cell_size * 1/4, y_centre_of_square + cell_size * 1/4)
        draw_tree(x_centre_of_square + cell_size * 1/4, y_centre_of_square - cell_size * 1/4)
        draw_tree(x_centre_of_square - cell_size * 1/4, y_centre_of_square - cell_size * 1/4)
        #tracer(False)
    
    if Play_Countries_mat[y_location][x_location] == -2:
        #Turtle.tracer(True)
        wavy_outline(x_centre_of_square, y_centre_of_square, 4, 20)
        wavy_outline(x_centre_of_square, y_centre_of_square + cell_size * 1/4, 4, 20)
        wavy_outline(x_centre_of_square, y_centre_of_square - cell_size * 1/4, 4, 20)
        #Turtle.tracer(False)
    
    Turtle.tracer(True)

def draw_tree(y_start, x_start):
    Turtle.goto(y_start, x_start)

    
    #draw trunk
    Turtle.pendown()
    Turtle.width(3)
    Turtle.pencolor("brown")
    Turtle.setheading(90)
    Turtle.forward(cell_size // 10)
    #print(pos())
    Turtle.penup()
    
    Turtle.setheading(180)
    Turtle.forward(cell_size // 18)
    Turtle.setheading(90)
    Turtle.forward(cell_size // 14)
    #print(pos())
    Turtle.dot(cell_size // 6, "green")
    #print(pos())
    Turtle.goto(y_start, x_start + cell_size // 10)
    #print(pos())
    Turtle.setheading(0)
    Turtle.forward(cell_size // 18)
    #print(pos())
    Turtle.setheading(90)
    Turtle.forward(cell_size // 14)
    #print(pos())
    
    Turtle.dot(cell_size // 6, "green")

    Turtle.goto(y_start, x_start + cell_size // 10 + cell_size // 10)

    Turtle.dot(cell_size // 6, "green")
    
    #print()

# Define drawing a wave
def wavy_outline(x_start, y_start, no_of_curves, rad):
    #print(x_start)
    #print(y_start)
    #print(x_start - cell_size // 8)
    Turtle.pencolor("white")
    Turtle.width(2)
    Turtle.goto(x_start - cell_size // 3, y_start)
    Turtle.pendown()
    for curve in range(no_of_curves):
        Turtle.setheading(45)
        Turtle.circle(cell_size // -rad, extent = 90)
        Turtle.circle(cell_size // rad, extent = 90)
    Turtle.penup()
    
main()
