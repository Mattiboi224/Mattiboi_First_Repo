import Config as C
import util as m
import game as G
import turtle
import Board as Board
import Bugs as B

def main():

    Board = Board()
    Game = G()


    # Blank matrix for all the current tiles
    current_tile_mat = []
    current_bug_mat = []
    p1_tiles = []
    p2_tiles = []
    z_p1_tiles = []
    z_p2_tiles = []
    p1_insect_mat = []
    p2_insect_mat = []
    current_tile_mat_class = []
    p1_class = []
    p2_class = []

    C.draw_board('Green', -390, 400, "Comp")
    C.draw_board('Red', 240, 400, "You")

    for turns in range(50):

        y_positions = [385, 370, 355, 340, 325]
        insect_types = ['Queen', 'Ant', 'Grasshopper', 'Spider', 'Beetle']
        totals = [C.total_queen, C.total_ant, C.total_grasshopper, C.total_spider, C.total_beetle]

        # Announce for player 2
        Game.announce_remaining_insects('Green', [-283, -292, -242, -278, -278], y_positions, insect_types, totals, C.p2_insect_mat)

        # Announce for player 1
        Game.announce_remaining_insects('Red', [385] * len(insect_types), y_positions, insect_types, totals, C.p1_insect_mat)    

        # Whether Human is playing
        if turns % 2 == 1:
            human = 1
        else:
            human = 0

        if human == 0:
            ava_pos, place_move_mat, original_position_mat, place_move_insect = Game.avaliable_moves(current_tile_mat_class, turns, human, Board)

        if human == 1:
            chosen_bug, move_type, orig_position = G.Human_Player(current_tile_mat_class, human)

            insect = chosen_bug.bug_type
            tile = orig_position
            loc = chosen_bug.original_position
            if move_type == 'Place':
                placement = 0

            if move_type == 'Move':
                placement = 1

    


##    def board_updates(game, placement, tile, loc, insect, p1_tiles, p2_tiles, p1_insect_mat, p2_insect_mat, z_p1_tiles, z_p2_tiles, current_tile_mat, current_bug_mat):

##    insect = place_move_insect[ran_loc]
##    tile = original_position_mat[ran_loc]
##    loc = final_pos[ran_loc]
##    placement = place_move_mat[ran_loc]

        # Placing Tiles Logic
        if placement == 0 or turns == 0 or turns == 1:
            #time.sleep(0.25)
            turtle.tracer(False)
            C.main_turtle.goto(loc[0],loc[1])
            # Draw shape and put assigned name
            m.hexagon_shape(loc[0],loc[1], 'Main')

            C.main_turtle.color('black')
            
            C.main_turtle.goto(loc[0],loc[1])
            current_tile_mat.append([loc[0],loc[1]])
            Board.current_positions.append([loc[0],loc[1]])
            current_tile_mat_class.append(chosen_bug)
            
            #assign_tile(insect, turns)
            
            if turns % 2 == 1:
                p1_tiles.append([loc[0],loc[1]])
                p1_insect_mat.append(insect)
                current_bug_mat.append(insect)
                z_p1_tiles.append(0)
                p1_class.append(chosen_bug)

                #print(p1_tiles)
            else:
                p2_tiles.append([loc[0],loc[1]])
                p2_insect_mat.append(insect)
                current_bug_mat.append(insect)
                z_p2_tiles.append(0)
                p2_class.append(chosen_bug)


            turtle.tracer(True)
            #time.sleep(0.25)
            
        else:
            #time.sleep(0.25)
            #print(ava_pos)
            # If P2
            
            if turns % 2 == 0:

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

            elif turns % 2 == 1:

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
                                                    # Update the Class of the bug that moved    
                                                else:
                                                    z_p1_tiles[filled_indicesp1[i]] += 1
                                                    # Update the Class of the bug that moved    
                                            # Not a stack of beetles
                                            else:
                                                if z_p1_tiles[filled_indicesp1[i]] == -1:
                                                    z_p1_tiles[filled_indicesp1[i]] = 0
                                                    # Update the Class of the bug that moved    
                                            

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
                                                    # Update the Class of the bug that moved    
                                            # Not a stack of beetles
                                            else:
                                                if z_p2_tiles[filled_indicesp2[i]] == -1:
                                                    z_p2_tiles[filled_indicesp2[i]] = 0
                                                    # Update the Class of the bug that moved    

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
                                                # Update the Class of the bug that moved    

                                    if len(indicesp2) > 0:
                                        for i in range(len(indicesp2)):
                                            if z_p2_tiles[indicesp2[i]] == 1:
                                                z_p2_tiles[indicesp2[i]] = -1
                                                # Update the Class of the bug that moved    
                                            else:
                                                z_p2_tiles[indicesp2[i]] -= 1
                                                # Update the Class of the bug that moved    

                                else:
                                    z_p1_tiles[b] = 0
                                    # Update the Class of the bug that moved    

                            # If moving onto empty space
                            else:
                                z_p1_tiles[b] = 0     
                                # Update the Class of the bug that moved                 

                        
    ##                        # Update to new location
    ##                        for a in range(len(current_tile_mat)):
    ##                            if current_tile_mat[a] == p1_tiles[b]:
    ##                                current_tile_mat[a][0] = loc[0]
    ##                                current_tile_mat[a][1] = loc[1]

                        p1_tiles[b][0] = loc[0]
                        p1_tiles[b][1] = loc[1]

                        # Update the class of the bug that moved


    ##            if p1_insect_mat[pick_a_tile] == 'Grasshopper' or p2_insect_mat[pick_a_tile] == 'Grasshopper':
    ##                time.sleep(2)
        #Redraw All the Tiles
    
            turtle.tracer(False)
            C.main_turtle.clear()

            for i in len(current_tile_mat_class):
                if i.z >= 0:
                    m.hexagon_shape(i.original_tile[0],i.original_tile[1], 'Main')
                    i.draw()

            current_tile_mat = p1_tiles + p2_tiles

    ##    return p1_tiles, p2_tiles, p1_insect_mat, p2_insect_mat, z_p1_tiles, z_p2_tiles, current_tile_mat, current_bug_mat

main()