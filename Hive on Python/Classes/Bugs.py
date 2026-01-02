

import turtle
import util as m
import Config as C
from collections import deque

class Bugs():


    def __init__(self, bug_type, x, y, z, team):
        self.bug_type = bug_type
        self.original_tile = [x, y]
        self.x = x
        self.y = y
        self.z = z
        self.m_p = None
        self.Tile = None
        self.radius = C.radius

        self.team = team
        self.colour = team.colour

    def pos(self):
        return [self.x, self.y]
    
    def update(self, new_tile):
        self.x = new_tile[0]
        self.y = new_tile[1]
        self.original_tile = new_tile

    def draw(self):

        turtle.tracer(False)

        C.main_turtle.color(self.colour)
        C.main_turtle.goto(self.x, self.y - 20)

        #Draw Bugs
        if self.bug_type == 'Queen':
            #C.main_turtle.right(90)
            #C.main_turtle.forward(20)
            C.main_turtle.write("Q", False, align="center", font=("Arial", 30, "normal"))

            '''
            current_pos_x = C.main_turtle.xcor() 
            current_pos_y = C.main_turtle.ycor() + 20
            #Body
            C.main_turtle.up()
            C.main_turtle.left(90)
            C.main_turtle.forward(20)
            C.main_turtle.dot(20, "blue")
            C.main_turtle.right(180)
            C.main_turtle.forward(25)
            C.main_turtle.dot(40,"blue")

            #Front Legs
            C.main_turtle.goto(current_pos_x, current_pos_y)
            C.main_turtle.setheading(90)
            #C.main_turtle.forward(9)
            C.main_turtle.down()
            C.main_turtle.pencolor("blue")
            C.main_turtle.circle(20, 100)
            C.main_turtle.up()
            C.main_turtle.goto(current_pos_x, current_pos_y)
            C.main_turtle.setheading(-90)
            C.main_turtle.down()
            C.main_turtle.circle(20, -100)
            C.main_turtle.up()
            #Antenna
            C.main_turtle.goto(current_pos_x - 1, current_pos_y)
            C.main_turtle.setheading(90)
            C.main_turtle.down()
            C.main_turtle.circle(100, 12)
            C.main_turtle.setheading(180)
            C.main_turtle.forward(5)
            C.main_turtle.up()
            C.main_turtle.goto(current_pos_x + 1, current_pos_y)
            C.main_turtle.setheading(-90)
            C.main_turtle.down()
            C.main_turtle.circle(100, -12)
            C.main_turtle.setheading(0)
            C.main_turtle.forward(5)
            C.main_turtle.up()
            C.main_turtle.goto(current_pos_x, current_pos_y)
            '''

        elif self.bug_type == 'Grasshopper':
            #C.main_turtle.right(90)
            #C.main_turtle.forward(20)
            C.main_turtle.write("G", False, align="center", font=("Arial", 30, "normal"))

        elif self.bug_type == 'Beetle':
            #C.main_turtle.right(90)
            #C.main_turtle.forward(20)
            C.main_turtle.write("B", False, align="center", font=("Arial", 30, "normal"))

        elif self.bug_type == 'Ant':
            #C.main_turtle.right(90)
            #C.main_turtle.forward(20)
            C.main_turtle.write("A", False, align="center", font=("Arial", 30, "normal"))

        elif self.bug_type == 'Spider':
            #C.main_turtle.right(90)
            #C.main_turtle.forward(20)
            C.main_turtle.write("S", False, align="center", font=("Arial", 30, "normal"))

        turtle.tracer(True)

    def avaliable_move(self, current_tile_mat):

        # Check for slideable
        open_loc = m.slideable_locs(self.original_tile, current_tile_mat)

        if len(open_loc) == 0 and self.bug_type in ('Queen', 'Ant', 'Spider'):
            final_loc = []
            return final_loc

        # Check if not breaking the hive
        connected = m.connected_tiles(self.original_tile, current_tile_mat)
        if not connected:
            final_loc = []
            return final_loc
        
    
        if self.bug_type == 'Queen':
            #def queen_logic(original_tile, current_tile_mat):

            position = m.getlocations(self.original_tile[0], self.original_tile[1])

            open_loc = m.slideable_locs(position, current_tile_mat)

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
                in_mat = m.getlocations(open_loc[p][0], open_loc[p][1])

                if self.original_tile in in_mat:
                    in_mat.remove(self.original_tile)

                #Check to see if it's next to an existing tile
                for q in range(len(in_mat)):
                    if in_mat[q] in current_tile_mat and open_loc[p] not in final_pos:
                        if open_loc[p] in final_pos:
                            continue
                        final_pos.append(open_loc[p])

            return final_pos
        
        if self.bug_type == 'Spider':

            tile = (self.original_tile[0], self.original_tile[1])
            
            position = m.getlocations(tile[0], tile[1])
            slideable_mat = m.slideable_locs(position, current_tile_mat)
            next_to_something = []
            final_position = []

            #while slideable_mat:
            for i in range(3):
                new_slideables = []

                for x, y in slideable_mat:
                    check_locs = m.getlocations(x, y)

                    if any(loc in current_tile_mat and loc != tile for loc in check_locs):
                        if [x, y] not in next_to_something:
                            next_to_something.append([x, y])
                            new_slideables.extend(m.slideable_locs(m.getlocations(x, y), current_tile_mat))
                            if i == 2:
                                final_position.append([x,y])

                slideable_mat = new_slideables

            return final_position
        

        elif self.bug_type == 'Grasshopper':

            # Get everything that is around
            position = m.getlocations(self.original_tile[0], self.original_tile[1])
            original_tile_tup = tuple(self.original_tile)
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
                
                neighbors = m.getlocations(current[0], current[1])
                neighbors = [tuple(inner_list) for inner_list in neighbors]

                for i in range(len(filled_local)):     
                    for neighbor in neighbors:
                        if neighbor not in visited and m.is_on_line(original_tile_tup[0], original_tile_tup[1], filled_local[i][0], filled_local[i][1], neighbor[0], neighbor[1]) and neighbor != original_tile_tup:
                            if neighbor in current_tile_mat_tup:
                                queue.append(neighbor)
                            else:
                                if neighbor in position and neighbor not in filled_local:
                                    continue
                                if neighbor not in final_loc:
                                    final_loc.append(neighbor)

            return final_loc

        elif self.bug_type == 'Beetle':

            final_loc = []
            # Get Everything around the Beetle
            position = m.getlocations(self.original_tile[0], self.original_tile[1])

            # For every position make sure it's next to something
            for i in range(len(position)):
                local_pos = m.getlocations(position[i][0], position[i][1])
                
                for j in range(len(local_pos)):
                    
                    # Ignore Original Tile
                    if local_pos[j] in current_tile_mat and local_pos[j] != self.original_tile:
                        final_loc.append(position[i])

            return final_loc

        elif self.bug_type == 'Ant':
            final_loc = []
            # Get every location on the edge of the board
            position = m.get_all_locations(current_tile_mat, self.original_tile)
            position_tup = [tuple(inner_list) for inner_list in position]
            
            for j in range(len(position)):
                check_locs = m.getlocations(position[j][0], position[j][1])
                #print('Check Locs: ')
                #print(check_locs)
                # Check if can slide into the location
                slideable_get_locs = m.slideable_locs(check_locs, current_tile_mat)
                #print(slideable_get_locs)

                # If you can't slide into position
                if len(slideable_get_locs) == 0:
                    continue

                avaliable_pos = tuple(position[j])
                
                # For the slidable position are they linked to the main position
                if m.is_connected(avaliable_pos, (self.original_tile[0], self.original_tile[1]), position_tup, (self.original_tile[0], self.original_tile[1])):
                        final_loc.append(position[j])    

            return final_loc
        

    def get_tile(self, Tile_Mat):

        for i in Tile_Mat:

            if i.x == self.x and i.y == self.y:

                self.Tile = i