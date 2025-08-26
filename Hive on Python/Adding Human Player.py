import turtle
import math
from collections import deque

# Initialize the screen and main turtle
wn = turtle.Screen()
main_turtle = turtle.Turtle()
main_turtle.hideturtle()
board_turtle = turtle.Turtle()
board_turtle.hideturtle()
move_place_turtle = turtle.Turtle()
move_place_turtle.hideturtle()
selection_turtle = turtle.Turtle()
selection_turtle.hideturtle()

# Putting Everything Up
main_turtle.up()
board_turtle.up()
move_place_turtle.up()
selection_turtle.up()

# Constants
total_ant = 3
total_grasshopper = 3
total_beetle = 2
total_spider = 2
total_queen = 1
side_length = 40
num_sides = 6
angle = 360.0 / num_sides

# Draw a hexagon
def hexagon_shape(position_x, position_y, sel_turtle):

    if sel_turtle == 'Main':
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

    if sel_turtle == 'Board':
        turtle.tracer(False)
        # Start Location to Start of Hexagon
        board_turtle.color('black')
        board_turtle.goto(position_x, position_y)
        board_turtle.right(board_turtle.heading())
        board_turtle.up()
        board_turtle.left(angle * 2)
        board_turtle.forward(side_length)
        #main_turtle.right(angle * 2)
        board_turtle.right(board_turtle.heading())
        board_turtle.down()

        # Draw Hexagon
        for i in range(num_sides):
            board_turtle.forward(side_length)
            board_turtle.right(angle)

        # Back to Start Location
        board_turtle.up()
        board_turtle.right(angle)
        board_turtle.forward(side_length)
        board_turtle.left(angle)

        board_turtle.goto(position_x, position_y)
        board_turtle.right(board_turtle.heading())
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
        
        hexagon_shape(p1_tiles_copy[i][0],p1_tiles_copy[i][1], 'Main')

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

        hexagon_shape(p2_tiles_copy[i][0],p2_tiles_copy[i][1], 'Main')

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

# Get surrounding hexagon locations
def getlocations(posx, posy):
    available_positions = []
    
    for i in range(6):
        turtle.tracer(False)
        main_turtle.goto(posx, posy)
        main_turtle.setheading(0)
        main_turtle.up()
        main_turtle.left(150 - 60 * i)
        main_turtle.forward(side_length * math.sqrt(3))
        main_turtle.right(150)
        xpos = main_turtle.xcor()
        ypos = main_turtle.ycor()
        available_positions.append([round(xpos, 3), round(ypos, 3)])
        turtle.tracer(True)
    
    return available_positions

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

# Build the board
def build_the_board():
    turtle.tracer(False)
    position = getlocations(0, 0)
    position = [tuple(inner_list) for inner_list in position]
    
    visited = set()
    queue = deque([(0, 0)] + position)
    
    final_loc = []
    
    while queue:
        current = queue.popleft()
        
        if current in visited:
            continue
        
        hexagon_shape(current[0], current[1], 'Board')
        final_loc.append([current[0], current[1]])
        
        visited.add(current)
        
        neighbors = getlocations(current[0], current[1])
        neighbors = [tuple(inner_list) for inner_list in neighbors]
        
        for neighbor in neighbors:
            if neighbor not in visited:
                queue.append(neighbor)
        
        if len(final_loc) == 91:
            break
    
    turtle.tracer(True)
    return final_loc

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

# Place a tile
def place_tile(x, y):
    global close_position, picking_pos
    
    pos_points = []
    for loc in all_locs:
        dist = math.sqrt((x - loc[0])**2 + (y - loc[1])**2)
        pos_points.append(dist)
    
    min_pos_points = min(pos_points)
    index = pos_points.index(min_pos_points)
    
    close_position = all_locs[index]
    picking_pos = True

