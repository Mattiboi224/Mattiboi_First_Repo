import turtle
import random
import sys
import signal
from collections import deque
import time
import math

wn = turtle.Screen()
main_turtle = turtle.Turtle()
total_ant = 3
total_grasshopper = 3
total_beetle = 2
total_spider = 2
total_queen = 1
side_length = 40
num_sides = 6
angle = 360.0 / num_sides
main_turtle.hideturtle()
##print(angle)

def hexagon_shape (position_x, position_y):
    
    turtle.tracer(False)
    # Start Location to Start of Hexagon
    main_turtle.color('black')
    main_turtle.goto(position_x, position_y)
    main_turtle.right(main_turtle.heading())
    main_turtle.up()
    main_turtle.left(angle * 2)
    main_turtle.forward(side_length)
    #main_turtle.right(angle * 2)
    main_turtle.right(main_turtle.heading())
    main_turtle.down()

    # Draw Hexagon
    for i in range(num_sides):
        main_turtle.forward(side_length)
        main_turtle.right(angle)

    # Back to Start Location
    main_turtle.up()
    main_turtle.right(angle)
    main_turtle.forward(side_length)
    main_turtle.left(angle)

    main_turtle.goto(position_x, position_y)
    main_turtle.right(main_turtle.heading())
    turtle.tracer(True)

#Redraw All the Tiles
def redraw_tiles(p1_tiles, p1_insect_mat, p2_tiles, p2_insect_mat, z_p1_tiles, z_p2_tiles):
    turtle.tracer(False)
    main_turtle.clear()

    # Copy Exact Location
    p1_tiles_copy = p1_tiles.copy()
    p2_tiles_copy = p2_tiles.copy()

    # Copy the insects
    p1_insect_mat_copy = p1_insect_mat.copy()
    p2_insect_mat_copy = p2_insect_mat.copy()

    # Find all the covered spots
    indicesp1 = [i for i, x in enumerate(z_p1_tiles) if x < 0]
    indicesp2 = [i for i, x in enumerate(z_p2_tiles) if x < 0]

    # Remove all the covered spots from the mat
    if len(indicesp1) >= 1:
        for i in range(len(indicesp1)):
            p1_tiles_copy.pop(indicesp1[i] - i)
            p1_insect_mat_copy.pop(indicesp1[i] - i)

    if len(indicesp2) >= 1:
        for i in range(len(indicesp2)):
            p2_tiles_copy.pop(indicesp2[i] - i)
            p2_insect_mat_copy.pop(indicesp2[i] - i)
    
    for i in range(len(p1_tiles_copy)):
        
        hexagon_shape(p1_tiles_copy[i][0],p1_tiles_copy[i][1])

        main_turtle.color('red')

        if p1_insect_mat_copy[i] == 'Queen':
            turtle.tracer(False)
            queen_drawing()
        elif p1_insect_mat_copy[i] == 'Ant':
            turtle.tracer(False)
            ant_drawing()
        elif p1_insect_mat_copy[i] == 'Grasshopper':
            turtle.tracer(False)
            grasshopper_drawing()
        elif p1_insect_mat_copy[i] == 'Beetle':
            turtle.tracer(False)
            beetle_drawing()
        elif p1_insect_mat_copy[i] == 'Spider':
            turtle.tracer(False)
            spider_drawing()

    for i in range(len(p2_tiles_copy)):

        hexagon_shape(p2_tiles_copy[i][0],p2_tiles_copy[i][1])

        main_turtle.color('green')

        if p2_insect_mat_copy[i] == 'Queen':
            turtle.tracer(False)
            queen_drawing()
            turtle.tracer(True)
        elif p2_insect_mat_copy[i] == 'Ant':
            turtle.tracer(False)
            ant_drawing()
            turtle.tracer(True)
        elif p2_insect_mat_copy[i] == 'Grasshopper':
            turtle.tracer(False)
            grasshopper_drawing()
            turtle.tracer(True)
        elif p2_insect_mat_copy[i] == 'Beetle':
            turtle.tracer(False)
            beetle_drawing()
            turtle.tracer(True)
        elif p2_insect_mat_copy[i] == 'Spider':
            turtle.tracer(False)
            spider_drawing()
            turtle.tracer(True)
    turtle.tracer(True)     
        
        

#Draw Bugs
def queen_drawing():
    main_turtle.right(90)
    main_turtle.forward(20)
    main_turtle.write("Q", False, align="center", font=("Arial", 30, "normal"))

    '''
    current_pos_x = main_turtle.xcor() 
    current_pos_y = main_turtle.ycor() + 20
    #Body
    main_turtle.up()
    main_turtle.left(90)
    main_turtle.forward(20)
    main_turtle.dot(20, "blue")
    main_turtle.right(180)
    main_turtle.forward(25)
    main_turtle.dot(40,"blue")

    #Front Legs
    main_turtle.goto(current_pos_x, current_pos_y)
    main_turtle.setheading(90)
    #main_turtle.forward(9)
    main_turtle.down()
    main_turtle.pencolor("blue")
    main_turtle.circle(20, 100)
    main_turtle.up()
    main_turtle.goto(current_pos_x, current_pos_y)
    main_turtle.setheading(-90)
    main_turtle.down()
    main_turtle.circle(20, -100)
    main_turtle.up()
    #Antenna
    main_turtle.goto(current_pos_x - 1, current_pos_y)
    main_turtle.setheading(90)
    main_turtle.down()
    main_turtle.circle(100, 12)
    main_turtle.setheading(180)
    main_turtle.forward(5)
    main_turtle.up()
    main_turtle.goto(current_pos_x + 1, current_pos_y)
    main_turtle.setheading(-90)
    main_turtle.down()
    main_turtle.circle(100, -12)
    main_turtle.setheading(0)
    main_turtle.forward(5)
    main_turtle.up()
    main_turtle.goto(current_pos_x, current_pos_y)
    '''

def grasshopper_drawing():
    main_turtle.right(90)
    main_turtle.forward(20)
    main_turtle.write("G", False, align="center", font=("Arial", 30, "normal"))

def beetle_drawing():
    main_turtle.right(90)
    main_turtle.forward(20)
    main_turtle.write("B", False, align="center", font=("Arial", 30, "normal"))

def ant_drawing():
    main_turtle.right(90)
    main_turtle.forward(20)
    main_turtle.write("A", False, align="center", font=("Arial", 30, "normal"))

def spider_drawing():
    main_turtle.right(90)
    main_turtle.forward(20)
    main_turtle.write("S", False, align="center", font=("Arial", 30, "normal"))

# Assign Title
def assign_tile (assigned_tile, turn):
    # 1 = Queen, 2 = Beetle, 3 = Spider, 4 = Ant, 5 = Grasshopper
    turtle.tracer(False)
    if turn % 2 == 0:
        main_turtle.color('green')
    
    else:
        main_turtle.color('red')
    
    if assigned_tile == 'Queen':
        queen_drawing()
        assigned_tile = 'Queen'
    elif assigned_tile == 'Beetle':
        beetle_drawing()
        assigned_tile = 'Beetle'
    elif assigned_tile == 'Spider':
        spider_drawing()
        assigned_tile = 'Spider'
    elif assigned_tile == 'Ant':
        ant_drawing()
        assigned_tile = 'Ant'
    elif assigned_tile == 'Grasshopper':
        grasshopper_drawing()
        assigned_tile = 'Grasshopper'
    
    turtle.tracer(True)

def getlocations(posx, posy):
    avaliable_position = []
    
    for i in range(6):
        turtle.tracer(False)
        main_turtle.goto(posx, posy)
        main_turtle.setheading(0)
        main_turtle.up()
        main_turtle.left(150 - 60 * i)
        main_turtle.forward(side_length * math.sqrt(3))
        main_turtle.right(150)
        main_turtle.setheading(0)
        xpos = main_turtle.xcor()
        ypos = main_turtle.ycor()
        avaliable_position.append([round(xpos,3), round(ypos,3)])
        turtle.tracer(True)
    
    return avaliable_position
        

# Place First Tile
# Draw the Hexagon

# Get all avaliable edge locations in the Hive
def get_all_locations(current_tile_mat, original_tile):
    tot_mat = []
    for a in range(len(current_tile_mat)):
        if current_tile_mat[a] == original_tile:
            continue
        a_pos = getlocations(current_tile_mat[a][0], current_tile_mat[a][1])

        for b in range(len(a_pos)):
            if a_pos[b] in current_tile_mat:
                continue

            if a_pos[b] in tot_mat:
                continue

            tot_mat.append(a_pos[b])
    return tot_mat

