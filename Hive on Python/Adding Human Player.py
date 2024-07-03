import turtle
import random
import sys
import signal
from collections import deque
import time
import math

wn = turtle.Screen()
main_turtle = turtle.Turtle()
total_ant = 3
total_grasshopper = 3
total_beetle = 2
total_spider = 2
total_queen = 1
side_length = 40
num_sides = 6
angle = 360.0 / num_sides
main_turtle.hideturtle()
##print(angle)

def hexagon_shape (position_x, position_y):
    
    turtle.tracer(False)
    # Start Location to Start of Hexagon
    main_turtle.color('black')
    main_turtle.goto(position_x, position_y)
    main_turtle.right(main_turtle.heading())
    main_turtle.up()
    main_turtle.left(angle * 2)
    main_turtle.forward(side_length)
    #main_turtle.right(angle * 2)
    main_turtle.right(main_turtle.heading())
    main_turtle.down()

    # Draw Hexagon
    for i in range(num_sides):
        main_turtle.forward(side_length)
        main_turtle.right(angle)

    # Back to Start Location
    main_turtle.up()
    main_turtle.right(angle)
    main_turtle.forward(side_length)
    main_turtle.left(angle)

    main_turtle.goto(position_x, position_y)
    main_turtle.right(main_turtle.heading())
    turtle.tracer(True)

def getlocations(posx, posy):
    avaliable_position = []
    
    for i in range(6):
        turtle.tracer(False)
        main_turtle.goto(posx, posy)
        main_turtle.setheading(0)
        main_turtle.up()
        main_turtle.left(150 - 60 * i)
        main_turtle.forward(side_length * math.sqrt(3))
        main_turtle.right(150)
        main_turtle.setheading(0)
        xpos = main_turtle.xcor()
        ypos = main_turtle.ycor()
        avaliable_position.append([round(xpos,3), round(ypos,3)])
        turtle.tracer(True)
    
    return avaliable_position

hexagon_shape(0,0)

def build_the_board():  ##(start, filled_close_pos_mat, current_tile, current_tile_mat, close_pos_mat):
    turtle.tracer(False)
    # Get everything that is around
    position = getlocations(0,0)
    
    position = [tuple(inner_list) for inner_list in position]
    
    visited = set()
    queue = [(0,0)]
    
    for i in range(len(position)):
        queue.append(position[i])

    #`print(queue)
    queue = deque(queue)
    final_loc = []


    
    while queue:
        current = queue.popleft()
        #print(current)

        if current in visited:
            continue

        hexagon_shape(current[0], current[1])
        final_loc.append([current[0], current[1]])
        
        visited.add(current)
        
        neighbors = getlocations(current[0], current[1])
        neighbors = [tuple(inner_list) for inner_list in neighbors]

        for i in range(len(neighbors)):
            #print(neighbors[i])
            if neighbors[i] not in visited:
                queue.append(neighbors[i])


        if len(final_loc) == 91:
            break
    turtle.tracer(True)
    return final_loc

def place_tile (x, y):

    global close_position, running
    
    pos_points = []

    # Find the nearest coordinate
    for i in range(len(all_locs)):
        dist = math.sqrt((x - all_locs[i][0])**2 + (y - all_locs[i][1])**2)
        pos_points.append(dist)

    min_pos_points = min(pos_points)

    index = [i for i, x in enumerate(pos_points) if x == min_pos_points]

    close_position = all_locs[index[0]]

    running = True
        
global all_locs, running, close_position
running = False
close_position = None
all_locs = build_the_board()



turtle.onscreenclick(place_tile)

while not running:

    wn.update()


print(close_position)

main_turtle.up()
main_turtle.goto(close_position[0], close_position[1])
main_turtle.dot(10, "Red")
