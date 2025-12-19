import turtle
import math
from collections import deque
import random
import Config as C


# Draw a hexagon
def hexagon_shape(position_x, position_y, sel_turtle, colour, side_length, fill_on_off, big_hex):

    if sel_turtle == 'Main':
        turtle.tracer(False)
        # Start Location to Start of Hexagon
        C.main_turtle.color(colour)
        C.main_turtle.goto(position_x, position_y)
        C.main_turtle.right(C.main_turtle.heading())
        C.main_turtle.up()
        C.main_turtle.left(C.angle * 2)
        C.main_turtle.forward(side_length)
        #main_turtle.right(angle * 2)
        C.main_turtle.right(C.main_turtle.heading())
        C.main_turtle.down()

        # Draw Hexagon
        for i in range(C.num_sides):
            C.main_turtle.forward(side_length)
            C.main_turtle.right(C.angle)

        # Back to Start Location
        C.main_turtle.up()
        C.main_turtle.right(C.angle)
        C.main_turtle.forward(side_length)
        C.main_turtle.left(C.angle)

        C.main_turtle.goto(position_x, position_y)
        C.main_turtle.right(C.main_turtle.heading())
        turtle.tracer(True)

    if sel_turtle == 'Board':
        turtle.tracer(False)
        # Start Location to Start of Hexagon

        C.board_turtle.pencolor('Black')
        C.board_turtle.fillcolor(colour)
        C.board_turtle.goto(position_x, position_y)
        C.board_turtle.right(C.board_turtle.heading())
        C.board_turtle.up()

        if big_hex == 'No':
            C.board_turtle.left(C.angle * 2)

        if big_hex == 'Yes':
            C.board_turtle.left(90)

        C.board_turtle.forward(side_length)
        #main_turtle.right(angle * 2)
        C.board_turtle.right(C.board_turtle.heading())
        
        if big_hex == 'Yes':
            C.board_turtle.right(30)

        C.board_turtle.down()

        # Draw Hexagon

        if fill_on_off == 'On':
            C.board_turtle.begin_fill()

        for i in range(C.num_sides):
            C.board_turtle.forward(side_length)
            C.board_turtle.right(C.angle)

        if fill_on_off == 'On':
            C.board_turtle.end_fill()

        # Back to Start Location
        C.board_turtle.up()
        C.board_turtle.right(C.angle)
        C.board_turtle.forward(side_length)
        C.board_turtle.left(C.angle)

        C.board_turtle.goto(position_x, position_y)
        C.board_turtle.right(C.board_turtle.heading())
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

def get_corners(posx, posy, sel_turtle):
    if sel_turtle == 'Main':
        turtle.tracer(False)
        # Start Location to Start of Hexagon
        C.main_turtle.color('Black')
        C.main_turtle.goto(posx, posy)
        C.main_turtle.right(C.main_turtle.heading())
        C.main_turtle.up()
        C.main_turtle.left(C.angle * 2)
        C.main_turtle.forward(C.side_length)
        #main_turtle.right(angle * 2)
        C.main_turtle.right(C.main_turtle.heading())
        C.main_turtle.down()

        corner_mat = []

        # Draw Hexagon
        C.main_turtle.begin_fill()
        for i in range(C.num_sides):
            xpos = C.main_turtle.xcor()
            ypos = C.main_turtle.ycor()
            corner_mat.append([round(xpos,3), round(ypos,3)])
            C.main_turtle.forward(C.side_length)
            C.main_turtle.right(C.angle)

        C.main_turtle.end_fill()

        return corner_mat


def dist(a, b):
    return math.hypot(a[0]-b[0], a[1]-b[1])


def rectangle_shape(x, y, w, h, sel_turtle, fill='No', colour ='black'):
    if sel_turtle == 'Selection':
    
        turtle.tracer(False)
        
        if colour == 'Red':
            C.selection_turtle.fillcolor('red')
            C.selection_turtle.pencolor('red')

        C.selection_turtle.up()
        C.selection_turtle.goto(x, y)
        C.selection_turtle.right(C.selection_turtle.heading())
        C.selection_turtle.down()

        if fill != 'No':
            C.selection_turtle.begin_fill()
        for _ in range(2):
            C.selection_turtle.forward(w)
            C.selection_turtle.right(90)
            C.selection_turtle.forward(h)
            C.selection_turtle.right(90)
        
        if fill != 'No':
            C.selection_turtle.end_fill()

        if colour == 'Red':
            C.selection_turtle.fillcolor('black')
            C.selection_turtle.pencolor('black')

        C.selection_turtle.up()
        
        turtle.tracer(True)

