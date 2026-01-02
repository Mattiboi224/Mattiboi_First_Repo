import Config as C
import util as m
import turtle
import math
from Bugs import Bugs as B
import random
from Board import Board
from collections import Counter

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

            self.apply_move(C.bug, C.close_position)


    def apply_move(self, bug_class, move):
        for i in self.board.Tiles_Mat:
            
            if i.loc == move:
                a = i
                #print(a)

            if i.loc == bug_class.original_tile:
                b = i


                #print(b)
            

        old_bugs_on_a_tile = []
        new_bugs_on_a_tile = []

        if bug_class.bug_type == 'Beetle':

            
            for i in self.all_bugs_class:
                
                # Find what it's moving onto
                if i.original_tile == move:
                    new_bugs_on_a_tile.append(i)

                # Find what it's moving from
                if bug_class.original_tile == i.original_tile and i != bug_class:
                    old_bugs_on_a_tile.append(i)


                if i == bug_class:
                    #print('Found itself')
                    pass


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
                b.is_occupied = 1

        else:
            a.is_occupied = 1
            b.is_occupied = 0

        # Check if this works
        bug_class.update(move)
        bug_class.get_tile(self.board.Tiles_Mat)


    
    # Used to find all the avaliable locations a piece can be placed for a team
    def placement(self, team, all_bugs):

        #current_positions = Board.current_positions
        
        current_teams = []
        current_bug = []
        current_z = []
        current_positions = []

        for a in all_bugs:
            current_teams.append(a.team)
            current_z.append(a.z)
            current_bug.append(a.bug_type)
            current_positions.append(a.original_tile)

        
        for i in all_bugs:

            # If Not Team Skip
            if i.team != team:
                continue

            # If under something Skip
            if i.z < 0:
                continue

            # Find all the positions around the tile
            ##possible_locs = m.getlocations(i.original_tile[0], i.original_tile[1])

            possible_locs = i.Tile.nearby_tiles

            # All Avaliable Positions
            ava_pos = []

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
                        if l.Tile == k and l.z >= 0:

                    # Check if the surrounding tile is from the other team
                            if l.team != team:
                                wrong_team = 1
                        
                
                if j.loc not in ava_pos and wrong_team == 0:
                    ava_pos.append(j.loc)

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
            if turns == 7 and team.remaining_queen == 1:
                place_move_mat.append(0)
                place_move_insect.append('Queen')

            elif turns == 6 and team.remaining_queen == 1:
                place_move_mat.append(0)
                place_move_insect.append('Queen')

            elif turns < 7 and turns % 2 == 0 and team.remaining_queen == 1:
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

                        
            return original_bug_class, bug_class_mat
    
    
    def ai_select_a_move(self, original_bug_class, bug_class_mat, all_bug):
        pass


    def ai_random_number_generator(self, team, original_bug_class, bug_class_mat, all_bug):
        
        # No Move Avaliable
        if len(bug_class_mat) == 0:
            return

        chosen_number = random.randint(0, len(bug_class_mat) - 1)

        # If the chosen one is Place a Tile
        if bug_class_mat[chosen_number].m_p == 'Place':

            if bug_class_mat[chosen_number].bug_type == 'Queen':

                team.remaining_queen -= 1

            if bug_class_mat[chosen_number].bug_type == 'Ant':

                team.remaining_ant -= 1

            if bug_class_mat[chosen_number].bug_type == 'Grasshopper':

                team.remaining_grasshopper -= 1

            if bug_class_mat[chosen_number].bug_type == 'Beetle':

                team.remaining_beetle -= 1

            if bug_class_mat[chosen_number].bug_type == 'Spider':

                team.remaining_spider -= 1        


            bug_class_mat[chosen_number].m_p = None

            all_bug.append(bug_class_mat[chosen_number])

            for i in self.board.Tiles_Mat:
                
                if i == bug_class_mat[chosen_number].Tile:
                    i.is_occupied = 1

            #print(bug_class_mat[chosen_number].Tile)

            C.move_type = 'Place'
        
        else:

            C.move_type = 'Move'

            #print(bug_class_mat[chosen_number].original_tile)

            self.apply_move(original_bug_class[chosen_number], bug_class_mat[chosen_number].original_tile)


    def is_win(self, team):

        for i in self.all_bugs_class:

            count = 0

            # Find the Opposing Queen
            if i.bug_type == 'Queen' and i.team != team:
                
                for j in i.Tile.nearby_tiles:
                    
                    if j.is_occupied == 1:

                        count += 1

                # If all spaces around it is occupied

                #print(team.team, ' ', count)
                if count == 6:
                    return True
                
        return False
