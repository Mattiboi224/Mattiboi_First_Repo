import turtle
import Config as C
import math
from collections import deque
import random


# Draw a hexagon
def hexagon_shape(position_x, position_y, sel_turtle):

    if sel_turtle == 'Main':
        turtle.tracer(False)
        # Start Location to Start of Hexagon
        C.main_turtle.color('black')
        C.main_turtle.goto(position_x, position_y)
        C.main_turtle.right(C.main_turtle.heading())
        C.main_turtle.up()
        C.main_turtle.left(C.angle * 2)
        C.main_turtle.forward(C.side_length)
        #main_turtle.right(angle * 2)
        C.main_turtle.right(C.main_turtle.heading())
        C.main_turtle.down()

        # Draw Hexagon
        for i in range(C.num_sides):
            C.main_turtle.forward(C.side_length)
            C.main_turtle.right(C.angle)

        # Back to Start Location
        C.main_turtle.up()
        C.main_turtle.right(C.angle)
        C.main_turtle.forward(C.side_length)
        C.main_turtle.left(C.angle)

        C.main_turtle.goto(position_x, position_y)
        C.main_turtle.right(C.main_turtle.heading())
        turtle.tracer(True)

    if sel_turtle == 'Board':
        turtle.tracer(False)
        # Start Location to Start of Hexagon
        C.board_turtle.color('black')
        C.board_turtle.goto(position_x, position_y)
        C.board_turtle.right(C.board_turtle.heading())
        C.board_turtle.up()
        C.board_turtle.left(C.angle * 2)
        C.board_turtle.forward(C.side_length)
        #main_turtle.right(angle * 2)
        C.board_turtle.right(C.board_turtle.heading())
        C.board_turtle.down()

        # Draw Hexagon
        for i in range(C.num_sides):
            C.board_turtle.forward(C.side_length)
            C.board_turtle.right(C.angle)

        # Back to Start Location
        C.board_turtle.up()
        C.board_turtle.right(C.angle)
        C.board_turtle.forward(C.side_length)
        C.board_turtle.left(C.angle)

        C.board_turtle.goto(position_x, position_y)
        C.board_turtle.right(C.board_turtle.heading())
        turtle.tracer(True)

# Draw a rectangle
def draw_rectangle(x, y, w, h, sel_turtle):

    if sel_turtle == 'Main':
    
        turtle.tracer(False)
        C.main_turtle.up()
        C.main_turtle.goto(x, y)
        C.main_turtle.right(C.main_turtle.heading())
        C.main_turtle.down()
        for _ in range(2):
            C.main_turtle.forward(w)
            C.main_turtle.left(90)
            C.main_turtle.forward(h)
            C.main_turtle.left(90)
        C.main_turtle.up()
        turtle.tracer(True)

    elif sel_turtle == 'Selection':
    
        turtle.tracer(False)
        C.selection_turtle.up()
        C.selection_turtle.goto(x, y)
        C.selection_turtle.right(C.selection_turtle.heading())
        C.selection_turtle.down()
        for _ in range(2):
            C.selection_turtle.forward(w)
            C.selection_turtle.left(90)
            C.selection_turtle.forward(h)
            C.selection_turtle.left(90)
        C.selection_turtle.up()
        turtle.tracer(True)

    elif sel_turtle == 'Move_Place':
    
        turtle.tracer(False)
        C.move_place_turtle.up()
        C.move_place_turtle.goto(x, y)
        C.move_place_turtle.right(C.move_place_turtle.heading())
        C.move_place_turtle.down()
        for _ in range(2):
            C.move_place_turtle.forward(w)
            C.move_place_turtle.left(90)
            C.move_place_turtle.forward(h)
            C.move_place_turtle.left(90)
        C.move_place_turtle.up()
        turtle.tracer(True)

    elif sel_turtle == 'Board':
    
        turtle.tracer(False)
        C.board_turtle.up()
        C.board_turtle.goto(x, y)
        C.board_turtle.right(C.board_turtle.heading())
        C.board_turtle.down()
        for _ in range(2):
            C.board_turtle.forward(w)
            C.board_turtle.left(90)
            C.board_turtle.forward(h)
            C.board_turtle.left(90)
        C.board_turtle.up()
        turtle.tracer(True)

def getlocations(posx, posy):
    avaliable_position = []
    
    for i in range(6):
        turtle.tracer(False)
        C.main_turtle.goto(posx, posy)
        C.main_turtle.setheading(0)
        C.main_turtle.up()
        C.main_turtle.left(150 - 60 * i)
        C.main_turtle.forward(C.side_length * math.sqrt(3))
        C.main_turtle.right(150)
        C.main_turtle.setheading(0)
        xpos = C.main_turtle.xcor()
        ypos = C.main_turtle.ycor()
        avaliable_position.append([round(xpos,3), round(ypos,3)])
        turtle.tracer(True)
    
    return avaliable_position

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

    surround_loc = getlocations(location[0],location[1])
    filled_mat = []
    for i in range(len(surround_loc)):
        if surround_loc[i] in current_tile_mat:
            filled_mat.append(surround_loc[i])

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

def dist(a, b):
    return math.hypot(a[0]-b[0], a[1]-b[1])


def select_move_type(x, y):
        
    if x >= 400 and x <= 450 and y >= 25 and y <= 125 and C.place_trigger == 1:
        C.move_type = 'Place'
        C.picking_pos = True

    elif x >= 400 and x <= 450 and y >= -125 and y <= -25 and C.move_trigger == 1:
        C.move_type = 'Move'
        C.picking_pos = True
    
    else:
        print('Invalid Click')
        C.picking_pos = False


    # Select a tile
def select_tile(x, y):

    C.move_type = None

    if x >= -550 and x <= -500 and y >= -350 and y <= -250:
        C.move_type = 'Beetle'
        C.picking_pos = True

    elif x >= -550 and x <= -500 and y >= -200 and y <= -100:
        C.move_type = 'Spider'
        C.picking_pos = True

    elif x >= -550 and x <= -500 and y >= -50 and y <= 50:
        C.move_type = 'Grasshopper'
        C.picking_pos = True

    elif x >= -550 and x <= -500 and y >= 100 and y <= 200:
        C.move_type = 'Ant'
        C.picking_pos = True

    elif x >= -550 and x <= -500 and y >= 250 and y <= 350:
        C.move_type = 'Queen'
        C.picking_pos = True

    else:
        print('Invalid Click')
        C.picking_pos = False