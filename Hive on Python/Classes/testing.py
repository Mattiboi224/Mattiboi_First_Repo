import math
from Bugs import Bugs
import Config as C
import turtle
from Player import Player as P
from game import Game

team_1 = P('TEAM_1', C.team0, 1)
team_2 = P('TEAM_2', C.team1, -1)
team_mat = []
team_mat.append(team_1)
team_mat.append(team_2)


current_teams = ['TEAM_1', 'TEAM_2', 'TEAM_1', 'TEAM_2']
current_z = [0, 0, 0, 0]
current_bug_types = ['Queen', 'Ant', 'Ant', 'Queen']
current_tiles = [[0, 0], [-60.0, -34.641], [-60.0, -173.205], [-60.0, -103.923]]

game = Game()

current_bug_mat = []
for i in range(len(current_tiles)):
    a = Bugs(current_bug_types[i], current_tiles[i][0], current_tiles[i][1], 0, team_mat[i % 2])
    a.get_tile(game.board.Tiles_Mat)
    current_bug_mat.append(a)

    for i in game.board.Tiles_Mat:
        if i.loc == a.original_tile:
            i.is_occupied = 1


game.all_bugs_class = current_bug_mat


    


# Used to find all the avaliable locations a piece can be placed for a team
def placement(team, all_bugs):

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

    print(current_teams)
    print(current_z)
    print(current_bug)
    print(current_positions)

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

        

        # Criteria for avaliable position
        for j in possible_locs:

            # If it's already full skip
            if j.is_occupied == 1:
                print('Occupied')
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


    C.testing_turtle.clear()
    C.move_type = 'Move'
    game.draw()
    turtle.tracer(False)
    for i in range(len(ava_pos)):
        C.testing_turtle.goto(ava_pos[i])
        C.testing_turtle.dot(10)

    print(ava_pos)
    return ava_pos

a = placement(team_2, current_bug_mat)

C.wn.exitonclick()