# For a set of positions return which are slidable
def slideable_locs(location,current_tile_mat):
    slideable_mat_filled = []
    slideable_mat = []
    
    for i in range(len(location)):
        if location[i] in current_tile_mat:
            slideable_mat_filled.append(1)
        else:
            slideable_mat_filled.append(0)
            
    for j in range(len(slideable_mat_filled)):
        if slideable_mat_filled[j] == 0 and slideable_mat_filled[j - 1] == 0:
            if location[j] not in slideable_mat:
                slideable_mat.append(location[j])
            if location[j - 1] not in slideable_mat:
                slideable_mat.append(location[j - 1])

    return slideable_mat

def filled_loc(location, current_tile_mat):

    all_locs = getlocations(location[0],location[1])
    filled_mat = []
    for i in range(len(all_locs)):
        if all_locs[i] in current_tile_mat:
            filled_mat.append(all_locs[i])

    return filled_mat

def connected_tiles(original_tile, current_tile_mat):
    final_output = False

    next_to_mat = []
    
    # Find all the filled positions next to tile
    position = getlocations(original_tile[0], original_tile[1])
    position_tup = [tuple(inner_list) for inner_list in position]
    current_tile_mat_tup = [tuple(inner_list) for inner_list in current_tile_mat]
    
    
    # Create Matrix that shows which tiles are filled
    for pos in position_tup:
        if pos in current_tile_mat_tup:
            next_to_mat.append(pos)

    number_of_tiles = 0
    # If there is 0 then this is a bug and continue
    if len(next_to_mat) == 0:
        place_move_rand = random.randint(0,1)
        final_output = False

    if len(next_to_mat) == 1:
        final_output = True
            
    # If there is 2 or more determine if they are next to each other or connected via another pathway
    elif len(next_to_mat) in [2,3,4]:
        final_output = True
        # For each tile next to the main tile determine if they next to the other tiles surrounding the main tile
        for s in range(len(next_to_mat)):
            for t in range(s + 1, len(next_to_mat)):
                if not is_connected(next_to_mat[s], next_to_mat[t], current_tile_mat_tup, [(original_tile[0], original_tile[1])]):
                    final_output = False
                    break
                if not final_output:
                    break
                
        if not final_output:
            final_output = False

    elif len(next_to_mat) in [5,6]:
        final_output = True

    return final_output

def queen_logic(original_tile, current_tile_mat):

    position = getlocations(original_tile[0], original_tile[1])

    open_loc = slideable_locs(position, current_tile_mat)

    final_pos = []
    
    for p in range(len(open_loc)):
        
        # Already Exists
        if open_loc[p] in current_tile_mat:
            continue

        # Already in the available locations matrix
        if open_loc[p] in final_pos:
            continue

        # Check in next to a current tile
        # Get all the location surround an option
        in_mat = getlocations(open_loc[p][0], open_loc[p][1])

        if original_tile in in_mat:
            in_mat.remove(original_tile)

        #Check to see if it's next to an existing tile
        for q in range(len(in_mat)):
            if in_mat[q] in current_tile_mat and open_loc[p] not in final_pos:
                if open_loc[p] in final_pos:
                    continue
                final_pos.append(open_loc[p])

    return final_pos

def spider_logic(original_tile, current_tile_mat):

    tile = (original_tile[0], original_tile[1])
    
    position = getlocations(tile[0], tile[1])
    slideable_mat = slideable_locs(position, current_tile_mat)
    next_to_something = []
    final_position = []

    #while slideable_mat:
    for i in range(3):
        new_slideables = []

        for x, y in slideable_mat:
            check_locs = getlocations(x, y)

            if any(loc in current_tile_mat and loc != tile for loc in check_locs):
                if [x, y] not in next_to_something:
                    next_to_something.append([x, y])
                    new_slideables.extend(slideable_locs(getlocations(x, y), current_tile_mat))
                    if i == 2:
                        final_position.append([x,y])

        slideable_mat = new_slideables

    return final_position

def grasshopper_pathway(original_tile, current_tile_mat):  ##(start, filled_close_pos_mat, current_tile, current_tile_mat, close_pos_mat):

    # Get everything that is around
    position = getlocations(original_tile[0], original_tile[1])
    original_tile_tup = tuple(original_tile)
    current_tile_mat_tup = [tuple(inner_list) for inner_list in current_tile_mat]
    
    filled_local = []
    
    for h in range(len(position)):
        if position[h] in current_tile_mat:
            filled_local.append(position[h])

    filled_local = [tuple(inner_list) for inner_list in filled_local]
    position = [tuple(inner_list) for inner_list in position]

    #grasshopper_pathway(original_tile_tup, filled_local, original_tile_tup, current_tile_mat_tup, position)
    
    visited = set()
    queue = []
    
    for i in range(len(filled_local)):
        queue.append(filled_local[i])
    
    queue = deque(queue)
    final_loc = []
    
    while queue:
        current = queue.popleft()
        #print(current)

        if current in visited:
            continue
        
        visited.add(current)
        
        neighbors = getlocations(current[0], current[1])
        neighbors = [tuple(inner_list) for inner_list in neighbors]

        for i in range(len(filled_local)):     
            for neighbor in neighbors:
                if neighbor not in visited and is_on_line(original_tile_tup[0], original_tile_tup[1], filled_local[i][0], filled_local[i][1], neighbor[0], neighbor[1]) and neighbor != original_tile_tup:
                    if neighbor in current_tile_mat_tup:
                        queue.append(neighbor)
                    else:
                        if neighbor in position and neighbor not in filled_local:
                            continue
                        if neighbor not in final_loc:
                            final_loc.append(neighbor)

    return final_loc

def beetle_logic(original_tile, current_tile_mat):

    final_loc = []
    # Get Everything around the Beetle
    position = getlocations(original_tile[0], original_tile[1])

    # For every position make sure it's next to something
    for i in range(len(position)):
        local_pos = getlocations(position[i][0], position[i][1])
        
        for j in range(len(local_pos)):
            
            # Ignore Original Tile
            if local_pos[j] in current_tile_mat and local_pos[j] != original_tile:
                final_loc.append(position[i])

    return final_loc

def ant_logic(original_tile, current_tile_mat):
    final_loc = []
    # Get every location on the edge of the board
    position = get_all_locations(current_tile_mat, original_tile)
    position_tup = [tuple(inner_list) for inner_list in position]
    
    for j in range(len(position)):
        check_locs = getlocations(position[j][0], position[j][1])
        #print('Check Locs: ')
        #print(check_locs)
        # Check if can slide into the location
        slideable_get_locs = slideable_locs(check_locs, current_tile_mat)
        #print(slideable_get_locs)

        # If you can't slide into position
        if len(slideable_get_locs) == 0:
            continue

        avaliable_pos = tuple(position[j])
        
        # For the slidable position are they linked to the main position
        if is_connected(avaliable_pos, (original_tile[0], original_tile[1]), position_tup, (original_tile[0], original_tile[1])):
                final_loc.append(position[j])    

    return final_loc

def is_on_line(a, b, c, d, x, y):
    m_top = d - b
    m_bot = c - a

    if m_top == 0:
        if y == d:
            return True
        else:
            return False

    if m_bot == 0:
        if x == c:
            return True
        else:
            return False

    m = m_top / m_bot

    c = - m * a + b

    if y == round(m * x + c, 3):
        return True
    else:
        return False

def is_connected(start, end, current_tile_mat, current_tile):
    
    visited = set()
    queue = deque([start])
    
    while queue:
        current = queue.popleft()
        
        if current == end:
            return True

        if current in visited:
            continue
        
        visited.add(current)
        
        neighbors = getlocations(current[0], current[1])
        neighbors = [tuple(inner_list) for inner_list in neighbors]
        if end != current_tile:
            for neighbor in neighbors:
                if neighbor in current_tile_mat and neighbor not in visited and neighbor not in current_tile:
                    queue.append(neighbor)

        elif end == current_tile:
            for neighbor in neighbors:
                if (neighbor in current_tile_mat and neighbor not in visited) or neighbor == current_tile:
                    queue.append(neighbor)
        
    return False

