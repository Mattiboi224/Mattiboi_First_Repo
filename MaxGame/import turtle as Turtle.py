import turtle as Turtle

grid_width = 5
grid_height = 5
cell_size = 50 # pixels (default is 100)
x_margin = cell_size * 2.5 # pixels, the size of the margin left/right of the grid
y_margin = cell_size // 2 # pixels, the size of the margin below/above the grid
window_grid_height = grid_height * cell_size + y_margin * 2
window_grid_width = grid_width * cell_size + x_margin * 2

def main():

    setupmapscreen(label_spaces = False)

def setupmapscreen(bg_colour = 'light grey',
                          line_colour = 'slate grey',
                          draw_grid = True,
                          label_spaces = True): # NO! DON'T CHANGE THIS!
    
    # Set up the drawing canvas with enough space for the grid and
    # spaces on either side
    Turtle.setup(window_grid_width, window_grid_height)
    Turtle.bgcolor(bg_colour)

    # Draw as quickly as possible
    Turtle.tracer(False)

    # Get ready to draw the grid
    Turtle.penup()
    Turtle.color(line_colour)
    Turtle.width(2)

    # Determine the left-bottom coords of the grid
    left_edge = -(grid_width * cell_size) // 2 
    bottom_edge = -(grid_height * cell_size) // 2

    # Optionally draw the grid
    if draw_grid:

        # Draw the horizontal grid lines
        Turtle.setheading(0) # face east
        for line_no in range(0, grid_height + 1):
            Turtle.penup()
            Turtle.goto(left_edge, bottom_edge + line_no * cell_size)
            Turtle.pendown()
            Turtle.forward(grid_width * cell_size)
            #print(pos())
            
        # Draw the vertical grid lines
        Turtle.setheading(90) # face north
        for line_no in range(0, grid_width + 1):
            Turtle.penup()
            Turtle.goto(left_edge + line_no * cell_size, bottom_edge)
            Turtle.pendown()
            Turtle.forward(grid_height * cell_size)
            #print(pos())
    #print(pos())
    Turtle.penup()
    Turtle.tracer(True)

main()