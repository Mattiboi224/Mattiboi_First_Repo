import Config as C
import util as m
import turtle
import math
from Bugs import Bugs as B
import random
from Board import Board
from collections import Counter
import copy
from dataclasses import dataclass
import time

class Game:
    def __init__(self):
        self.board = Board()
        self.all_bugs_class = []
        self.get_nearby_tiles()

    def draw(self):

        if C.move_type == 'Place':

            self.all_bugs_class[-1].draw()

        else:

            C.main_turtle.clear()

            for i in self.all_bugs_class:
                
                if i.z >= 0:
                    i.draw()

    def get_nearby_tiles(self):

        for i in self.board.Tiles_Mat:

            i.get_nearby_tiles(self.board.Tiles_Mat)

    # Announce Remaining Insects
    def announce_remaining_insects(self, team, x_positions, y_positions): 
        ##color, x_positions, y_positions, insect_types, totals, player_insects):
        
        color = team.colour
        C.announcer_turtle.color(color)

        insect_types = ['Queen', 'Ant', 'Grasshopper', 'Spider', 'Beetle']

        current_counts = [team.remaining_queen, team.remaining_ant, team.remaining_grasshopper, \
                          team.remaining_spider, team.remaining_beetle]

        for i in range(len(insect_types)):
            turtle.tracer(False)
            message = current_counts[i]
            C.announcer_turtle.goto(x_positions[i], y_positions[i])
            C.announcer_turtle.write(message, False, align="left", font=("Arial", 10, "normal"))
            turtle.tracer(True)


    # Place a tile
    def place_tile(self, x, y):
        
    
        for loc in self.board.Tiles_Mat:

            if m.dist([x, y], loc.pos()) <= loc.radius:

                if loc.is_occupied == 1:
                    continue

                C.close_position = [loc.x, loc.y]
                C.picking_pos = True

                return
        
        print('Invalid Click')
        C.picking_pos = False

    # Select a bug
    def select_a_bug(self, x, y):
    
        for loc in self.all_bugs_class:

            if m.dist([x, y], loc.pos()) <= loc.radius and loc.z >= 0 and loc.team == C.team:

                current_positions = []

                for i in self.all_bugs_class:

                    current_positions.append(i.original_tile)                
                
                # If no moves for the selected tile
                if len(loc.avaliable_move(current_positions)) == 0:
                    continue

                C.close_position = [loc.x, loc.y]
                C.picking_pos = True
                C.bug = loc

                return
        
        print('Invalid Click')
        C.picking_pos = False    


    # Move a tile
    def move_tile(self, x, y):
        
    
        for loc in range(len(self.ava_pos)):

            if m.dist([x, y], [self.ava_pos[loc][0], self.ava_pos[loc][1]]) <= C.radius:

                C.close_position = [self.ava_pos[loc][0], self.ava_pos[loc][1]]
                C.picking_pos = True

                return
        
        print('Invalid Click')
        C.picking_pos = False




        # Human Player
    def Human_Player(self, team, turns):

        C.picking_pos = False
        C.close_position = None
        C.move_type = None
        C.place_trigger = 0
        C.move_trigger = 0

        if team.remaining_ant > 0 or team.remaining_grasshopper > 0 or team.remaining_beetle > 0 or \
            team.remaining_spider > 0 or team.remaining_queen > 0:

            C.place_trigger = 1

            m.draw_rectangle(400, 25, 50, 100, 'Move_Place')
            turtle.tracer(False)
            C.move_place_turtle.goto(425,75)
            C.move_place_turtle.right(90)
            C.move_place_turtle.forward(20)
            C.move_place_turtle.write("P", False, align="center", font=("Arial", 30, "normal"))
            turtle.tracer(True)

        if turns > 1 and team.remaining_queen == 0:

            C.move_trigger = 1

            m.draw_rectangle(400, -125, 50, 100, 'Move_Place')
            turtle.tracer(False)
            C.move_place_turtle.goto(425,-75)
            C.move_place_turtle.right(90)
            C.move_place_turtle.forward(20)
            C.move_place_turtle.write("M", False, align="center", font=("Arial", 30, "normal"))
            turtle.tracer(True)

        
        turtle.onscreenclick(m.select_move_type)

        while not C.picking_pos and C.move_type is None:
            C.wn.update()

        turtle.onscreenclick(None)

        C.move_place_turtle.clear()

        #print(C.move_type)
        if C.move_type == 'Place':
            C.picking_pos = False

            # Main loop
            turtle.onscreenclick(self.place_tile)

            while not C.picking_pos:
                C.wn.update()

            turtle.onscreenclick(None)

            # Identify the chosen tile
            C.selection_turtle.up()
            C.selection_turtle.goto(C.close_position[0], C.close_position[1])
            C.selection_turtle.dot(10, "Red")

            # Add rule to remove breaking of incorrect amount of tiles

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
                
            C.picking_pos = False

            turtle.onscreenclick(m.select_tile)

            turtle.tracer(True)

            while not C.picking_pos:
                C.wn.update()

            turtle.onscreenclick(None)

            C.selection_turtle.clear()

            if C.move_type == 'Queen':
                C.main_turtle.goto(C.close_position[0], C.close_position[1])
                C.main_turtle.right(C.main_turtle.heading())
                chosen_bug = B('Queen', C.close_position[0], C.close_position[1], 0, team)
                team.remaining_queen -= 1

            elif C.move_type == 'Ant':
                C.main_turtle.goto(C.close_position[0], C.close_position[1])
                C.main_turtle.right(C.main_turtle.heading())
                chosen_bug = B('Ant', C.close_position[0], C.close_position[1], 0, team)
                team.remaining_ant -= 1

            elif C.move_type == 'Grasshopper':
                C.main_turtle.goto(C.close_position[0], C.close_position[1])
                C.main_turtle.right(C.main_turtle.heading())
                chosen_bug = B('Grasshopper', C.close_position[0], C.close_position[1], 0, team)
                team.remaining_grasshopper -= 1

            elif C.move_type == 'Spider':
                C.main_turtle.goto(C.close_position[0], C.close_position[1])
                C.main_turtle.right(C.main_turtle.heading())
                chosen_bug = B('Spider', C.close_position[0], C.close_position[1], 0, team)
                team.remaining_spider -= 1

            elif C.move_type == 'Beetle':
                C.main_turtle.goto(C.close_position[0], C.close_position[1])
                C.main_turtle.right(C.main_turtle.heading())
                chosen_bug = B('Beetle', C.close_position[0], C.close_position[1], 0, team)
                team.remaining_beetle -= 1

            for i in self.board.Tiles_Mat:
                if i.x == C.close_position[0] and i.y == C.close_position[1]:
                    i.tile = chosen_bug

            chosen_bug.get_tile(self.board.Tiles_Mat)
            self.all_bugs_class.append(chosen_bug)
            

            for i in self.board.Tiles_Mat:
                
                if i.pos() == C.close_position:
                    i.is_occupied = 1


        elif C.move_type == 'Move':

            C.picking_pos = False
            C.team = team

            # Pick the Tile you want to move
            turtle.onscreenclick(self.select_a_bug)

            while not C.picking_pos:
                C.wn.update()

            turtle.onscreenclick(None)

            current_tile_mat = []
            for i in self.all_bugs_class:
                current_tile_mat.append(i.original_tile)
                

            self.ava_pos = []
            self.ava_pos = C.bug.avaliable_move(current_tile_mat)

            for j in range(len(self.ava_pos)):
                turtle.tracer(False)
                C.selection_turtle.up()
                C.selection_turtle.goto(self.ava_pos[j][0], self.ava_pos[j][1])
                C.selection_turtle.dot(10, 'Blue')
                turtle.tracer(True)

            C.picking_pos = False

            # Pick the Tile the position you want to move to
            turtle.onscreenclick(self.move_tile)

            while not C.picking_pos:
                C.wn.update()

            C.selection_turtle.clear()

            turtle.onscreenclick(None)

            all_bugs, all_tiles = self.apply_move_tile(C.bug, C.close_position, self.all_bugs_class, self.board.Tiles_Mat)

            self.all_bugs_class = all_bugs
            self.board.Tiles_Mat = all_tiles


    def apply_move_tile(self, bug_class, move, all_bugs, all_tiles):

        #print(move)
        #print(bug_class)
        for i in all_tiles:
            
            if i.loc == move:
                a = i
                #print(a)

            if i.loc == bug_class.original_tile:
                b = i


                #print(b)
            

        old_bugs_on_a_tile = []
        new_bugs_on_a_tile = []

        if bug_class.bug_type == 'Beetle':

            
            for i in all_bugs:
                
                # Find what it's moving onto
                if i.original_tile == move:
                    new_bugs_on_a_tile.append(i)

                # Find what it's moving from
                if bug_class.original_tile == i.original_tile and i != bug_class:
                    old_bugs_on_a_tile.append(i)




            # Move onto something and adjust everything underneath
            if len(new_bugs_on_a_tile) > 0:

                for i in new_bugs_on_a_tile:
                    i.z -= 1

            else:
                a.is_occupied = 1


            # Move from something and readjust everything underneath
            if len(old_bugs_on_a_tile) > 0:

                for i in old_bugs_on_a_tile:
                    i.z += 1

            else:
                b.is_occupied = 0

        else:
            a.is_occupied = 1
            b.is_occupied = 0
            #print('Adjusted')

        # Check if this works
        bug_class.update(move)
        bug_class.get_tile(all_tiles)

        return all_bugs, all_tiles




    
    # Used to find all the avaliable locations a piece can be placed for a team
    def placement(self, team, all_bugs):

        #current_positions = Board.current_positions
        
        current_teams = []
        current_bug = []
        current_z = []
        current_positions = []

        for a in all_bugs:
            current_teams.append(a.team.team)
            current_z.append(a.z)
            current_bug.append(a.bug_type)
            current_positions.append(a.original_tile)

        # print(current_teams)
        # print(current_z)
        # print(current_bug)
        # print(current_positions)

        # All Avaliable Positions
        ava_pos = []
        
        # All the avaliable positions around your own tiles
        for i in all_bugs:

            # If Not Team Skip
            if i.team.team != team.team:
                continue

            # If under something Skip
            if i.z < 0:
                continue

            # Find all the positions around the tile
            ##possible_locs = m.getlocations(i.original_tile[0], i.original_tile[1])

            possible_locs = i.Tile.nearby_tiles

            # if i.Tile in self.board.Tiles_Mat:
            #     print('Tile is in self')

            # Criteria for avaliable position
            for j in possible_locs:

                # If it's already full skip
                if j.is_occupied == 1:
                    continue

                # Get All the locations around the selected position
                #j.nearby_tiles

                # Find if it belongs to the other team
                wrong_team = 0
                for k in j.nearby_tiles:
                    
                    # Remove the original one
                    if k == j:
                        continue

                    for l in all_bugs:
                        if l.Tile.loc == k.loc and l.z >= 0:

                    # Check if the surrounding tile is from the other team
                            if l.team.team != team.team:
                                wrong_team = 1
                        
                
                if j.loc not in ava_pos and wrong_team == 0:
                    ava_pos.append(j.loc)


        # C.testing_turtle.clear()
        # turtle.tracer(False)
        # for i in range(len(ava_pos)):
        #     C.testing_turtle.goto(ava_pos[i])
        #     C.testing_turtle.dot(10)

        return ava_pos
    
    
    def avaliable_moves (self, team, turns, all_bugs):

        # Determine if a place or move action
        # Place = 0 and Move = 1

        ava_pos = []
        final_pos = []
        place_move_mat = []
        place_move_insect = []
        original_position_mat = []
        current_positions = []
        bug_class_mat = []
        original_bug_class = []

        for i in all_bugs:

            current_positions.append(i.original_tile)

        ## If it's the first turn
        if turns == 0:

            for i in range(5):
                if i == 0:
                    insect = 'Queen'
                elif i == 1:
                    insect = 'Beetle'
                elif i == 2:
                    insect = 'Spider'
                elif i == 3:
                    insect = 'Ant'
                elif i == 4:
                    insect = 'Grasshopper'


                bug_class = B(insect, 0, 0, 0, team)
                bug_class.m_p = 'Place'
                bug_class.get_tile(self.board.Tiles_Mat)

                bug_class_mat.append(bug_class)
                original_bug_class.append(bug_class)


                return original_bug_class, bug_class_mat
        
        # If a piece has already been played
        if turns == 1:
            current_tile = all_bugs[0]
            
            # Find Locations around the tile
            avaliable_locs = current_tile.Tile.nearby_tiles

            #print(avaliable_locs)

            # For all the avaliable places get all the options
            for j in avaliable_locs:

                if j.is_occupied == 1:
                    continue

                for i in range(5):
                    if i == 0:
                        insect = 'Queen'
                    elif i == 1:
                        insect = 'Beetle'
                    elif i == 2:
                        insect = 'Spider'
                    elif i == 3:
                        insect = 'Ant'
                    elif i == 4:
                        insect = 'Grasshopper'

                    bug_class = B(insect, j.x, j.y, 0, team)
                    bug_class.m_p = 'Place'
                    bug_class.get_tile(self.board.Tiles_Mat)
                    bug_class_mat.append(bug_class)
                    original_bug_class.append(bug_class)

            return original_bug_class, bug_class_mat
        
        if turns > 1:
            
            place_move_choice = 1
        
            # This needs to be remerged into the main query

            # Must Place Queen in
            if turns < 7 and turns % 2 == 0 and team.remaining_queen == 1:
                place_move_choice = 0

            elif turns < 6 and turns % 2 == 1 and team.remaining_queen == 1:
                place_move_choice = 0


            ### PLACEMENT ###
            
            for place_move_rand in range(2):
                if place_move_rand == 0:

                    # I can place so here's the placement options
                    ava_pos = self.placement(team, all_bugs)

                    for bug_choice in range(5):

                        if place_move_choice == 0:
                            bug_choice = 0

                        if bug_choice == 0 and team.remaining_queen == 0:
                            continue

                        if bug_choice == 1 and team.remaining_ant == 0:
                            continue

                        if bug_choice == 2 and team.remaining_grasshopper == 0:
                            continue

                        if bug_choice == 3 and team.remaining_beetle == 0:
                            continue

                        if bug_choice == 4 and team.remaining_spider == 0:
                            continue

                        if bug_choice == 0:
                            insect = 'Queen'
                        elif bug_choice == 1:
                            insect = 'Ant'
                        elif bug_choice == 2:
                            insect = 'Grasshopper'
                        elif bug_choice == 3:
                            insect = 'Beetle'
                        elif bug_choice == 4:
                            insect = 'Spider'




                        # Merge Avaliable Positions and Avaliable Bugs together in same sized matrixes
                        for i in range(len(ava_pos)):
                            bug_class = B(insect, ava_pos[i][0], ava_pos[i][1], 0, team)
                            bug_class.m_p = 'Place'
                            bug_class.get_tile(self.board.Tiles_Mat)
                            
                            if bug_class not in bug_class_mat:
                                bug_class_mat.append(bug_class)
                                original_bug_class.append(bug_class)

                            


                    # Append to these matrixes to complete this part
                    #return ava_pos, place_move_mat, original_position_mat, place_move_insect

        

                elif place_move_rand == 1 and place_move_choice == 1:
                
                    ### MOVEMENT ###
                    ava_pos_combo = []
                    class_combo = []
                
                    for i in all_bugs:

                        # Under something skip
                        if i.z < 0:
                            continue

                        # Check for your team
                        if i.team == team:
                            ava_pos_combo.append(i.avaliable_move(current_positions))
                            class_combo.append(i)
                            
                        

                    for i in range(len(ava_pos_combo)):
                        for j in range(len(ava_pos_combo[i])):


                            # Check if the place it's going exists in the play area
                            for k in self.board.Tiles_Mat:
                                if k.loc == ava_pos_combo[i][j]:


                                    bug_class = B(class_combo[i].bug_type, ava_pos_combo[i][j][0], ava_pos_combo[i][j][1], 0, team)
                                    bug_class.m_p = 'Move'
                                    original_bug_class.append(class_combo[i])
                                    bug_class_mat.append(bug_class)

                                    break

            #print('Moved Queen Bug')

            
            return original_bug_class, bug_class_mat
    
    
    def ai_select_a_move(self, original_bug_class, bug_class_mat, all_bug):
        pass


    def ai_random_number_generator(self, team, turns, original_bug_class, bug_class_mat, all_bug, all_tiles):
        
        # No Move Avaliable
        if len(bug_class_mat) == 0:
            return

        chosen_number = random.randint(0, len(bug_class_mat) - 1)

        self.apply_move(team, turns, original_bug_class[chosen_number], bug_class_mat[chosen_number], all_bug, all_tiles)

    def apply_move(self, team, turns, original_bug, bug_class, all_bug, all_tiles):
        
        # If the chosen one is Place a Tile
        if bug_class.m_p == 'Place':

            if bug_class.bug_type == 'Queen':

                team.remaining_queen -= 1

            if bug_class.bug_type == 'Ant':

                team.remaining_ant -= 1

            if bug_class.bug_type == 'Grasshopper':

                team.remaining_grasshopper -= 1

            if bug_class.bug_type == 'Beetle':

                team.remaining_beetle -= 1

            if bug_class.bug_type == 'Spider':

                team.remaining_spider -= 1        


            bug_class.m_p = None

            all_bug.append(bug_class)

            for i in all_tiles:

                if i.loc == bug_class.original_tile:
                    
                    i.is_occupied = 1

            #print(bug_class_mat[chosen_number].Tile)

            C.move_type = 'Place'

        
        else:

            C.move_type = 'Move'

            #print(bug_class_mat[chosen_number].original_tile)

            bug_class.m_p = None

            all_bug, all_tiles = self.apply_move_tile(original_bug, bug_class.original_tile, all_bug, \
                            all_tiles)
            
        return all_bug, all_tiles


    def is_terminal(self, team, turns):

        if turns == 49:
            return True

        for i in self.all_bugs_class:

            count_opp = 0
            count_own = 0

            # Find the Opposing Queen
            if i.bug_type == 'Queen' and i.team != team:
                
                for j in i.Tile.nearby_tiles:
                    
                    if j.is_occupied == 1:

                        count_opp += 1

                # If all spaces around it is occupied

                #print(team.team, ' ', count)
                if count_opp == 6:
                    return True

            # Find the Opposing Queen
            if i.bug_type == 'Queen' and i.team == team:
                
                for j in i.Tile.nearby_tiles:
                    
                    if j.is_occupied == 1:

                        count_own += 1

                # If all spaces around it is occupied

                #print(team.team, ' ', count)
                if count_own == 6:
                    return True

        return False

    def evaluate(self, team, turns):

        if turns == 49:
            return 0
        
        for i in self.all_bugs_class:

            count_opp = 0
            count_own = 0

            # Find the Opposing Queen
            if i.bug_type == 'Queen' and i.team != team:
                
                for j in i.Tile.nearby_tiles:
                    
                    if j.is_occupied == 1:

                        count_opp += 1

                # If all spaces around it is occupied

                #print(team.team, ' ', count)
                if count_opp == 6:
                    return 1

            # Find the Opposing Queen
            if i.bug_type == 'Queen' and i.team == team:
                
                for j in i.Tile.nearby_tiles:
                    
                    if j.is_occupied == 1:

                        count_own += 1

                # If all spaces around it is occupied

                #print(team.team, ' ', count)
                if count_own == 6:
                    return 0
                     

    def scoring(self, team, turns, real_original_bug_class, real_bug_class_mat, real_all_bugs, real_all_tiles):
                #points_ranking, move_place, insect_type, new_pos, orig_pos, own_queen_mat, opp_queen_mat, \
                #own_tiles, opp_tiles, own_insect_mat, opp_insect_mat, opp_queen_loc, filled_own_queen_mat, \
                #filled_opp_queen_mat, connect_to_own, connect_to_opp, current_tile_mat, current_tile_mat_copy, game):

        score = 0
        piece_close_to_own_queen = 0
        piece_close_to_opp_queen = 0
        opp_queen_exists = False
        own_queen_exists = False
        curr_current_positions = []

        # Current Avaliable Moves
        ava_pos_all = []
        for i in real_all_bugs:

            if team.team != i.team.team:
                ava_pos = i.avaliable_move(curr_current_positions)
                ava_pos_all.append(ava_pos)

            if i.bug_type == 'Queen' and team.team != i.team.team:
                curr_opp_slideable_locs = m.slideable_locs(i.original_tile, curr_current_positions)

            if i.bug_type == 'Queen' and team.team == i.team.team:
                curr_same_slideable_locs = m.slideable_locs(i.original_tile, curr_current_positions)

        for i in real_all_bugs:

            curr_current_positions.append(i.original_tile)

        all_bugs = copy.deepcopy(real_all_bugs)
        all_tiles = copy.deepcopy(real_all_tiles)
        original_bug_class = real_original_bug_class
        bug_class_mat = real_bug_class_mat

        # Reassigning internal classes
        for i in all_tiles:
            i.get_nearby_tiles(all_tiles)

        for i in all_bugs:
            for j in all_tiles:
                if i.original_tile == j.loc:
                    i.Tile = j

        for j in all_tiles:
            if original_bug_class.original_tile == j.loc:
                original_bug_class.Tile = j

            if bug_class_mat.original_tile == j.loc:
                bug_class_mat.Tile = j


        # Pre Information Required
        for i in all_bugs:


            # Find the Opposing Queen
            if i.bug_type == 'Queen' and i.team.team != team.team:

                opp_queen_exists = True
                queen_bug = i
                
                for j in i.Tile.nearby_tiles:
                    
                    if j.is_occupied == 1:

                        piece_close_to_own_queen += 1

            # Find the Opposing Queen
            if i.bug_type == 'Queen' and i.team.team == team.team:

                own_queen_exists = True

                for j in i.Tile.nearby_tiles:
                    
                    if j.is_occupied == 1:

                        piece_close_to_opp_queen += 1

        if bug_class_mat.m_p == 'Place':
            
            # Apply the steps
            all_bugs.append(bug_class_mat)

            new_current_positions = []

            for i in all_bugs:

                new_current_positions.append(i.original_tile)

            if own_queen_exists:
                
                close_queen_locs = []
                for j in i.Tile.nearby_tiles:
                    close_queen_locs.append(j.loc)

                for j in range(len(i.avaliable_move(curr_current_positions))):

                    if j in close_queen_locs:
                        
                        # You can win
                        if piece_close_to_opp_queen == 5:
                            score += 500

                        elif piece_close_to_opp_queen == 4:
                            score += 100

                        

                        else:
                            score += 20


        if bug_class_mat.m_p == 'Move':
            
            all_bugs, all_tiles = self.apply_move_tile(original_bug_class, bug_class_mat.original_tile, all_bugs, all_tiles)

            new_current_positions = []

            for i in all_bugs:
                new_current_positions.append(i.original_tile)

            ava_pos_new = []
            for i in all_bugs:

                if team.team != i.team.team:
                    ava_pos = i.avaliable_move(new_current_positions)
                    ava_pos_new.append(ava_pos)

                if i.bug_type == 'Queen' and team.team != i.team.team:
                    new_opp_slideable_locs = m.slideable_locs(i.original_tile, new_current_positions)

                if i.bug_type == 'Queen' and team.team == i.team.team:
                    new_same_slideable_locs = m.slideable_locs(i.original_tile, new_current_positions)

            ava_pos_all_flat = [x for sub in ava_pos_all for x in sub]
            ava_pos_new_flat = [x for sub in ava_pos_new for x in sub]

            # If Original Has More moves then new block yourself
            if len(ava_pos_new_flat) - len(ava_pos_all_flat) < 0:

                score -= 20

            if len(ava_pos_new_flat) - len(ava_pos_all_flat) > 5:

                score += 5

            if len(ava_pos_new_flat) - len(ava_pos_all_flat) > 10:

                score += 10

            if len(ava_pos_new_flat) - len(ava_pos_all_flat) > 20:

                score += 20

            # Pre Information Required
            new_piece_close_to_opp_queen = 0
            new_piece_close_to_own_queen = 0
            for i in all_bugs:


                # Find the Opposing Queen
                if i.bug_type == 'Queen' and i.team != team:

                    for j in i.Tile.nearby_tiles:
                        
                        if j.is_occupied == 1:

                            new_piece_close_to_opp_queen += 1

                # Find the Opposing Queen
                if i.bug_type == 'Queen' and i.team == team:
                    
                    for j in i.Tile.nearby_tiles:
                        
                        if j.is_occupied == 1:

                            new_piece_close_to_own_queen += 1

            # Moved Next to the Queen
            if new_piece_close_to_opp_queen > piece_close_to_opp_queen:
                
                score += 20
            
            # Won the Game
            if new_piece_close_to_opp_queen == 6:
                
                score += 1000

            # Close to Winning
            if new_piece_close_to_opp_queen == 5 and piece_close_to_opp_queen == 4:

                score += 100

            # Moved Away from Opposing Queen bad
            if len(new_opp_slideable_locs) < len(curr_opp_slideable_locs) and own_queen_exists and opp_queen_exists:
                score -= 20
            
            # Moved Towards Opposing Queen
            if len(new_opp_slideable_locs) > len(curr_opp_slideable_locs) and own_queen_exists and opp_queen_exists:
                score += 50

            # Moved Away from Opp Queen
            if len(new_opp_slideable_locs) < len(curr_opp_slideable_locs) and own_queen_exists and opp_queen_exists:
                score -= 20

            # Blocks Opp Queen from moving
            if len(new_opp_slideable_locs) == 0 and len(curr_opp_slideable_locs) > 0 and own_queen_exists and opp_queen_exists:
                score += 300

            
            # Lose the Game
            if new_piece_close_to_own_queen == 5 and piece_close_to_own_queen == 4 and own_queen_exists and opp_queen_exists:

                score -= 1000

            # Close to Winning
            if new_piece_close_to_own_queen == 5 and piece_close_to_own_queen == 4 and own_queen_exists and opp_queen_exists:

                score -= 100

            # Stop Opposition from Winning
            if new_piece_close_to_own_queen == 4 and piece_close_to_own_queen == 5 and own_queen_exists and opp_queen_exists:

                score += 400

            # If you give your queen more moves
            if len(new_same_slideable_locs) > len(curr_same_slideable_locs) and own_queen_exists:

                score += 20
            
            if len(new_same_slideable_locs) > 0 and len(curr_same_slideable_locs) == 0 and own_queen_exists:

                score += 200

        return score
    

    def minimax(self, team, turns, original_bug, bug_class, all_bugs, all_tiles, depth, alpha, beta, maximizing):
        if depth == 0 or self.is_terminal(team, turns):
            return self.evaluate(team, turns)
        
        print(depth)

        if maximizing:  # AI
            max_eval = -math.inf

            orig_move, actual_move = self.avaliable_moves(team, turns, all_bugs)
            for i in range(len(actual_move)):
                all_bugs, all_tiles = self.apply_move(team, turns, orig_move[i], actual_move[i], all_bugs, all_tiles)
                result = self.minimax(team, turns, orig_move[i], actual_move[i], all_bugs, all_tiles, depth - 1, alpha, beta, True)
                score_result = self.scoring(team, turns, orig_move[i], actual_move[i], all_bugs, all_tiles)
                print(score_result)
                max_eval = max(max_eval, result, score_result)
                alpha = max(alpha, result, score_result)
                if alpha >= beta:
                    break
            return max_eval
        
    def best_move(self, team, turns, all_bugs, all_tiles):
        best_value = -math.inf
        move_chosen = None

        orig_move, actual_move = self.avaliable_moves(team, turns, all_bugs)

        for i in range(len(actual_move)):
            all_bugs, all_tiles = self.apply_move(team, turns, orig_move[i], actual_move[i], all_bugs, all_tiles)
            value = self.minimax(team, turns, orig_move[i], actual_move[i], all_bugs, all_tiles, 9, -math.inf, math.inf, True)
            if value > best_value:
                best_value = value
                move_chosen = actual_move

        return move_chosen

        # else:  # Human
        #     min_eval = math.inf
        #     for move in get_possible_moves(board):
        #         result = minimax(apply_move(board, move, HUMAN), depth - 1, alpha, beta, True)
        #         min_eval = min(min_eval, result)
        #         beta = min(beta, result)
        #         if alpha >= beta:
        #             break
        #     return min_eval

            

        # # Move next opposing queen!
        # if move_place == 1 and new_pos in opp_queen_mat and orig_pos not in opp_queen_mat and insect_type != 'Queen' and new_pos not in current_tile_mat:
        #     points_ranking += 50

        #     slideable = slideable_locs(opp_queen_mat, current_tile_mat)
        #     slideable_mod = slideable_locs(opp_queen_mat, current_tile_mat_copy)

        #     # Win Game
        #     if len(filled_opp_queen_mat) == 5:
        #         points_ranking += 500

        #     # Win Game
        #     if len(filled_opp_queen_mat) == 4:
        #         points_ranking += 75

        #     # Adding Bonus Point based on location
        #     if len(slideable) == len(slideable_mod):
        #         points_ranking += 0

        #     elif len(slideable) - len(slideable_mod) == 1:
        #         points_ranking += 20
                
        #     # Blocking a slide
        #     elif len(slideable) - len(slideable_mod) == 2:
        #         points_ranking += 35

        #     # Blocking an exit
        #     elif len(slideable) - len(slideable_mod) == 3:
        #         points_ranking += 40

        #     else:
        #         points_ranking += 55

        # # Move Bettle on a piece which next to the opposing queen!
        # if move_place == 1 and new_pos in opp_queen_mat and orig_pos not in opp_queen_mat and insect_type != 'Queen' and new_pos in current_tile_mat:
        #     points_ranking += 20

        #     slideable = slideable_locs(opp_queen_mat, current_tile_mat)
        #     slideable_mod = slideable_locs(opp_queen_mat, current_tile_mat_copy)

        #     # Win Game
        #     if len(filled_opp_queen_mat) == 5:
        #         points_ranking += 300

        #     # Adding Bonus Point based on location
        #     if len(slideable) == len(slideable_mod):
        #         points_ranking += 0

        #     elif len(slideable) - len(slideable_mod) == 1:
        #         points_ranking += 10
                
        #     # Blocking a slide
        #     elif len(slideable) - len(slideable_mod) == 2:
        #         points_ranking += 15

        #     # Blocking an exit
        #     elif len(slideable) - len(slideable_mod) == 3:
        #         points_ranking += 20

        #     else:
        #         points_ranking += 25

        # # Move next to own queen defensive piece
        # if move_place == 1 and new_pos in own_queen_mat and len(filled_own_queen_mat) <= 3 and insect_type != 'Queen':
        #     points_ranking += 15

        # # Move a piece that blocks queen
        # if move_place == 1 and new_pos in own_queen_mat and len(filled_own_queen_mat) == 4 and insect_type != 'Queen':
        #     points_ranking += -15

        #     slideable = slideable_locs(opp_queen_mat, current_tile_mat)
        #     slideable_mod = slideable_locs(opp_queen_mat, current_tile_mat_copy)        

        #     # Now not slideable and probably will lose
        #     if len(slideable) == 2 and len(slideable_mod) == 0:
        #         points_ranking += -20

        # if 'Queen' in opp_insect_mat:
        #     slideable = slideable_locs(opp_queen_mat, current_tile_mat)
        #     # Sit Beetle on Queen and Queen Can Move and Slide Out
        #     if move_place == 1 and insect_type == 'Beetle' and opp_tiles[opp_queen_loc] == new_pos and len(slideable) > 0 and connect_to_own:
        #         points_ranking += 50

        #     # Sit Beetle on Queen and Queen Can't Move but can slide out
        #     if move_place == 1 and insect_type == 'Beetle' and opp_tiles[opp_queen_loc] == new_pos and len(slideable) > 0 and not connect_to_own:
        #         points_ranking += 35

        #     # Sit Beetle on Queen and Queen Can't Move and can't slide out
        #     if move_place == 1 and insect_type == 'Beetle' and opp_tiles[opp_queen_loc] == new_pos and len(slideable) == 0 and not connect_to_own:
        #         points_ranking += 30

        # # Move a piece that loses the game
        # if move_place == 1 and new_pos in own_queen_mat and len(filled_own_queen_mat) == 5:
        #     points_ranking += -100

        # #ava_pos_new, final_pos_new, place_move_mat_new, place_move_insect_new, original_position_mat_new = available_moves(game, current_tile_mat, current_bug_mat, opp_tiles, own_tiles, z_p1_tiles, z_p2_tiles, opp_insect_mat, own_insect_mat)

        # # Placing piece priority
        # if move_place == 0 and game >= 3:

        #     if insect_type == 'Beetle' and 'Queen' in own_insect_mat:
        #         beetle_pos = beetle_logic(new_pos, current_tile_mat_copy)
        #         current_tile_mat_copy.pop(-1)
        #         one_time = 1
        #         for p in range(len(beetle_pos)):
        #             if beetle_pos[p] in opp_queen_mat:
        #                 points_ranking += 10
        #                 current_tile_mat_copy.append(beetle_pos[p])

        #                 slideable = slideable_locs(opp_queen_mat, current_tile_mat)
        #                 slideable_mod = slideable_locs(opp_queen_mat, current_tile_mat_copy)
                        
        #                 # Win Game
        #                 if len(filled_opp_queen_mat) == 5:
        #                     if one_time == 1:
        #                         points_ranking += 30

        #                 # Adding Bonus Point based on location
        #                 if len(slideable) == len(slideable_mod):
        #                     points_ranking += 0

        #                 elif len(slideable) - len(slideable_mod) == 1:
        #                     points_ranking += 2
                            
        #                 # Blocking a slide
        #                 elif len(slideable) - len(slideable_mod) == 2:
        #                     points_ranking += 5

        #                 # Blocking an exit
        #                 elif len(slideable) - len(slideable_mod) == 3:
        #                     points_ranking += 10

        #                 current_tile_mat_copy.pop(-1)

        #     if insect_type == 'Spider' and 'Queen' in opp_insect_mat:
        #         spider_pos = spider_logic(new_pos, current_tile_mat_copy)
        #         current_tile_mat_copy.pop(-1)
        #         for p in range(len(spider_pos)):
        #             if spider_pos[p] in own_queen_mat:
        #                 points_ranking += 15

        #                 current_tile_mat_copy.append(spider_pos[p])

        #                 slideable = slideable_locs(opp_queen_mat, current_tile_mat)
        #                 slideable_mod = slideable_locs(opp_queen_mat, current_tile_mat_copy)

        #                 # Win Game
        #                 if len(filled_opp_queen_mat) == 5:
        #                     points_ranking += 40

        #                 # Win Game
        #                 if len(filled_opp_queen_mat) == 4:
        #                     points_ranking += 30

        #                 # Adding Bonus Point based on location
        #                 if len(slideable) == len(slideable_mod):
        #                     points_ranking += 0

        #                 elif len(slideable) - len(slideable_mod) == 1:
        #                     points_ranking += 2
                            
        #                 # Blocking a slide
        #                 elif len(slideable) - len(slideable_mod) == 2:
        #                     points_ranking += 5

        #                 # Blocking an exit
        #                 elif len(slideable) - len(slideable_mod) == 3:
        #                     points_ranking += 10

        #                 current_tile_mat_copy.pop(-1)


        #     if insect_type == 'Ant' and 'Queen' in opp_insect_mat:

        #         ant_pos = ant_logic(new_pos, current_tile_mat_copy)
        #         current_tile_mat_copy.pop(-1)
        #         for p in range(len(ant_pos)):
        #             if ant_pos[p] in opp_queen_mat:
        #                 points_ranking += 5

        #                 current_tile_mat_copy.append(ant_pos[p])

        #                 slideable = slideable_locs(opp_queen_mat, current_tile_mat)
        #                 slideable_mod = slideable_locs(opp_queen_mat, current_tile_mat_copy)

        #                 # Win Game
        #                 if len(filled_opp_queen_mat) == 5:
        #                     points_ranking += 40

        #                 # Win Game
        #                 if len(filled_opp_queen_mat) == 4:
        #                     points_ranking += 30

        #                 # Adding Bonus Point based on location
        #                 if len(slideable) == len(slideable_mod):
        #                     points_ranking += 0

        #                 elif len(slideable) - len(slideable_mod) == 1:
        #                     points_ranking += 2
                            
        #                 # Blocking a slide
        #                 elif len(slideable) - len(slideable_mod) == 2:
        #                     points_ranking += 5

        #                 # Blocking an exit
        #                 elif len(slideable) - len(slideable_mod) == 3:
        #                     points_ranking += 10

        #                 current_tile_mat_copy.pop(-1)
                        
        #     if insect_type == 'Grasshopper' and 'Queen' in opp_insect_mat:
        #         grass_pos = grasshopper_pathway(new_pos, current_tile_mat_copy)
        #         grass_pos = [list(inner_list) for inner_list in grass_pos]
        #         current_tile_mat_copy.pop(-1)
                
        #         for p in range(len(grass_pos)):
        #             if grass_pos[p] in opp_queen_mat:
        #                 points_ranking += 15

        #                 current_tile_mat_copy.append(grass_pos[p])

        #                 slideable = slideable_locs(opp_queen_mat, current_tile_mat)
        #                 slideable_mod = slideable_locs(opp_queen_mat, current_tile_mat_copy)

        #                 # Win Game
        #                 if len(filled_opp_queen_mat) == 5:
        #                     points_ranking += 40

        #                 # Win Game
        #                 if len(filled_opp_queen_mat) == 4:
        #                     points_ranking += 30

        #                 # Adding Bonus Point based on location
        #                 if len(slideable) == len(slideable_mod):
        #                     points_ranking += 10

        #                 elif len(slideable) - len(slideable_mod) == 1:
        #                     points_ranking += 15
                            
        #                 # Blocking a slide
        #                 elif len(slideable) - len(slideable_mod) == 2:
        #                     points_ranking += 10

        #                 # Blocking an exit
        #                 elif len(slideable) - len(slideable_mod) == 3:
        #                     points_ranking += 15

        #                 current_tile_mat_copy.pop(-1)
        # return points_ranking

