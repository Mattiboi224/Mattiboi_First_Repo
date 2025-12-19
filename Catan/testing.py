from player import Player as P
import Config as C
import random

# Create Teams
TEAM_1 = P(C.TEAM_1_COLOUR, 'TEAM_1', 1)
TEAM_2 = P(C.TEAM_2_COLOUR, 'TEAM_2', 1)
TEAM_3 = P(C.TEAM_3_COLOUR, 'TEAM_3', 1)

team_mat = []

# Team LIST
team_mat.append(TEAM_1)
team_mat.append(TEAM_2)
team_mat.append(TEAM_3)

curr_team = team_mat[0]

original_x = -300
original_y = 300

C.announcer_turtle.clear()

C.announcer_turtle.color('Black')
C.announcer_turtle.goto(original_x, original_y)
C.announcer_turtle.write('Statistics', False, align="left", font=("Arial", 20, "bold"))

C.announcer_turtle.goto(original_x, original_y - 20)
C.announcer_turtle.write('Victory Points', False, align="left", font=("Arial", 15, "bold"))

count = original_y  - 40
for i in team_mat:
    label = str(i.team) + ' = ' + str(i.current_points)

    C.announcer_turtle.color(i.colour)
    C.announcer_turtle.goto(original_x, count)
    C.announcer_turtle.write(label, False, align="left", font=("Arial", 10, "normal"))
    count -= 20

C.announcer_turtle.color('Black')
C.announcer_turtle.goto(original_x, original_y - 120)
C.announcer_turtle.write('Cards in Deck: ' + str(len(C.DEVELOPMENT_CARD_DECK)), False, align="left", font=("Arial", 15, "bold"))


C.announcer_turtle.color('Black')
C.announcer_turtle.goto(original_x, original_y - 150)
C.announcer_turtle.write('Avaliable Pieces', False, align="left", font=("Arial", 15, "bold"))

C.announcer_turtle.color(curr_team.colour)
C.announcer_turtle.goto(original_x, original_y - 165)
C.announcer_turtle.write('Roads: ' + str(curr_team.avaliable_road_pieces), False, align="left", font=("Arial", 10, "normal"))

C.announcer_turtle.goto(original_x, original_y - 180)
C.announcer_turtle.write('Settlements: ' + str(curr_team.avaliable_settlement_pieces), False, align="left", font=("Arial", 10, "normal"))

C.announcer_turtle.goto(original_x, original_y - 195)
C.announcer_turtle.write('Cities: ' + str(curr_team.avaliable_city_pieces), False, align="left", font=("Arial", 10, "normal"))


C.announcer_turtle.color('Black')
C.announcer_turtle.goto(original_x, original_y - 220)
C.announcer_turtle.write('Resources in Hand: ' + str(len(curr_team.resources)), False, align="left", font=("Arial", 15, "bold"))

C.announcer_turtle.color(curr_team.colour)
C.announcer_turtle.goto(original_x, original_y - 235)
C.announcer_turtle.write('Wood: ' + str(curr_team.resources.count('Wood')), False, align="left", font=("Arial", 10, "normal"))

C.announcer_turtle.goto(original_x, original_y - 250)
C.announcer_turtle.write('Brick: ' + str(curr_team.resources.count('Brick')), False, align="left", font=("Arial", 10, "normal"))

C.announcer_turtle.goto(original_x, original_y - 265)
C.announcer_turtle.write('Wheat: ' + str(curr_team.resources.count('Wheat')), False, align="left", font=("Arial", 10, "normal"))

C.announcer_turtle.goto(original_x, original_y - 280)
C.announcer_turtle.write('Sheep: ' + str(curr_team.resources.count('Sheep')), False, align="left", font=("Arial", 10, "normal"))

C.announcer_turtle.goto(original_x, original_y - 295)
C.announcer_turtle.write('Stone: ' + str(curr_team.resources.count('Stone')), False, align="left", font=("Arial", 10, "normal"))



if len(curr_team.cards) > 0:
    C.announcer_turtle.color('Black')
    C.announcer_turtle.goto(original_x, original_y - 325)
    C.announcer_turtle.write('Cards in Hand', False, align="left", font=("Arial", 15, "bold"))

    C.announcer_turtle.color(curr_team.colour)
    if curr_team.cards.count('Knight') > 0:
        C.announcer_turtle.goto(original_x, original_y - 340)
        C.announcer_turtle.write('Knight: ' + str(curr_team.cards.count('Knight')), False, align="left", font=("Arial", 10, "normal"))

    if curr_team.cards.count('VP') > 0:
        C.announcer_turtle.goto(original_x, original_y - 355)
        C.announcer_turtle.write('VP: ' + str(curr_team.cards.count('VP')), False, align="left", font=("Arial", 10, "normal"))

    if curr_team.cards.count('Monopoly') > 0:
        C.announcer_turtle.goto(original_x, original_y - 370)
        C.announcer_turtle.write('Monopoly: ' + str(curr_team.cards.count('Monopoly')), False, align="left", font=("Arial", 10, "normal"))

    if curr_team.cards.count('Road Building') > 0:
        C.announcer_turtle.goto(original_x, original_y - 385)
        C.announcer_turtle.write('Road Building: ' + str(curr_team.cards.count('Road Building')), False, align="left", font=("Arial", 10, "normal"))

    if curr_team.cards.count('Year of Plenty') > 0:
        C.announcer_turtle.goto(original_x, original_y - 400)
        C.announcer_turtle.write('Year of Plenty: ' + str(curr_team.cards.count('Year of Plenty')), False, align="left", font=("Arial", 10, "normal"))


C.wn.exitonclick()