def placement(game, place_move_rand, current_tile_mat, ava_pos, place_move_mat, place_move_insect, original_position_mat, team_tiles, opp_team, team_insect):
#        elif game % 2 == 0 and game != 0 and place_move_rand == 0:

    for k in range(len(current_tile_mat)):

        # Opposing Team's Tiles
        if current_tile_mat[k] in opp_team:
            continue
        
        position = getlocations(current_tile_mat[k][0], current_tile_mat[k][1])
                        
        # Clean out filled positions
        for j in range(len(position)):

            if position[j] in current_tile_mat:
                continue

            check_loc = getlocations(position[j][0], position[j][1])
            checking_num = 0

            # If next to opposing tile can't use
            for m in range(len(check_loc)):
                if check_loc[m] in opp_team:
                    continue
                
                checking_num += 1

            if checking_num == len(check_loc):

                # Assign the tile
                for random_num in range(5):
                    random_num += 1

                    # Must Play a Queen in the first 3 Turns
                    if game >= 6 and 'Queen' not in team_insect:
                        random_num = 1
                        if position[j] in ava_pos:

                            index = [i for i, x in enumerate(ava_pos) if x == position[j]]
                            
                            for z in range(len(index)):
                                if place_move_mat[z] == 0 and (random_num == 1 and place_move_insect[z] == 'Queen'):
                                    continue
                                else:
                                    ava_pos.append(position[j])
                                    place_move_mat.append(place_move_rand)
                                    place_move_insect.append('Queen')
                                    original_position_mat.append(position[j])
                        else:
                            ava_pos.append(position[j])
                            place_move_mat.append(place_move_rand)
                            place_move_insect.append('Queen')
                            original_position_mat.append(position[j])

                    # If you have a queen don't play another
                    elif 'Queen' in team_insect and random_num == 1:
                        continue

                    elif team_insect.count('Beetle') == 2 and random_num == 2:
                        continue   
                    
                    elif team_insect.count('Spider') == 2 and random_num == 3:
                        continue

                    elif team_insect.count('Ant') == 3 and random_num == 4:
                        continue

                    elif team_insect.count('Grasshopper') == 3 and random_num == 5:
                        continue                    

                    else:
                
                        if position[j] in ava_pos:
                            index = [i for i, x in enumerate(ava_pos) if x == position[j]]
                            
                            for z in range(len(index)):
                                if place_move_mat[index[z]] == 0 and ((random_num == 1 and place_move_insect[z] == 'Queen') or \
                                                               (random_num == 2 and place_move_insect[z] == 'Beetle') or \
                                                               (random_num == 3 and place_move_insect[z] == 'Spider') or \
                                                               (random_num == 4 and place_move_insect[z] == 'Ant') or \
                                                               (random_num == 5 and place_move_insect[z] == 'Grasshopper')):
                                    continue

                        if random_num == 1:
                            ava_pos.append(position[j])
                            place_move_mat.append(place_move_rand)
                            place_move_insect.append('Queen')
                            original_position_mat.append(position[j])
                            

                        if random_num == 2:
                            ava_pos.append(position[j])
                            place_move_mat.append(place_move_rand)
                            place_move_insect.append('Beetle')
                            original_position_mat.append(position[j])

                        if random_num == 3:
                            ava_pos.append(position[j])
                            place_move_mat.append(place_move_rand)
                            place_move_insect.append('Spider')
                            original_position_mat.append(position[j])

                        if random_num == 4:
                            ava_pos.append(position[j])
                            place_move_mat.append(place_move_rand)
                            place_move_insect.append('Ant')
                            original_position_mat.append(position[j])

                        if random_num == 5:
                            ava_pos.append(position[j])
                            place_move_mat.append(place_move_rand)
                            place_move_insect.append('Grasshopper')
                            original_position_mat.append(position[j])    

    return ava_pos, place_move_mat, place_move_insect, original_position_mat

def available_moves (game, current_tile_mat, current_bug_mat, p1_tiles, p2_tiles, z_p1_tiles, z_p2_tiles, p1_insect_mat, p2_insect_mat):

    ava_pos = []
    final_pos = []
    place_move_mat = []
    place_move_insect = []
    original_position_mat = []

    # Determine if a place or move action
    # Place = 0 and Move = 1
    #place_move_rand = random.randint(0,1)
    #place_move_rand = 0

##        if game == 7:
##            place_move_rand = 1
    can_go = 0
    
        # Player 2's first tile
        # Determine who's turn it is
#        while can_go == 0:
    for place_move_rand in range(2):
        can_go = 0
        #place_move_rand = random.randint(0,1)
        

        # Must Place Queen in
        if game == 7 and 'Queen' not in p1_insect_mat:
            place_move_rand = 0

        if game == 6 and 'Queen' not in p2_insect_mat:
            place_move_rand = 0

        if game < 7 and game % 2 == 0 and 'Queen' not in p2_insect_mat:
            place_move_rand = 0

        if game < 6 and game % 2 == 1 and 'Queen' not in p1_insect_mat:
            place_move_rand = 0

        if game == 0:

            ava_pos.append([0,0])
            place_move_mat.append(0)
            original_position_mat.append([0,0])

            rand = random.randint(1,5)
            if rand == 1:
                place_move_insect.append('Queen')
            elif rand == 2:
                place_move_insect.append('Beetle')
            elif rand == 3:
                place_move_insect.append('Spider')
            elif rand == 4:
                place_move_insect.append('Ant')
            elif rand == 5:
                place_move_insect.append('Grasshopper')
            
        elif game == 1:
            for k in range(len(current_tile_mat)):
                positions = getlocations(current_tile_mat[0][0], current_tile_mat[0][1])
        
        
        
        # Clean out filled positions
                for j in range(len(positions)):
                    
                    if positions[j] in current_tile_mat:
                        continue

                    if positions[j] in ava_pos:
                        continue

                    ava_pos.append(positions[j])
                    place_move_mat.append(place_move_rand)
                    original_position_mat.append(positions[j])
                    rand = random.randint(1,5)
                    if rand == 1:
                        place_move_insect.append('Queen')
                    elif rand == 2:
                        place_move_insect.append('Beetle')
                    elif rand == 3:
                        place_move_insect.append('Spider')
                    elif rand == 4:
                        place_move_insect.append('Ant')
                    elif rand == 5:
                        place_move_insect.append('Grasshopper')

            ####### Insect Needs Moving up to selection

##                can_go = 1
##                break
        
############################################## Player 2 Placement ###########################################################################
        
        # Player 2's Turn and places a tile         
        elif game % 2 == 0 and game != 0 and place_move_rand == 0:
            # Too Many Tiles
            if len(p2_insect_mat) == 11:
                continue

            ava_pos, place_move_mat, place_move_insect, original_position_mat = placement(game, place_move_rand, current_tile_mat, ava_pos, place_move_mat, place_move_insect, original_position_mat, p2_tiles, p1_tiles, p2_insect_mat)

##                if len(ava_pos) >= 1:
##                    can_go = 1
##                    break
##
##                else:
##                    can_go = 0
##                    continue

############################################## Player 1 Placement ###########################################################################
            
        # Player 1's Turn and places a tile
        elif game % 2 == 1 and game != 1 and place_move_rand == 0:
            if len(p1_insect_mat) == 11:
                continue

            ava_pos, place_move_mat, place_move_insect, original_position_mat = placement(game, place_move_rand, current_tile_mat, ava_pos, place_move_mat, place_move_insect, original_position_mat, p1_tiles, p2_tiles, p1_insect_mat)

            #print(place_move_rand)
                                    
##                if len(ava_pos) >= 1:
##                    can_go = 1
##                    break

##                else:
##                    can_go = 0
##                    continue
            
############################################## Player 2 Movement ###########################################################################
            
        # Player 2 Moves a Tile
        elif game % 2 == 0 and game != 0 and place_move_rand == 1:

            for pick_a_tile in range(len(p2_tiles)):
                
            
