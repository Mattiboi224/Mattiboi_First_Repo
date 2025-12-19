import turtle

# Constants
total_ant = 3
total_grasshopper = 3
total_beetle = 2
total_spider = 2
total_queen = 1
side_length = 40
num_sides = 6
angle = 360.0 / num_sides

# Initialize the screen and main turtle
wn = turtle.Screen()
wn.setup(1200,900)
main_turtle = turtle.Turtle()
main_turtle.hideturtle()
board_turtle = turtle.Turtle()
board_turtle.hideturtle()
selection_turtle = turtle.Turtle()
selection_turtle.hideturtle()
move_place_turtle = turtle.Turtle()
move_place_turtle.hideturtle()
announcer_turtle = turtle.Turtle()
announcer_turtle.hideturtle()

# Putting Everything Up
main_turtle.up()
board_turtle.up()
move_place_turtle.up()
selection_turtle.up()
announcer_turtle.up()

# Team Colours
team0 = 'green'
team1 = 'red'