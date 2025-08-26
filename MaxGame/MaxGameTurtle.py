from turtle import *



writer = Turtle()
writer.hideturtle()
writer.up()

grid_width = 40
grid_height = 40
cell_size = 25 # pixels (default is 100)
x_margin = cell_size * 2.5 # pixels, the size of the margin left/right of the grid
y_margin = cell_size // 2 # pixels, the size of the margin below/above the grid
window_grid_height = grid_height * cell_size + y_margin * 2
window_grid_width = grid_width * cell_size + x_margin * 2

def main():

    [size_of_screen, map_square_size] = setupmapscreen()

def setupmapscreen():
    size_of_screen = 230
    map_square_size = size_of_screen * 2 / 5
    repeats = size_of_screen * 2 / map_square_size + 1
    repeats = int(repeats)
    tracer(False)
    for i in range(repeats):
        location_spot = -size_of_screen + map_square_size * i
        writer.setposition(location_spot, size_of_screen)
        writer.down()
        writer.setposition(location_spot, -size_of_screen)
        writer.up()
        writer.setposition(-size_of_screen, location_spot)
        writer.down()
        writer.setposition(size_of_screen, location_spot)
        writer.up()
    #player_map.showturtle()
    tracer(True)
    return size_of_screen, map_square_size



main()

print("Finished")