##                #Green
##                while True:
##                    pick_a_tile = random.randint(0, len(p2_tiles)-1)

                if z_p2_tiles[pick_a_tile] < 0:
                    continue

                original_tile = [p2_tiles[pick_a_tile][0], p2_tiles[pick_a_tile][1]]
                position = getlocations(original_tile[0], original_tile[1])
                       
                # Check for Slideable
                open_loc = slideable_locs(position, current_tile_mat)

                if len(open_loc) == 0 and (p2_insect_mat[pick_a_tile] == 'Queen' or p2_insect_mat[pick_a_tile] == 'Ant' or p2_insect_mat[pick_a_tile] == 'Spider'):
                    continue

                # Check if Breaking the Hive
                connected = connected_tiles(original_tile, current_tile_mat)

                if not connected:
                    continue
                
                # If Selected tile is queen
                if p2_insect_mat[pick_a_tile] == 'Queen':

                    choice_pos = queen_logic(original_tile, current_tile_mat)

                    for i in range(len(choice_pos)):
                        ava_pos.append(choice_pos[i])
                        place_move_mat.append(place_move_rand)
                        place_move_insect.append(p2_insect_mat[pick_a_tile])
                        original_position_mat.append(original_tile)

                elif p2_insect_mat[pick_a_tile] == 'Ant':

                    choice_pos = ant_logic(original_tile, current_tile_mat)

                    for i in range(len(choice_pos)):
                        ava_pos.append(choice_pos[i])
                        place_move_mat.append(place_move_rand)
                        place_move_insect.append(p2_insect_mat[pick_a_tile])
                        original_position_mat.append(original_tile)
                        
                elif p2_insect_mat[pick_a_tile] == 'Spider':
                    
                    choice_pos = spider_logic(original_tile, current_tile_mat)

                    for i in range(len(choice_pos)):
                        ava_pos.append(choice_pos[i])
                        place_move_mat.append(place_move_rand)
                        place_move_insect.append(p2_insect_mat[pick_a_tile])
                        original_position_mat.append(original_tile)
                        
                elif p2_insect_mat[pick_a_tile] == 'Grasshopper':

                    choice_pos = grasshopper_pathway(original_tile, current_tile_mat)
                    choice_pos = [list(inner_list) for inner_list in choice_pos]

                    for i in range(len(choice_pos)):
                        ava_pos.append(choice_pos[i])
                        place_move_mat.append(place_move_rand)
                        place_move_insect.append(p2_insect_mat[pick_a_tile])
                        original_position_mat.append(original_tile)
                        
                elif p2_insect_mat[pick_a_tile] == 'Beetle':

                    choice_pos = beetle_logic(original_tile, current_tile_mat)
                    

                    for i in range(len(choice_pos)):
                        ava_pos.append(choice_pos[i])
                        place_move_mat.append(place_move_rand)
                        place_move_insect.append(p2_insect_mat[pick_a_tile])
                        original_position_mat.append(original_tile)

##                    if len(ava_pos) >= 1:
##                        can_go = 1
##                        break
##
##                    else:
##                        can_go = 0
##                        continue

############################################## Player 1 Movement ###########################################################################
            
        # Player 1 Moves the Queen Tile
        elif game % 2 == 1 and game != 1 and place_move_rand == 1:
            
#                while True:
#                    pick_a_tile = random.randint(0, len(p1_tiles)-1)

            for pick_a_tile in range(len(p1_tiles)):

                
                if z_p1_tiles[pick_a_tile] < 0:
                    continue

                original_tile = [p1_tiles[pick_a_tile][0], p1_tiles[pick_a_tile][1]]
                position = getlocations(original_tile[0], original_tile[1])

                open_loc = slideable_locs(position, current_tile_mat)

                # These pieces can't slide out
                if len(open_loc) == 0 and (p1_insect_mat[pick_a_tile] == 'Queen' or p1_insect_mat[pick_a_tile] == 'Ant' or p1_insect_mat[pick_a_tile] == 'Spider'):
                    continue

                # Check if Breaking the Hive
                connected = connected_tiles(original_tile, current_tile_mat)

                if not connected:
                    continue
                
                if p1_insect_mat[pick_a_tile] == 'Queen':

                    choice_pos = queen_logic(original_tile, current_tile_mat)

                    for i in range(len(choice_pos)):
                        ava_pos.append(choice_pos[i])
                        place_move_mat.append(place_move_rand)
                        place_move_insect.append(p1_insect_mat[pick_a_tile])
                        original_position_mat.append(original_tile)
                                                
                elif p1_insect_mat[pick_a_tile] == 'Ant':

                    choice_pos = ant_logic(original_tile, current_tile_mat)

                    for i in range(len(choice_pos)):
                        ava_pos.append(choice_pos[i])
                        place_move_mat.append(place_move_rand)
                        place_move_insect.append(p1_insect_mat[pick_a_tile])
                        original_position_mat.append(original_tile)
                                                                    
                elif p1_insect_mat[pick_a_tile] == 'Spider':
                    
                    choice_pos = spider_logic(original_tile, current_tile_mat)

                    for i in range(len(choice_pos)):
                        ava_pos.append(choice_pos[i])
                        place_move_mat.append(place_move_rand)
                        place_move_insect.append(p1_insect_mat[pick_a_tile])
                        original_position_mat.append(original_tile)
                                                
                elif p1_insect_mat[pick_a_tile] == 'Grasshopper':
                    
                    choice_pos = grasshopper_pathway(original_tile, current_tile_mat)
                    choice_pos = [list(inner_list) for inner_list in choice_pos]

                    for i in range(len(choice_pos)):
                        ava_pos.append(choice_pos[i])
                        place_move_mat.append(place_move_rand)
                        place_move_insect.append(p1_insect_mat[pick_a_tile])
                        original_position_mat.append(original_tile)
                                                
                elif p1_insect_mat[pick_a_tile] == 'Beetle':
                    
                    choice_pos = beetle_logic(original_tile, current_tile_mat)

                    for i in range(len(choice_pos)):
                        ava_pos.append(choice_pos[i])
                        place_move_mat.append(place_move_rand)
                        place_move_insect.append(p1_insect_mat[pick_a_tile])
                        original_position_mat.append(original_tile)
                        
    return ava_pos, final_pos, place_move_mat, place_move_insect, original_position_mat

