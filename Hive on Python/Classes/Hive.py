# Improvements
# Keep moving objects over
# Add clicking to game

# Add Different AI versions

# Bugs

# Fix moving bugs updating logic

import Config as C
import util as m
from game import Game as G
import turtle
from Player import Player as P
import copy
import math
import random
import time

team_1 = P('TEAM_1', C.team0, 1)
team_2 = P('TEAM_2', C.team1, -1)

team_mat = []

team_mat.append(team_1)
team_mat.append(team_2)



def main():

    Game = G()

    Game.board.draw_board(team_mat[1].colour, -390, 400, team_mat[1].text)
    Game.board.draw_board(team_mat[0].colour, 240, 400, team_mat[0].text)

    for turns in range(12):

        y_positions = [385, 370, 355, 340, 325]
        insect_types = ['Queen', 'Ant', 'Grasshopper', 'Spider', 'Beetle']

        # Clear the announcer
        C.announcer_turtle.clear()

        # Announce for player 2
        Game.announce_remaining_insects(team_mat[1], [-283, -292, -242, -278, -278], y_positions)

        # Announce for player 1
        Game.announce_remaining_insects(team_mat[0], [385] * len(insect_types), y_positions)

        team = team_mat[turns % 2]
        human = team.is_human


        if turns % 2 == 0:
            print(turns)
            if human == 1:
                Game.Human_Player(team_mat[turns % 2], turns)
                #print(turns)

        if turns % 2 == 1:
            print(turns)
            if human == 0 or human == -1:
                #print(turns)

                # C.testing_turtle.clear()
                # for i in Game.board.Tiles_Mat:
                #     if i.is_occupied == 1:
                #         turtle.tracer(False)
                #         C.testing_turtle.goto(i.loc)
                #         C.testing_turtle.color('Blue')
                #         C.testing_turtle.dot(10)
                #         turtle.tracer(True)

                original_bug_class, bug_class_mat = Game.avaliable_moves(team_mat[turns % 2], turns, Game.all_bugs_class)

                ## Change to Have Move + State = New State
                ## Pull Out Apply Move
                
                if human == 0:
                    # Starting with Random Number Generator
                    Game.ai_random_number_generator(team_mat[turns % 2], turns, original_bug_class, bug_class_mat, Game.all_bugs_class, Game.board.Tiles_Mat)
                    
                    if turns == 11:
                        best_move = Game.best_move(team_mat[turns % 2], turns, Game.all_bugs_class, Game.board.Tiles_Mat)

                        print(best_move.m_p)
                        C.testing_turtle.goto(best_move.x, best_move.y)
                        C.testing_turtle.dot(30)

                elif human == -1:
                    score_ranking = []
                    for i in range(len(bug_class_mat)):
                        score = Game.scoring(team_mat[turns % 2], turns, original_bug_class[i], bug_class_mat[i], Game.all_bugs_class, Game.board.Tiles_Mat)

                        score_ranking.append(score)
                    
                    #print(max(score_ranking))

                    max_tile = max(score_ranking)

                    index = [i for i, x in enumerate(score_ranking) if x == max_tile]

                    random_highest = random.randint(0, len(index)-1)
                    #print(random_highest)

                    all_bugs, all_tiles = Game.apply_move(team_mat[turns % 2], turns, original_bug_class[random_highest], bug_class_mat[random_highest], Game.all_bugs_class, Game.board.Tiles_Mat)
                    
                    for i in all_bugs:
                        i.get_tile(Game.board.Tiles_Mat)
                    
                    Game.all_bugs_class = all_bugs
                    Game.board.Tiles_Mat = all_tiles

        # C.testing_turtle.clear()
        # for i in Game.board.Tiles_Mat:
        #     if i.is_occupied == 1:
        #         turtle.tracer(False)
        #         C.testing_turtle.goto(i.loc)
        #         C.testing_turtle.color('Blue')
        #         C.testing_turtle.dot(10)
        #         turtle.tracer(True)

        #Redraw All the Tiles
        #print('Drawing ', turns)
        #time.sleep(4)
        Game.draw()
        #print('Drawed ', turns)

            # print(str(team_mat[turns % 2].team) + ' Wins')
            # print('The Other Teams Queen is surrounded')
            # print('Player 1 wins in ' + str(turns) + ' moves')
            # C.main_turtle.goto(0,0)
            # C.main_turtle.color('red')

            # if team_mat[turns % 2].is_human == 1:
            #     C.main_turtle.write("You Win!", False, align="center", font=("Arial", 100, "normal"))
            # elif team_mat[turns % 2].is_human == 0:
            #     C.main_turtle.write("You Lose!", False, align="center", font=("Arial", 100, "normal"))

            # break



main()    
print('End')
C.wn.exitonclick()