# Draw a rectangle
def draw_rectangle(x, y, w, h, sel_turtle):

    if sel_turtle == 'Main':
    
        turtle.tracer(False)
        main_turtle.up()
        main_turtle.goto(x, y)
        main_turtle.right(main_turtle.heading())
        main_turtle.down()
        for _ in range(2):
            main_turtle.forward(w)
            main_turtle.left(90)
            main_turtle.forward(h)
            main_turtle.left(90)
        main_turtle.up()
        turtle.tracer(True)

    elif sel_turtle == 'Selection':
    
        turtle.tracer(False)
        selection_turtle.up()
        selection_turtle.goto(x, y)
        selection_turtle.right(selection_turtle.heading())
        selection_turtle.down()
        for _ in range(2):
            selection_turtle.forward(w)
            selection_turtle.left(90)
            selection_turtle.forward(h)
            selection_turtle.left(90)
        selection_turtle.up()
        turtle.tracer(True)

    elif sel_turtle == 'Move_Place':
    
        turtle.tracer(False)
        move_place_turtle.up()
        move_place_turtle.goto(x, y)
        move_place_turtle.right(move_place_turtle.heading())
        move_place_turtle.down()
        for _ in range(2):
            move_place_turtle.forward(w)
            move_place_turtle.left(90)
            move_place_turtle.forward(h)
            move_place_turtle.left(90)
        move_place_turtle.up()
        turtle.tracer(True)

# Select a tile
def select_tile(x, y):
    global picking_pos, chose_tile

    counter = 0
    
    while counter == 0:

        if x >= -450 and x <= -400 and y >= -350 and y <= -250:
            chose_tile = 'Beetle'
            break

        if x >= -450 and x <= -400 and y >= -200 and y <= -100:
            chose_tile = 'Spider'
            break

        if x >= -450 and x <= -400 and y >= -50 and y <= 50:
            chose_tile = 'Grasshopper'
            break

        if x >= -450 and x <= -400 and y >= 100 and y <= 200:
            chose_tile = 'Ant'
            break

        if x >= -450 and x <= -400 and y >= 250 and y <= 350:
            chose_tile = 'Queen'
            break

    picking_pos = True

def select_move_type(x, y):
    global move_type, picking_pos

    counter = 0
    
    while counter == 0:
        
        if x >= 400 and x <= 450 and y >= 25 and y <= 125:
            move_type = 'Place'
            break

        if x >= 400 and x <= 450 and y >= -125 and y <= -25:
            move_type = 'Move'
            break
    else:
        counter = 0

    picking_pos = True
    