def scoring(points_ranking, move_place, insect_type, new_pos, orig_pos, own_queen_mat, opp_queen_mat, \
            own_tiles, opp_tiles, own_insect_mat, opp_insect_mat, opp_queen_loc, filled_own_queen_mat, \
            filled_opp_queen_mat, connect_to_own, connect_to_opp, current_tile_mat, current_tile_mat_copy, game):

    # Move next opposing queen!
    if move_place == 1 and new_pos in opp_queen_mat and orig_pos not in opp_queen_mat and insect_type != 'Queen' and new_pos not in current_tile_mat:
        points_ranking += 50

        slideable = slideable_locs(opp_queen_mat, current_tile_mat)
        slideable_mod = slideable_locs(opp_queen_mat, current_tile_mat_copy)

        # Win Game
        if len(filled_opp_queen_mat) == 5:
            points_ranking += 500

        # Win Game
        if len(filled_opp_queen_mat) == 4:
            points_ranking += 75

        # Adding Bonus Point based on location
        if len(slideable) == len(slideable_mod):
            points_ranking += 0

        elif len(slideable) - len(slideable_mod) == 1:
            points_ranking += 20
            
        # Blocking a slide
        elif len(slideable) - len(slideable_mod) == 2:
            points_ranking += 35

        # Blocking an exit
        elif len(slideable) - len(slideable_mod) == 3:
            points_ranking += 40

        else:
            points_ranking += 55

    # Move Bettle on a piece which next to the opposing queen!
    if move_place == 1 and new_pos in opp_queen_mat and orig_pos not in opp_queen_mat and insect_type != 'Queen' and new_pos in current_tile_mat:
        points_ranking += 20

        slideable = slideable_locs(opp_queen_mat, current_tile_mat)
        slideable_mod = slideable_locs(opp_queen_mat, current_tile_mat_copy)

        # Win Game
        if len(filled_opp_queen_mat) == 5:
            points_ranking += 300

        # Adding Bonus Point based on location
        if len(slideable) == len(slideable_mod):
            points_ranking += 0

        elif len(slideable) - len(slideable_mod) == 1:
            points_ranking += 10
            
        # Blocking a slide
        elif len(slideable) - len(slideable_mod) == 2:
            points_ranking += 15

        # Blocking an exit
        elif len(slideable) - len(slideable_mod) == 3:
            points_ranking += 20

        else:
            points_ranking += 25

    # Move next to own queen defensive piece
    if move_place == 1 and new_pos in own_queen_mat and len(filled_own_queen_mat) <= 3 and insect_type != 'Queen':
        points_ranking += 15

    # Move a piece that blocks queen
    if move_place == 1 and new_pos in own_queen_mat and len(filled_own_queen_mat) == 4 and insect_type != 'Queen':
        points_ranking += -15

        slideable = slideable_locs(opp_queen_mat, current_tile_mat)
        slideable_mod = slideable_locs(opp_queen_mat, current_tile_mat_copy)        

        # Now not slideable and probably will lose
        if len(slideable) == 2 and len(slideable_mod) == 0:
            points_ranking += -20

    if 'Queen' in opp_insect_mat:
        slideable = slideable_locs(opp_queen_mat, current_tile_mat)
        # Sit Beetle on Queen and Queen Can Move and Slide Out
        if move_place == 1 and insect_type == 'Beetle' and opp_tiles[opp_queen_loc] == new_pos and len(slideable) > 0 and connect_to_own:
            points_ranking += 50

        # Sit Beetle on Queen and Queen Can't Move but can slide out
        if move_place == 1 and insect_type == 'Beetle' and opp_tiles[opp_queen_loc] == new_pos and len(slideable) > 0 and not connect_to_own:
            points_ranking += 35

        # Sit Beetle on Queen and Queen Can't Move and can't slide out
        if move_place == 1 and insect_type == 'Beetle' and opp_tiles[opp_queen_loc] == new_pos and len(slideable) == 0 and not connect_to_own:
            points_ranking += 30

    # Move a piece that loses the game
    if move_place == 1 and new_pos in own_queen_mat and len(filled_own_queen_mat) == 5:
        points_ranking += -100

    #ava_pos_new, final_pos_new, place_move_mat_new, place_move_insect_new, original_position_mat_new = available_moves(game, current_tile_mat, current_bug_mat, opp_tiles, own_tiles, z_p1_tiles, z_p2_tiles, opp_insect_mat, own_insect_mat)

    # Placing piece priority
    if move_place == 0 and game >= 3:

        if insect_type == 'Beetle' and 'Queen' in own_insect_mat:
            beetle_pos = beetle_logic(new_pos, current_tile_mat_copy)
            current_tile_mat_copy.pop(-1)
            one_time = 1
            for p in range(len(beetle_pos)):
                if beetle_pos[p] in opp_queen_mat:
                    points_ranking += 10
                    current_tile_mat_copy.append(beetle_pos[p])

                    slideable = slideable_locs(opp_queen_mat, current_tile_mat)
                    slideable_mod = slideable_locs(opp_queen_mat, current_tile_mat_copy)
                    
                    # Win Game
                    if len(filled_opp_queen_mat) == 5:
                        if one_time == 1:
                            points_ranking += 30

                    # Adding Bonus Point based on location
                    if len(slideable) == len(slideable_mod):
                        points_ranking += 0

                    elif len(slideable) - len(slideable_mod) == 1:
                        points_ranking += 2
                        
                    # Blocking a slide
                    elif len(slideable) - len(slideable_mod) == 2:
                        points_ranking += 5

                    # Blocking an exit
                    elif len(slideable) - len(slideable_mod) == 3:
                        points_ranking += 10

                    current_tile_mat_copy.pop(-1)

        if insect_type == 'Spider' and 'Queen' in opp_insect_mat:
            spider_pos = spider_logic(new_pos, current_tile_mat_copy)
            current_tile_mat_copy.pop(-1)
            for p in range(len(spider_pos)):
                if spider_pos[p] in own_queen_mat:
                    points_ranking += 15

                    current_tile_mat_copy.append(spider_pos[p])

                    slideable = slideable_locs(opp_queen_mat, current_tile_mat)
                    slideable_mod = slideable_locs(opp_queen_mat, current_tile_mat_copy)

                    # Win Game
                    if len(filled_opp_queen_mat) == 5:
                        points_ranking += 40

                    # Win Game
                    if len(filled_opp_queen_mat) == 4:
                        points_ranking += 30

                    # Adding Bonus Point based on location
                    if len(slideable) == len(slideable_mod):
                        points_ranking += 0

                    elif len(slideable) - len(slideable_mod) == 1:
                        points_ranking += 2
                        
                    # Blocking a slide
                    elif len(slideable) - len(slideable_mod) == 2:
                        points_ranking += 5

                    # Blocking an exit
                    elif len(slideable) - len(slideable_mod) == 3:
                        points_ranking += 10

                    current_tile_mat_copy.pop(-1)


        if insect_type == 'Ant' and 'Queen' in opp_insect_mat:

            ant_pos = ant_logic(new_pos, current_tile_mat_copy)
            current_tile_mat_copy.pop(-1)
            for p in range(len(ant_pos)):
                if ant_pos[p] in opp_queen_mat:
                    points_ranking += 5

                    current_tile_mat_copy.append(ant_pos[p])

                    slideable = slideable_locs(opp_queen_mat, current_tile_mat)
                    slideable_mod = slideable_locs(opp_queen_mat, current_tile_mat_copy)

                    # Win Game
                    if len(filled_opp_queen_mat) == 5:
                        points_ranking += 40

                    # Win Game
                    if len(filled_opp_queen_mat) == 4:
                        points_ranking += 30

                    # Adding Bonus Point based on location
                    if len(slideable) == len(slideable_mod):
                        points_ranking += 0

                    elif len(slideable) - len(slideable_mod) == 1:
                        points_ranking += 2
                        
                    # Blocking a slide
                    elif len(slideable) - len(slideable_mod) == 2:
                        points_ranking += 5

                    # Blocking an exit
                    elif len(slideable) - len(slideable_mod) == 3:
                        points_ranking += 10

                    current_tile_mat_copy.pop(-1)
                    
        if insect_type == 'Grasshopper' and 'Queen' in opp_insect_mat:
            grass_pos = grasshopper_pathway(new_pos, current_tile_mat_copy)
            grass_pos = [list(inner_list) for inner_list in grass_pos]
            current_tile_mat_copy.pop(-1)
            
            for p in range(len(grass_pos)):
                if grass_pos[p] in opp_queen_mat:
                    points_ranking += 15

                    current_tile_mat_copy.append(grass_pos[p])

                    slideable = slideable_locs(opp_queen_mat, current_tile_mat)
                    slideable_mod = slideable_locs(opp_queen_mat, current_tile_mat_copy)

                    # Win Game
                    if len(filled_opp_queen_mat) == 5:
                        points_ranking += 40

                    # Win Game
                    if len(filled_opp_queen_mat) == 4:
                        points_ranking += 30

                    # Adding Bonus Point based on location
                    if len(slideable) == len(slideable_mod):
                        points_ranking += 10

                    elif len(slideable) - len(slideable_mod) == 1:
                        points_ranking += 15
                        
                    # Blocking a slide
                    elif len(slideable) - len(slideable_mod) == 2:
                        points_ranking += 10

                    # Blocking an exit
                    elif len(slideable) - len(slideable_mod) == 3:
                        points_ranking += 15

                    current_tile_mat_copy.pop(-1)
    return points_ranking

def board_updates(game, placement, tile, loc, insect, p1_tiles, p2_tiles, p1_insect_mat, p2_insect_mat, z_p1_tiles, z_p2_tiles, current_tile_mat, current_bug_mat):

