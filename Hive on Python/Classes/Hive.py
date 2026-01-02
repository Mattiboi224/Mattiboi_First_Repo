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

team_1 = P('TEAM_1', C.team0, 0)
team_2 = P('TEAM_2', C.team1, 0)

team_mat = []

team_mat.append(team_1)
team_mat.append(team_2)

def main():

    Game = G()

    Game.board.draw_board(team_mat[1].colour, -390, 400, team_mat[1].text)
    Game.board.draw_board(team_mat[0].colour, 240, 400, team_mat[0].text)

    for turns in range(50):

        y_positions = [385, 370, 355, 340, 325]
        insect_types = ['Queen', 'Ant', 'Grasshopper', 'Spider', 'Beetle']

        # Clear the announcer
        C.announcer_turtle.clear()

        # Announce for player 2
        Game.announce_remaining_insects(team_mat[1], [-283, -292, -242, -278, -278], y_positions)

        # Announce for player 1
        Game.announce_remaining_insects(team_mat[0], [385] * len(insect_types), y_positions)
        
        human = team_mat[turns % 2].is_human

        if human == 1:
            Game.Human_Player(team_mat[turns % 2], turns)

        elif human == 0:
            original_bug_class, bug_class_mat = Game.avaliable_moves(team_mat[turns % 2], turns, Game.all_bugs_class)

            # Starting with Random Number Generator
            Game.ai_random_number_generator(team_mat[turns % 2], original_bug_class, bug_class_mat, Game.all_bugs_class)


        #Redraw All the Tiles
        Game.draw()

        if Game.is_win(team_mat[turns % 2]):

            print(str(team_mat[turns % 2].team) + ' Wins')
            print('The Other Teams Queen is surrounded')
            print('Player 1 wins in ' + str(turns) + ' moves')
            C.main_turtle.goto(0,0)
            C.main_turtle.color('red')

            if team_mat[turns % 2].is_human == 1:
                C.main_turtle.write("You Win!", False, align="center", font=("Arial", 100, "normal"))
            elif team_mat[turns % 2].is_human == 0:
                C.main_turtle.write("You Lose!", False, align="center", font=("Arial", 100, "normal"))

            break



main()    
print('End')
C.wn.exitonclick()