def Human_Player(own_tiles, opp_tiles, own_insect, opp_insect, z_own, z_opp, current_tile_mat):
    # Initialize variables
    global all_locs, picking_pos, close_position, chose_tile, move_type

    picking_pos = False
    close_position = None
    chose_tile = None
    move_type = None
    all_locs = build_the_board()

    draw_rectangle(400, 25, 50, 100, 'Move_Place')
    turtle.tracer(False)
    move_place_turtle.goto(425,75)
    move_place_turtle.right(90)
    move_place_turtle.forward(20)
    move_place_turtle.write("P", False, align="center", font=("Arial", 30, "normal"))
    turtle.tracer(True)

    draw_rectangle(400, -125, 50, 100, 'Move_Place')
    turtle.tracer(False)
    move_place_turtle.goto(425,-75)
    move_place_turtle.right(90)
    move_place_turtle.forward(20)
    move_place_turtle.write("M", False, align="center", font=("Arial", 30, "normal"))
    turtle.tracer(True)

    turtle.onscreenclick(select_move_type)

    while not picking_pos and move_type is None:
        wn.update()

    move_place_turtle.clear()

    print(move_type)


    if move_type == 'Place':
        picking_pos = False

        # Main loop
        turtle.onscreenclick(place_tile)

        while not picking_pos:
            wn.update()

        #print(all_locs)

        selection_turtle.up()
        selection_turtle.goto(close_position[0], close_position[1])
        selection_turtle.dot(10, "Red")

        positions = [250, 100, -50, -200, -350]
        letters = ["Q", "A", "G", "S", "B"]

        for y, letter in zip(positions, letters):
            draw_rectangle(-450, y, 50, 100, 'Selection')
            turtle.tracer(False)
            selection_turtle.goto(-423, y + 50)
            selection_turtle.right(90)
            selection_turtle.forward(20)
            selection_turtle.write(letter, False, align="center", font=("Arial", 30, "normal"))
            turtle.tracer(True)
            
        picking_pos = False

        turtle.onscreenclick(select_tile)

        turtle.tracer(True)

        while not picking_pos and chose_tile is None:
            wn.update()

        selection_turtle.clear()

        if chose_tile == 'Queen':
            main_turtle.goto(close_position[0], close_position[1])
            main_turtle.right(main_turtle.heading())
            queen_drawing()

        elif chose_tile == 'Ant':
            main_turtle.goto(close_position[0], close_position[1])
            main_turtle.right(main_turtle.heading())
            ant_drawing()

        elif chose_tile == 'Grasshopper':
            main_turtle.goto(close_position[0], close_position[1])
            main_turtle.right(main_turtle.heading())
            grasshopper_drawing()

        elif chose_tile == 'Spider':
            main_turtle.goto(close_position[0], close_position[1])
            main_turtle.right(main_turtle.heading())
            spider_drawing()

        elif chose_tile == 'Beetle':
            main_turtle.goto(close_position[0], close_position[1])
            main_turtle.right(main_turtle.heading())
            beetle_drawing()

        print(chose_tile)
        print(close_position)

        orig_position = close_position
        
        return chose_tile, close_position, move_type, orig_position

    elif move_type == 'Move':

        picking_pos = False

        # Pick the Tile you want to move
        turtle.onscreenclick(place_tile)

        while not picking_pos:
            wn.update()

        orig_position = close_position

        # Find the Tile that has been placed
        for i in range(len(own_tiles)):

            if own_tiles[i] == close_position and z_own[i] >= 0:

                # Find the avaliable moves of the piece

                if own_insect[i] == 'Queen':
                    ava_pos = queen_logic(close_position, current_tile_mat)


                elif own_insect[i] == 'Ant':
                    ava_pos = ant_logic(close_position, current_tile_mat)
                    

                elif own_insect[i] == 'Grasshopper':
                    ava_pos = grasshopper_pathway(close_position, current_tile_mat)
                    

                elif own_insect[i] == 'Spider':
                    ava_pos = spider_logic(close_position, current_tile_mat)
                    

                elif own_insect[i] == 'Beetle':
                    ava_pos = beetle_logic(close_position, current_tile_mat)

                for j in range(len(ava_pos)):
                    turtle.tracer(False)
                    selection_turtle.up()
                    selection_turtle.goto(ava_pos[j][0], ava_pos[j][1])
                    selection_turtle.dot(10, 'Blue')
                    turtle.tracer(True)

                picking_pos = False

                # Pick the Tile the position you want to move to
                turtle.onscreenclick(place_tile)

                while not picking_pos:
                    wn.update()

                selection_turtle.clear()

                return own_insect[i], close_position, move_type, orig_position

        

        
p1_tiles = [[0.0, -69.282], [-0.0, -138.564], [-120.0, -0.0], [-0.0, -207.846], [-60.0, -34.641], [-60.0, 103.923], [-0.0, -277.128]]
p2_tiles = [[0.0, 69.282], [-180.0, -34.641], [-60.0, 34.641], [0.0, 69.282], [-0.0, 69.282]]
p1_insect_mat = ['Spider', 'Beetle', 'Ant', 'Queen', 'Beetle', 'Ant', 'Ant']
p2_insect_mat = ['Beetle', 'Grasshopper', 'Queen', 'Spider', 'Beetle']
z_p1_tiles = [0, 0, 0, 0, 0, 0, 0]
z_p2_tiles = [-1, 0, 0, -2, 1]
current_tile_mat = [[0.0, -69.282], [-0.0, -138.564], [-120.0, -0.0], [-0.0, -207.846], [-60.0, -34.641], [-60.0, 103.923], [0.0, 69.282], [-180.0, -34.641], [-60.0, 34.641], [0.0, 69.282], [-0.0, 69.282], [-0.0, -277.128]]        

redraw_tiles(p1_tiles, p1_insect_mat, p2_tiles, p2_insect_mat, z_p1_tiles, z_p2_tiles)

chose_tile, close_position, move_type, orig_position = Human_Player(p1_tiles, p2_tiles, p1_insect_mat, p2_insect_mat, z_p1_tiles, z_p2_tiles, current_tile_mat)

print(chose_tile)
print(close_position)
print(move_type)
print(orig_position)

print('End')

wn.exitonclick()