##    insect = place_move_insect[ran_loc]
##    tile = original_position_mat[ran_loc]
##    loc = final_pos[ran_loc]
##    placement = place_move_mat[ran_loc]

    # Placing Tiles Logic
    if placement == 0 or game == 0 or game == 1:
        #time.sleep(0.25)
        turtle.tracer(False)
        main_turtle.goto(loc[0],loc[1])
        # Draw shape and put assigned name
        hexagon_shape(loc[0],loc[1])

        main_turtle.color('black')
        
        main_turtle.goto(loc[0],loc[1])
        current_tile_mat.append([loc[0],loc[1]])
        
        assign_tile(insect, game)
        
        if game % 2 == 1:
            p1_tiles.append([loc[0],loc[1]])
            p1_insect_mat.append(insect)
            current_bug_mat.append(insect)
            z_p1_tiles.append(0)

            #print(p1_tiles)
        else:
            p2_tiles.append([loc[0],loc[1]])
            p2_insect_mat.append(insect)
            current_bug_mat.append(insect)
            z_p2_tiles.append(0)

        turtle.tracer(True)
        #time.sleep(0.25)
        
    else:
        #time.sleep(0.25)
        #print(ava_pos)
        # If P2
        
        if game % 2 == 0:

            for b in range(len(p2_tiles)):
                if p2_tiles[b] == tile and p2_insect_mat[b] == insect and z_p2_tiles[b] >= 0:               

                    # If Beetle going on top of another tile change the z axis
                    if insect == 'Beetle':

                        # If Currently on a tile
                        if z_p2_tiles[b] == 1:
                            # Find Everything it's sitting on top of
                            filled_indicesp1 = [i for i, x in enumerate(p1_tiles) if x == p2_tiles[b]]
                            filled_indicesp2 = [i for i, x in enumerate(p2_tiles) if x == p2_tiles[b]]
                            
                            # Re-adjust everything underneath
                            if len(filled_indicesp1) > 0:
                                for i in range(len(filled_indicesp1)):
                                    # If not the original_tile cause it's on top
                                    if z_p1_tiles[filled_indicesp1[i]] != 1:
                                        # Determine if it's a stack of 3 or more
                                        if len(filled_indicesp1) + len(filled_indicesp2) >= 3:
                                            # Promote the Highest Beetle to be on top
                                            if z_p1_tiles[filled_indicesp1[i]] == -1:
                                                z_p1_tiles[filled_indicesp1[i]] = 1
                                            else:
                                                z_p1_tiles[filled_indicesp1[i]] += 1
                                        # Not a stack of beetles
                                        else:
                                            if z_p1_tiles[filled_indicesp1[i]] == -1:
                                                z_p1_tiles[filled_indicesp1[i]] = 0
                                        

                            # Re-adjust everything underneath
                            if len(filled_indicesp2) > 0:
                                for i in range(len(filled_indicesp2)):
                                    # If not the original_tile cause it's on top
                                    if z_p2_tiles[filled_indicesp2[i]] != 1:
                                        # Determine if it's a stack of 3 or more
                                        if len(filled_indicesp1) + len(filled_indicesp2) >= 3:
                                            # Promote the Highest Beetle to be on top
                                            if z_p2_tiles[filled_indicesp2[i]] == -1:
                                                z_p2_tiles[filled_indicesp2[i]] = 1
                                            else:
                                                z_p2_tiles[filled_indicesp2[i]] += 1
                                        # Not a stack of beetles
                                        else:
                                            if z_p2_tiles[filled_indicesp2[i]] == -1:
                                                z_p2_tiles[filled_indicesp2[i]] = 0


                        # If moving onto something
                        if loc in p1_tiles or loc in p2_tiles:
                            
                            z_p2_tiles[b] = 1
                            indicesp1 = [i for i, x in enumerate(p1_tiles) if x == loc]
                            indicesp2 = [i for i, x in enumerate(p2_tiles) if x == loc]
                            if len(indicesp1) + len(indicesp2) > 0:
                                if len(indicesp1) > 0:
                                    for i in range(len(indicesp1)):
                                        if z_p1_tiles[indicesp1[i]] == 1:
                                            z_p1_tiles[indicesp1[i]] = -1
                                        else:
                                            z_p1_tiles[indicesp1[i]] -= 1

                                if len(indicesp2) > 0:
                                    for i in range(len(indicesp2)):
                                        if z_p2_tiles[indicesp2[i]] == 1:
                                            z_p2_tiles[indicesp2[i]] = -1
                                        else:
                                            z_p2_tiles[indicesp2[i]] -= 1

                            else:
                                z_p2_tiles[b] = 0

                        # If moving onto empty space
                        else:
                            z_p2_tiles[b] = 0
##                        # Update to new location
##                        for c in range(len(current_tile_mat)):
##                            if current_tile_mat[c] == p2_tiles[b] and z_p2_tiles[b] >= 0:
##                                current_tile_mat[c][0] = loc[0]
##                                current_tile_mat[c][1] = loc[1]         
                    
                    p2_tiles[b][0] = loc[0]
                    p2_tiles[b][1] = loc[1]

        elif game % 2 == 1:

            for b in range(len(p1_tiles)):
                if p1_tiles[b] == tile and p1_insect_mat[b] == insect and z_p1_tiles[b] >= 0:

                    # If Beetle going on top of another tile change the z axis
                    if insect == 'Beetle':

                        # If Currently on a tile
                        if z_p1_tiles[b] == 1:
                            # Find Everything it's sitting on top of
                            filled_indicesp1 = [i for i, x in enumerate(p1_tiles) if x == p1_tiles[b]]
                            filled_indicesp2 = [i for i, x in enumerate(p2_tiles) if x == p1_tiles[b]]
                            
                            # Re-adjust everything underneath
                            if len(filled_indicesp1) > 0:
                                for i in range(len(filled_indicesp1)):
                                    # If not the original_tile cause it's on top
                                    if z_p1_tiles[filled_indicesp1[i]] != 1:
                                        # Determine if it's a stack of 3 or more
                                        if len(filled_indicesp1) + len(filled_indicesp2) >= 3:
                                            # Promote the Highest Beetle to be on top
                                            if z_p1_tiles[filled_indicesp1[i]] == -1:
                                                z_p1_tiles[filled_indicesp1[i]] = 1
                                            else:
                                                z_p1_tiles[filled_indicesp1[i]] += 1
                                        # Not a stack of beetles
                                        else:
                                            if z_p1_tiles[filled_indicesp1[i]] == -1:
                                                z_p1_tiles[filled_indicesp1[i]] = 0
                                        

                            # Re-adjust everything underneath
                            if len(filled_indicesp2) > 0:
                                for i in range(len(filled_indicesp2)):
                                    # If not the original_tile cause it's on top
                                    if z_p2_tiles[filled_indicesp2[i]] != 1:
                                        # Determine if it's a stack of 3 or more
                                        if len(filled_indicesp1) + len(filled_indicesp2) >= 3:
                                            # Promote the Highest Beetle to be on top
                                            if z_p2_tiles[filled_indicesp2[i]] == -1:
                                                z_p2_tiles[filled_indicesp2[i]] = 1
                                            else:
                                                z_p2_tiles[filled_indicesp2[i]] += 1
                                        # Not a stack of beetles
                                        else:
                                            if z_p2_tiles[filled_indicesp2[i]] == -1:
                                                z_p2_tiles[filled_indicesp2[i]] = 0

                        # If moving onto something
                        if loc in p1_tiles or loc in p2_tiles:
                            
                            z_p1_tiles[b] = 1
                            indicesp1 = [i for i, x in enumerate(p1_tiles) if x == loc]
                            indicesp2 = [i for i, x in enumerate(p2_tiles) if x == loc]
                            if len(indicesp1) + len(indicesp2) > 0:
                                if len(indicesp1) > 0:
                                    for i in range(len(indicesp1)):
                                        if z_p1_tiles[indicesp1[i]] == 1:
                                            z_p1_tiles[indicesp1[i]] = -1
                                        else:
                                            z_p1_tiles[indicesp1[i]] -= 1

                                if len(indicesp2) > 0:
                                    for i in range(len(indicesp2)):
                                        if z_p2_tiles[indicesp2[i]] == 1:
                                            z_p2_tiles[indicesp2[i]] = -1
                                        else:
                                            z_p2_tiles[indicesp2[i]] -= 1

                            else:
                                z_p1_tiles[b] = 0

                        # If moving onto empty space
                        else:
                            z_p1_tiles[b] = 0                      

                    
##                        # Update to new location
##                        for a in range(len(current_tile_mat)):
##                            if current_tile_mat[a] == p1_tiles[b]:
##                                current_tile_mat[a][0] = loc[0]
##                                current_tile_mat[a][1] = loc[1]

                    p1_tiles[b][0] = loc[0]
                    p1_tiles[b][1] = loc[1]


##            if p1_insect_mat[pick_a_tile] == 'Grasshopper' or p2_insect_mat[pick_a_tile] == 'Grasshopper':
##                time.sleep(2)
        redraw_tiles(p1_tiles, p1_insect_mat, p2_tiles, p2_insect_mat, z_p1_tiles, z_p2_tiles)

        current_tile_mat = p1_tiles + p2_tiles

    return p1_tiles, p2_tiles, p1_insect_mat, p2_insect_mat, z_p1_tiles, z_p2_tiles, current_tile_mat, current_bug_mat

# Main Loop
def main():

    # Blank matrix for all the current tiles
    current_tile_mat = []
    current_bug_mat = []
    p1_tiles = []
    p2_tiles = []
    z_p1_tiles = []
    z_p2_tiles = []
    p1_insect_mat = []
    p2_insect_mat = []

    # Get the starting position's tile and put it in the matrix
    main_turtle.goto(0,0)
##    current_pos_x = main_turtle.xcor()
##    current_pos_y = main_turtle.ycor()
    turtle.tracer(False)