def write_text(label, x, y, w, h, width):
    turtle.tracer(False)
    for a in range(len(label)):
        C.selection_turtle.goto(x + w/2, y - width + a * - 40)
        C.selection_turtle.write(label[a], False, align="center", font=("Arial", 20, "normal"))
    turtle.tracer(True)    


def selection(x, y):
    
    # Road
    if x >= 290 and x <= 460 and y <= 350 and y >= 350 - 115 and C.road_check == 1:
        C.selecting_on_screen = True
        C.selecting_type = 'Road'

    # Settlement
    elif x >= 290 and x <= 460 and y <= 210 and y >= 210 - 115 and C.settlement_check == 1:
        C.selecting_on_screen = True
        C.selecting_type = 'Settlement'

    # City
    elif x >= 290 and x <= 460 and y <= 70 and y >= 70 - 115 and C.city_check == 1:
        C.selecting_on_screen = True
        C.selecting_type = 'City'

    # Development Card
    elif x >= 290 and x <= 460 and y <= -70 and y >= -70 - 115 and C.development_card_check == 1:
        C.selecting_on_screen = True
        C.selecting_type = 'Development Card'

    # Development Card
    elif x >= 290 and x <= 460 and y <= -210 and y >= -210 - 115 and C.card_check == 1:
        C.selecting_on_screen = True
        C.selecting_type = 'Play Card'

    # End Turn
    elif x >= -450 and x <= -450 + 170 and y <= -250 and y >= -250 - 125:
        C.selecting_on_screen = True
        C.selecting_type = 'End Turn'

    else:
        print('Invalid Click')
        C.selecting_on_screen = False

def card_selection(x, y):
    
    # Knight
    if x >= -230 and x <= -230 + 100 and y <= -250 and y >= -250 - 125 and C.knight_check == 1:
        C.selecting_on_screen = True
        C.selecting_type = 'Knight'

    # Monopoly
    elif x >= -105 and x <= -105 + 100 and y <= -250 and y >= -250 - 125 and C.monopoly_check == 1:
        C.selecting_on_screen = True
        C.selecting_type = 'Monopoly'

    # Road Building
    elif x >= 20 and x <= 20 + 100 and y <= -250 and y >= -250 - 125 and C.road_building_check == 1:
        C.selecting_on_screen = True
        C.selecting_type = 'Road Building'

    # Year of Plenty
    elif x >= 145 and x <= 145 + 100 and y <= -250 and y >= -250 - 125 and C.year_of_plenty_check == 1:
        C.selecting_on_screen = True
        C.selecting_type = 'Year of Plenty'

    # End Turn
    elif x >= -450 and x <= -450 + 170 and y <= -250 and y >= -250 - 125:
        C.selecting_on_screen = True
        C.selecting_type = 'End Turn'

    else:
        print('Invalid Click')
        C.selecting_on_screen = False

def resource_selection(x, y):
    
    # Wood
    if x >= -400 and x <= -400 + 100 and y <= 350 and y >= 350 - 50:
        C.selecting_on_screen = True
        C.selecting_type = 'Wood'

    # Brick
    elif x >= -375 and x <= -375 + 100 and y <= 350 and y >= 350 - 50:
        C.selecting_on_screen = True
        C.selecting_type = 'Brick'

    # Wheat
    elif x >= -250 and x <= -250 + 100 and y <= 350 and y >= 350 - 50:
        C.selecting_on_screen = True
        C.selecting_type = 'Wheat'

    # Sheep
    elif x >= -125 and x <= -125 + 100 and y <= 350 and y >= 350 - 50:
        C.selecting_on_screen = True
        C.selecting_type = 'Sheep'

    # Stone
    elif x >= 0 and x <= 0 + 100 and y <= 350 and y >= 350 - 50:
        C.selecting_on_screen = True
        C.selecting_type = 'Stone'

    # End Turn
    elif x >= -450 and x <= -450 + 170 and y <= -250 and y >= -250 - 125:
        C.selecting_on_screen = True
        C.selecting_type = 'End Turn'

    else:
        print('Invalid Click')
        C.selecting_on_screen = False