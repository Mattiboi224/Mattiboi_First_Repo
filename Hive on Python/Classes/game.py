import Config as C
import util as m
import turtle
import math
import Bugs as B
import random

class Game:
    def __init__(self):
        pass


    # Announce Remaining Insects
    def announce_remaining_insects(color, x_positions, y_positions, insect_types, totals, player_insects):
        C.announcer_turtle.color(color)
        for i, insect in enumerate(insect_types):
            turtle.tracer(False)
            message = player_insects.count(insect)
            message = totals[i] - message
            C.announcer_turtle.goto(x_positions[i], y_positions[i])
            C.announcer_turtle.write(message, False, align="left", font=("Arial", 10, "normal"))
            turtle.tracer(True)

    # Place a tile
    def place_tile(self, x, y):
        global close_position, picking_pos
        
        pos_points = []
        for loc in Board.all_locs:
            dist = math.sqrt((x - loc[0])**2 + (y - loc[1])**2)
            pos_points.append(dist)
        
        min_pos_points = min(pos_points)
        index = pos_points.index(min_pos_points)
        
        close_position = Board.all_locs[index]
        picking_pos = True

    def select_move_type(self, x, y):
        global move_type, picking_pos

        #print('X Cord: ', x)
        #print('Y Cord: ', y)

            
        if x >= 400 and x <= 450 and y >= 25 and y <= 125:
            move_type = 'Place'
            #click_event.set()
            picking_pos = True

        elif x >= 400 and x <= 450 and y >= -125 and y <= -25:
            move_type = 'Move'
            #click_event.set()
            picking_pos = True
        
        else:
            print('Invalid Click')
            picking_pos = False
            #turtle.onclick(None)

        # Select a tile
    def select_tile(self, x, y):
        global picking_pos, chose_tile

        counter = 0
        chose_tile = None

        print(x)
        print(y)
        
        while counter == 0:

            if x >= -550 and x <= -500 and y >= -350 and y <= -250:
                chose_tile = 'Beetle'
                break

            elif x >= -550 and x <= -500 and y >= -200 and y <= -100:
                chose_tile = 'Spider'
                break

            elif x >= -550 and x <= -500 and y >= -50 and y <= 50:
                chose_tile = 'Grasshopper'
                break

            elif x >= -550 and x <= -500 and y >= 100 and y <= 200:
                chose_tile = 'Ant'
                break

            elif x >= -550 and x <= -500 and y >= 250 and y <= 350:
                chose_tile = 'Queen'
                break
        
        picking_pos = True

        # Human Player
    def Human_Player(self, current_tile_mat_class, human):
        # Initialize variables
        global all_locs, picking_pos, close_position, chose_tile, move_type

        picking_pos = False
        close_position = None
        chose_tile = None
        move_type = None
        # all_locs = build_the_board()

        m.draw_rectangle(400, 25, 50, 100, 'Move_Place')
        turtle.tracer(False)
        C.move_place_turtle.goto(425,75)
        C.move_place_turtle.right(90)
        C.move_place_turtle.forward(20)
        C.move_place_turtle.write("P", False, align="center", font=("Arial", 30, "normal"))
        turtle.tracer(True)

        m.draw_rectangle(400, -125, 50, 100, 'Move_Place')
        turtle.tracer(False)
        C.move_place_turtle.goto(425,-75)
        C.move_place_turtle.right(90)
        C.move_place_turtle.forward(20)
        C.move_place_turtle.write("M", False, align="center", font=("Arial", 30, "normal"))
        turtle.tracer(True)

        #print('Move type: ', move_type)
        
        turtle.onscreenclick(self.select_move_type)

        #print('Waiting for a click')
        #click_event.wait()

        #print('Finished Waiting')

        #click_event.clear()

        #print('Move type: ', move_type)

    ##    turtle.onscreenclick(None)

        while not picking_pos and move_type is None:
            C.wn.update()

        turtle.onscreenclick(None)

        C.move_place_turtle.clear()

        #print(move_type)


        if move_type == 'Place':
            picking_pos = False

            # Main loop
            turtle.onscreenclick(self.place_tile)

            while not picking_pos:
                C.wn.update()

            #print(all_locs)

            C.selection_turtle.up()
            C.selection_turtle.goto(close_position[0], close_position[1])
            C.selection_turtle.dot(10, "Red")

            positions = [250, 100, -50, -200, -350]
            letters = ["Q", "A", "G", "S", "B"]

            for y, letter in zip(positions, letters):
                m.draw_rectangle(-550, y, 50, 100, 'Selection')
                turtle.tracer(False)
                C.selection_turtle.goto(-523, y + 50)
                C.selection_turtle.right(90)
                C.selection_turtle.forward(20)
                C.selection_turtle.write(letter, False, align="center", font=("Arial", 30, "normal"))
                turtle.tracer(True)
                
            picking_pos = False

            turtle.onscreenclick(self.select_tile)

            turtle.tracer(True)

            while not picking_pos and chose_tile is None:
                C.wn.update()

            C.selection_turtle.clear()
            
            if chose_tile == 'Queen':
                C.main_turtle.goto(close_position[0], close_position[1])
                C.main_turtle.right(C.main_turtle.heading())
                chosen_bug = B('Queen', close_position[0], close_position[1], 0, human)
                chosen_bug.draw()

            elif chose_tile == 'Ant':
                C.main_turtle.goto(close_position[0], close_position[1])
                C.main_turtle.right(C.main_turtle.heading())
                chosen_bug = B('Ant', close_position[0], close_position[1], 0, human)
                chosen_bug.draw()

            elif chose_tile == 'Grasshopper':
                C.main_turtle.goto(close_position[0], close_position[1])
                C.main_turtle.right(C.main_turtle.heading())
                chosen_bug = B('Grasshopper', close_position[0], close_position[1], 0, human)
                chosen_bug.draw()

            elif chose_tile == 'Spider':
                C.main_turtle.goto(close_position[0], close_position[1])
                C.main_turtle.right(C.main_turtle.heading())
                chosen_bug = B('Spider', close_position[0], close_position[1], 0, human)
                chosen_bug.draw()

            elif chose_tile == 'Beetle':
                C.main_turtle.goto(close_position[0], close_position[1])
                C.main_turtle.right(C.main_turtle.heading())
                chosen_bug = B('Beetle', close_position[0], close_position[1], 0, human)
                chosen_bug.draw()

            #print(chose_tile)
            #print(close_position)

            orig_position = close_position
            
            return chosen_bug, move_type, orig_position

        elif move_type == 'Move':

            picking_pos = False

            # Pick the Tile you want to move
            turtle.onscreenclick(self.place_tile)

            while not picking_pos:
                C.wn.update()

            current_tile_mat_pos = []

            orig_position = close_position

            for j in current_tile_mat_class:
                current_tile_mat_pos.append(current_tile_mat_class.original_tile)

            for i in current_tile_mat_class:
                if close_position == current_tile_mat_class.original_tile and current_tile_mat_class.z >= 0 and current_tile_mat_class.team == human:
                    ava_pos = current_tile_mat_class.avaliable_move(current_tile_mat_pos)

            for j in range(len(ava_pos)):
                turtle.tracer(False)
                C.selection_turtle.up()
                C.selection_turtle.goto(ava_pos[j][0], ava_pos[j][1])
                C.selection_turtle.dot(10, 'Blue')
                turtle.tracer(True)

            picking_pos = False

            # Pick the Tile the position you want to move to
            turtle.onscreenclick(self.place_tile)

            while not picking_pos:
                C.wn.update()

            C.selection_turtle.clear()



            return chosen_bug, move_type, orig_position
    
    # Used to find all the avaliable locations a piece can be placed for a team
    def placement(self, current_tile_mat_class, human, Board):

        #current_positions = Board.current_positions
        
        current_teams = []
        current_bug = []
        current_z = []
        current_positions = []

        for a in current_tile_mat_class:
            current_teams.append(a.team)
            current_z.append(a.z)
            current_bug.append(a.bug_type)
            current_positions.append(a.original_tile) 
        
        for i in current_tile_mat_class:

            # If Not Team Skip
            if i.human != human:
                continue

            # If under something Skip
            if i.z < 0:
                continue

            # Find all the positions around the tile
            ##possible_locs = m.getlocations(i.original_tile[0], i.original_tile[1])

            for l in Board.Tiles_Mat:
                if l.x == i.original_tile[0] and l.y == i.original_tile[1]:
                    possible_locs = l.close_tiles

            # All Avaliable Positions
            ava_pos = []

            # Criteria for avaliable position
            for j in range(len(possible_locs)):

                # If it's already full skip
                if possible_locs[j] in current_positions:
                    continue

                # Get All the locations around the selected position
                #surrounding_locs = m.getlocations(i.possible_locs[j][0], [j][1])

                for j in Board.Tiles_Mat:
                    if j.x == i.possible_locs[j][0] and l.y == i.possible_locs[j][1]:
                        surrounding_locs = l.close_tiles

                # Find if it belongs to the other team
                for k in range(len(surrounding_locs)):
                    
                    # Remove the original one
                    if surrounding_locs[k] == possible_locs[j]:
                        continue
                    
                    # Check if the surrounding tile is from the other team
                    if surrounding_locs[k] in current_positions:
                        locs = [b for b, c in enumerate(current_positions) if c == surrounding_locs[k]]

                        for d in range(len(locs)):
                            if current_z[locs[d]] < 0:
                                continue

                            if current_teams[locs[d]] != human:
                                continue
                
                if possible_locs[j] not in ava_pos:
                    ava_pos.append(possible_locs[j])

        return ava_pos
    
    
    def avaliable_moves (self, current_tile_mat_class, turns, human, Board):

        # Determine if a place or move action
        # Place = 0 and Move = 1

        ava_pos = []
        final_pos = []
        place_move_mat = []
        place_move_insect = []
        original_position_mat = []
        current_positions = Board.current_positions

        ## If it's the first turn
        if turns == 0:



            for i in range(5):
                ava_pos.append([0,0])
                place_move_mat.append(0)
                original_position_mat.append([0,0])
                if i == 0:
                    place_move_insect.append('Queen')
                elif i == 1:
                    place_move_insect.append('Beetle')
                elif i == 2:
                    place_move_insect.append('Spider')
                elif i == 3:
                    place_move_insect.append('Ant')
                elif i == 4:
                    place_move_insect.append('Grasshopper')

                return ava_pos, place_move_mat, original_position_mat, place_move_insect
        
        # If a piece has already been played
        if turns == 1:
            current_tile = Board.current_positions[0]
            
            # Find Locations around the tile
            avaliable_locs = m.getlocations(current_tile[0], current_tile[1])

            # For all the avaliable places get all the options
            for i in range(len(avaliable_locs)):
                for i in range(5):
                    ava_pos.append(avaliable_locs[i][0], avaliable_locs[i][1])
                    place_move_mat.append(0)
                    original_position_mat.append(avaliable_locs[i][0], avaliable_locs[i][1])
                    if i == 0:
                        place_move_insect.append('Queen')
                    elif i == 1:
                        place_move_insect.append('Beetle')
                    elif i == 2:
                        place_move_insect.append('Spider')
                    elif i == 3:
                        place_move_insect.append('Ant')
                    elif i == 4:
                        place_move_insect.append('Grasshopper')

            return ava_pos, place_move_mat, original_position_mat, place_move_insect

        if turns > 1:
            counter = 0
            for i in current_tile_mat_class:
                # Check for your team
                if i.team == human and i.bug_type == 'Queen':
                    counter = 1
        
            # This needs to be remerged into the main query

            # Must Place Queen in
            if turns == 7 and counter == 0:
                place_move_mat.append(0)
                place_move_insect.append('Queen')

            elif turns == 6 and counter == 0:
                place_move_mat.append(0)
                place_move_insect.append('Queen')

            elif turns < 7 and turns % 2 == 0 and counter == 0:
                place_move_rand = 0

            elif turns < 6 and turns % 2 == 1 and counter == 0:
                place_move_rand = 0


            ### PLACEMENT ###
            for place_move_rand in range(2):
                if place_move_rand == 0:

                    # Calculate if I can place something
                    if turns % 2 == 1:

                        for bug_choice in range(5):

                            if bug_choice == 0 and B.team_1_queen == 1:
                                continue

                            if bug_choice == 1 and B.team_1_ant == 3:
                                continue

                            if bug_choice == 2 and B.team_1_grasshopper == 3:
                                continue

                            if bug_choice == 3 and B.team_1_beetle == 2:
                                continue

                            if bug_choice == 4 and B.team_1_spider == 2:
                                continue

                            # Add Calculation to determine what's left

                    if turns % 2 == 0:

                        for bug_choice in range(5):

                            if bug_choice == 0 and B.team_2_queen == 1:
                                continue

                            if bug_choice == 1 and B.team_2_ant == 3:
                                continue

                            if bug_choice == 2 and B.team_2_grasshopper == 3:
                                continue

                            if bug_choice == 3 and B.team_2_beetle == 2:
                                continue

                            if bug_choice == 4 and B.team_2_spider == 2:
                                continue

                    # I can place so here's the placement options
                    ava_pos = self.placement(current_tile_mat_class, human, Board)

                    # Merge Avaliable Positions and Avaliable Bugs together in same sized matrixes


                    # Append to these matrixes to complete this part
                    #return ava_pos, place_move_mat, original_position_mat, place_move_insect

        

                elif place_move_rand == 1:
                
                    ### MOVEMENT ###
                    ava_pos_combo = []
                
                    for i in current_tile_mat_class:
                        # Check for your team
                        if i.team == human:
                            ava_pos_combo.append(i.avaliable_move(current_positions))

                    ava_pos = [item for sub in ava_pos_combo for item in sub]

                    # Somehow determine which bug has moved to add to original_position_mat and place_move_insect


                    #return ava_pos, place_move_mat, original_position_mat, place_move_insect

                #Merge both moving and placing into 1