##    # Draw Starting Tile
##    hexagon_shape(current_pos_x, current_pos_y)
##    
##
##    # Assign the tile
##    random_num = random.randint(1,5)
##    insect = assign_tile(random_num, -1)
##    turtle.tracer(True)
##    
##    
##    
##    current_tile_mat.append([round(current_pos_x, 3), round(current_pos_y, 3)])
##    current_bug_mat.append(insect)
##    p1_tiles.append([round(current_pos_x, 3), round(current_pos_y, 3)])
##    p1_insect_mat.append(insect)
##    z_p1_tiles.append(0)
    

    #print(main_turtle.xcor())
    #print(main_turtle.ycor())

    
    
    

        ##main_turtle.goto(current_pos_x, current_pos_y)

    for game in range(50):
        #print(game)

        ava_pos, final_pos, place_move_mat, place_move_insect, original_position_mat = available_moves(game, current_tile_mat, current_bug_mat, p1_tiles, p2_tiles, z_p1_tiles, z_p2_tiles, p1_insect_mat, p2_insect_mat)

                                                                    
##                if len(ava_pos) >= 1:
##                    can_go = 1
##                    break
##
##                else:
##                    can_go = 0
##                    continue

####################################### Selection Calculations #############################################################################

        #print(ava_pos)
        
        # Select one of avaliable locations
        if game == 0 or game == 1:
            final_pos = ava_pos
        else:
            for m in range(len(ava_pos)):
                if ava_pos[m] not in current_tile_mat and game != 0 or \
                   (place_move_mat[m] == 1 and place_move_insect[m] == 'Beetle'):
                    final_pos.append(ava_pos[m])

        if len(ava_pos) != len(final_pos):
            print('Different Moves')
            print(len(ava_pos))
            print(len(final_pos))

        if len(final_pos) == 0:
            print('No Moves Avaliable')
            continue

        for i in range(len(place_move_insect)):
            if place_move_insect[i] == 'Grasshopper' and place_move_mat[i] == 1 and (ava_pos[i] in p1_tiles or ava_pos[i] in p2_tiles):
                print('Grasshopper Bug')
                print(ava_pos[i])
                print(current_tile_mat)
                print(current_bug_mat)
                print(p1_tiles)
                print(p2_tiles)
                print(p1_insect_mat)
                print(p2_insect_mat)

                

## Criteria
## Next to Queen
## Block's Piece that can go to Queen
## Moves to Position that can go to Opposing Queen
##

        #print(current_tile_mat)

        #print(place_move_mat)

##        for i in range(len(ava_pos)):
##            if place_move_mat[i] == 1 and place_move_insect[i] == 'Grasshopper':
##                print("Place : " + str(ava_pos[i]) + '  Insect: ' + str(place_move_insect[i]))
    
        points = []


        # Queen in play
        if 'Queen' in p1_insect_mat and 'Queen' in p2_insect_mat:

            index_q_p1 = p1_insect_mat.index('Queen')
            next_to_p1_queen = getlocations(p1_tiles[index_q_p1][0], p1_tiles[index_q_p1][1])
            filled_next_to_p1_queen = filled_loc(p1_tiles[index_q_p1], current_tile_mat)

            index_q_p2 = p2_insect_mat.index('Queen')
            next_to_p2_queen = getlocations(p2_tiles[index_q_p2][0], p2_tiles[index_q_p2][1])
            filled_next_to_p2_queen = filled_loc(p2_tiles[index_q_p2], current_tile_mat)

            connected_p1 = connected_tiles(p1_tiles[index_q_p1], current_tile_mat)
            connected_p2 = connected_tiles(p2_tiles[index_q_p2], current_tile_mat)

        elif 'Queen' not in p1_insect_mat and 'Queen' in p2_insect_mat:

            index_q_p2 = p2_insect_mat.index('Queen')
            next_to_p2_queen = getlocations(p2_tiles[index_q_p2][0], p2_tiles[index_q_p2][1])
            filled_next_to_p2_queen = filled_loc(p2_tiles[index_q_p2], current_tile_mat)
            
            next_to_p1_queen = []
            filled_next_to_p1_queen = []

            connected_p2 = connected_tiles(p2_tiles[index_q_p2], current_tile_mat)
            connected_p1 = True
            

        elif 'Queen' in p1_insect_mat and 'Queen' not in p2_insect_mat:  

            index_q_p1 = p1_insect_mat.index('Queen')
            next_to_p1_queen = getlocations(p1_tiles[index_q_p1][0], p1_tiles[index_q_p1][1])
            filled_next_to_p1_queen = filled_loc(p1_tiles[index_q_p1], current_tile_mat)

            next_to_p2_queen = []
            filled_next_to_p2_queen = []

            
            connected_p1 = connected_tiles(p1_tiles[index_q_p1], current_tile_mat)
            connected_p2 = True

            
        else:
            next_to_p1_queen = []
            filled_next_to_p1_queen = []
            next_to_p2_queen = []
            filled_next_to_p2_queen = []
            connected_p1 = False
            connected_p2 = False
            index_q_p1 = 0
            index_q_p2 = 0
            
        for m in range(len(final_pos)):
            points_ranking = 0
                
            current_tile_mat_copy = current_tile_mat.copy()
            current_tile_mat_copy.append(final_pos[m])

            current_bug_mat_copy = current_bug_mat.copy()
            current_bug_mat_copy.append(place_move_insect[m])
            if game % 2 == 1:
                p1_tiles_copy = p1_tiles.copy()
                p1_tiles_copy.append(final_pos[m])
                z_p1_tiles_copy = z_p1_tiles.copy()
                z_p1_tiles_copy.append(0)
                p1_insect_mat_copy = p1_insect_mat.copy()
                p1_insect_mat_copy.append(place_move_insect[m])
                p2_tiles_copy = p2_tiles.copy()
                z_p2_tiles_copy = z_p2_tiles.copy()
                p2_insect_mat_copy = p2_insect_mat.copy()
            elif game % 2 == 0:
                p2_tiles_copy = p2_tiles.copy()
                p2_tiles_copy.append(final_pos[m])
                z_p2_tiles_copy = z_p2_tiles.copy()
                z_p2_tiles_copy.append(0)
                p2_insect_mat_copy = p2_insect_mat.copy()
                p2_insect_mat_copy.append(place_move_insect[m])
                p1_tiles_copy = p1_tiles.copy()
                z_p1_tiles_copy = z_p1_tiles.copy()
                p1_insect_mat_copy = p1_insect_mat.copy()

            if place_move_mat[m] == 0 and len(ava_pos) <= 100:
                ava_pos_new, final_pos_new, place_move_mat_new, place_move_insect_new, original_position_mat_new = available_moves(game, current_tile_mat_copy, current_bug_mat, p1_tiles, p2_tiles, z_p1_tiles, z_p2_tiles, p1_insect_mat, p2_insect_mat)

##                if game % 2 == 0 and game <= 8 and 'Queen' not in p2_insect_mat:
##                    print('Testing Length of Moves')
##                    print(len(ava_pos_new))
##                    print(len(ava_pos))
            
                # 4 Extra Positions
                if len(ava_pos_new) - len(ava_pos) >= 4:
                    points_ranking += 5

                # No Real Change
                if len(ava_pos_new) - len(ava_pos) < 5 and len(ava_pos_new) - len(ava_pos) > -5:
                    points_ranking +=0

                # Removing heaps of moves
                if len(ava_pos_new) - len(ava_pos) < -5:
                    points_ranking += -10
            
            ######################## Player 1 #############################
            # Player 1
            if game % 2 == 1 and game != 1:
                points_ranking = scoring(points_ranking, place_move_mat[m], place_move_insect[m], ava_pos[m], original_position_mat[m], \
                                          next_to_p1_queen, next_to_p2_queen, p1_tiles, p2_tiles, p1_insect_mat, p2_insect_mat, index_q_p2, \
                                          filled_next_to_p1_queen, filled_next_to_p2_queen, connected_p1, \
                                          connected_p2, current_tile_mat, current_tile_mat_copy, game)
                            
            ######################## Player 2 #############################
            # Player 2

            if game % 2 == 0 and game != 0:
                points_ranking = scoring(points_ranking, place_move_mat[m], place_move_insect[m], ava_pos[m], original_position_mat[m], \
                                          next_to_p2_queen, next_to_p1_queen, p2_tiles, p1_tiles, p2_insect_mat, p1_insect_mat, index_q_p1, \
                                          filled_next_to_p2_queen, filled_next_to_p1_queen, connected_p2, \
                                          connected_p1, current_tile_mat, current_tile_mat_copy, game)
                    
            
            points.append(points_ranking)
            current_tile_mat_copy.pop(-1)
            current_bug_mat_copy.pop(-1)
            if game % 2 == 1:
                p1_tiles_copy.pop(-1)
                z_p1_tiles_copy.pop(-1)
                p1_insect_mat_copy.pop(-1)

            if game % 2 == 0:
                p2_tiles_copy.pop(-1)
                z_p2_tiles_copy.pop(-1)
                p2_insect_mat_copy.pop(-1)

        ################# SELECTION ##################

        # Player 1 is the Best AI
        if game % 2 == 1:
            max_tile = max(points)

            index = [i for i, x in enumerate(points) if x == max_tile]

            random_highest = random.randint(0,len(index)-1)

            ran_loc = index[random_highest]

        # Player 2 is completely random
        if game % 2 == 0:
            min_tile = min(points)

            index = [i for i, x in enumerate(points) if x == min_tile]

            random_lowest = random.randint(0,len(index)-1)
            ran_loc = index[random_lowest]
        
        insect = place_move_insect[ran_loc]
        tile = original_position_mat[ran_loc]
        loc = final_pos[ran_loc]
        placement = place_move_mat[ran_loc]
        
        print(game)
##        print(points[ran_loc])
##        print(ran_loc)
##        print(placement)


        if game == 14:
            print('Current')
            print(current_tile_mat)
            print('Ava_Pos')
            print(ava_pos)
            print('Points')
            print(points)
            print('Place_move_mat')
            print(place_move_mat)
            print('Place_move_insect')
            print(place_move_insect)
            print('Original_position_mat')
            print(original_position_mat)
            print('Ran Loc')
            print(ran_loc)
            print('Point Value')
            print(points[ran_loc])
            print('End')
            
        if len(ava_pos) == 0:
            print(ava_pos)
            print(game)
            print(place_move_mat)
            print(place_move_insect)
            print(original_position_mat)
            print(p1_tiles)
            print(p2_tiles)
            print(p1_insect_mat)
            print(p2_insect_mat)
            print(z_p1_tiles)
            print(z_p2_tiles)
            print(points)

###################################### Placement #######################

        p1_tiles, p2_tiles, p1_insect_mat, \
                  p2_insect_mat, z_p1_tiles, \
                  z_p2_tiles, current_tile_mat, \
                  current_bug_mat = board_updates(game, placement, tile, loc, insect, p1_tiles, p2_tiles, \
                                                               p1_insect_mat, p2_insect_mat, z_p1_tiles, z_p2_tiles, current_tile_mat, current_bug_mat)


##        if place_move_rand == 1 and game == 7:
##            print(game)
##            print(final_pos[ran_loc])   



            #print(game)
            #time.sleep(0.25)

        ############### END GAME #############

        # Queen in play
        if 'Queen' in p1_insect_mat and 'Queen' in p2_insect_mat:

            index_q_p1 = p1_insect_mat.index('Queen')
            index_q_p2 = p2_insect_mat.index('Queen')

            open_slot_p1 = filled_loc(p1_tiles[index_q_p1], current_tile_mat)
            open_slot_p2 = filled_loc(p2_tiles[index_q_p2], current_tile_mat)

            if len(open_slot_p1) == 6 and len(open_slot_2) != 6:
                print('Player 2 Wins')
                print('Player 1''s Queen is surrounded')
                
                break

            if len(open_slot_p1) == 5 or len(open_slot_p2) == 5:
                print('About to Win')
                print(current_tile_mat)
                print('Ava_Pos')
                print(ava_pos)
                print('Points')
                print(points)
                print('Place_move_mat')
                print(place_move_mat)
                print('Place_move_insect')
                print(place_move_insect)
                print('Original_position_mat')
                print(original_position_mat)
                print('Ran Loc')
                print(ran_loc)
                print('Point Value')
                print(points[ran_loc])
                print('End')
                

            if len(open_slot_p2) == 6 and len(open_slot_p1) != 6:
                print('Player 1 Wins')
                print('Player 2''s Queen is surrounded')
                print('Player 1 in ' + str(game) + ' moves')
                print(points)
                print(final_pos)
                print(ran_loc)
                print(place_move_mat)
                print(original_position_mat)
                print(place_move_insect)
                print(current_tile_mat)
                print(current_bug_mat)
                break

            if len(open_slot_p2) == 6 and len(open_slot_p1) == 6:
                print('It'' a tie')
                print('Both Queen''s are surrounded')
                print(points)
                print(final_pos)
                print(ran_loc)
                print(place_move_mat)
                print(original_position_mat)
                print(place_move_insect)
                break

            #Player 1's Turn
    print('Final Stats')
    print('Game')
    print(game)
    print('Tiles')
    print(p1_tiles)
    print(p2_tiles)
    print(p1_insect_mat)
    print(p2_insect_mat)
    print(current_bug_mat)
    print(current_tile_mat)
    print(z_p1_tiles)
    print(z_p2_tiles)
    print('Last Select Move')
    print(ran_loc)
    print('Current')
    print(current_tile_mat)
    print('Ava_Pos')
    print(ava_pos)
    print('Points')
    print(points)
    print('Place_move_mat')
    print(place_move_mat)
    print('Place_move_insect')
    print(place_move_insect)
    print('Original_position_mat')
    print(original_position_mat)
    print('End')            

##            
##    print(p1_tiles)
##    print(p2_tiles)
##    print(p1_insect_mat)
##    print(p2_insect_mat)
####    print(current_bug_mat)
##    print(current_tile_mat)
##    print(z_p1_tiles)
##    print(z_p2_tiles)
##    
    ### Select location
    ##find_location = random.randint(1,6)
    ##print(positions[1])
    
    
    # Add the


    ##for i in range(10):
     # Select the location
        
##    random_loc = random.randint(0,5)
##    main_turtle.goto(positions[random_num])
##    main_turtle.tilt([0])
### Select the title
##    random_num = random.randint(1,5)
##    assign_tile(random_num)
##random.randint(1,6)

##assign_tile()
##
##main_turtle.goto(current_pos_x, current_pos_y)
##main_turtle.setheading(0)
##main_turtle.up()
##main_turtle.left(150)
##main_turtle.forward(side_length * 2)
##main_turtle.right(150)
##main_turtle.setheading(0)
##main_turtle.down()
##
##hexagon_shape()
##assign_tile()
##
##main_turtle.goto(current_pos_x, current_pos_y)
##main_turtle.setheading(0)
##main_turtle.up()
##main_turtle.left(angle + 30)
##main_turtle.forward(side_length * 2)
##main_turtle.right(angle + 30)
##main_turtle.setheading(0)
##main_turtle.down()
##
##hexagon_shape()
##assign_tile()
##
##main_turtle.goto(current_pos_x, current_pos_y)
##main_turtle.setheading(0)
##main_turtle.up()
##main_turtle.left(30)
##main_turtle.forward(side_length * 2)
##main_turtle.right(30)
##main_turtle.setheading(0)
##main_turtle.down()
##
##hexagon_shape()
##assign_tile()
##
##main_turtle.goto(current_pos_x, current_pos_y)
##main_turtle.setheading(0)
##main_turtle.up()
##main_turtle.left(-30)
##main_turtle.forward(side_length * 2)
##main_turtle.right(-30)
##main_turtle.setheading(0)
##main_turtle.down()
##
##hexagon_shape()
##assign_tile()
##
##main_turtle.goto(current_pos_x, current_pos_y)
##main_turtle.setheading(0)
##main_turtle.up()
##main_turtle.left(-90)
##main_turtle.forward(side_length * 2)
##main_turtle.right(-90)
##main_turtle.setheading(0)
##main_turtle.down()
##
##hexagon_shape()
##assign_tile()
##
##main_turtle.goto(current_pos_x, current_pos_y)
##main_turtle.setheading(0)
##main_turtle.up()
##main_turtle.left(-150)
##main_turtle.forward(side_length * 2)
##main_turtle.right(-150)
##main_turtle.setheading(0)
##main_turtle.down()
##
##hexagon_shape()
##assign_tile()
##
### Find next location
##random_num_2 = random.randint(1,6)
##if random_num == 1:
##    main_turtle.up()
##    main_turtle.left(angle)
##    main_turtle.forward(side_length * 2)
##    main_turtle.right(angle)
##    main_turtle.down()
##elif random_num == 2:
##    beetle_drawing()
##elif random_num == 3:
##    spider_drawing()
##elif random_num == 4:
##    ant_drawing()
##elif random_num == 5:
##    grasshopper_drawing()
##elif random_num == 6:
    
## Add Intellegence
## Get All the moves
## Find the "Best Move" Based on Criteria
## 



#print(main_turtle.position())
main()



print('Waiting')
wn.exitonclick()

#hexagon_shape()
