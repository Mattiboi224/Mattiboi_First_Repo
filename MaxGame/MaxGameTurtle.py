from turtle import *
import random

TURTLE_SIZE = 20
screen = Screen()
writer = Turtle()

#writer.shape("square")
a = writer.shapesize()

print(a)

writer.resizemode("user")
writer.shapesize(0.1, 0.1)
b = writer.shapesize()

print(b)

writer.hideturtle()
#writer.showturtle()
writer.up()
#writer.goto(TURTLE_SIZE/2-screen.window_width()/2, screen.window_height()/2 - TURTLE_SIZE/2)

#screensize(830,830)
window_width = 800
window_height = 800
margin = 2
screen.screensize(  # despite the name, screensize() does not change window/screen's size
    canvwidth=window_width - margin,  # named parameters give a hint of method's real goal
    canvheight=window_height - margin)  # canvas has to be smaller than window
screen.setup(window_width, window_height)  # setup() will change window/screen's size

screen.setworldcoordinates(0,805,805,0)


screen_width = 800
screen_height = 800
no_of_grid_width = 40
no_of_grid_height = 40
#cell_size = 10 # pixels (default is 100)
x_pixel_size = screen_width/no_of_grid_width # pixels, the size of the margin left/right of the grid
y_pixel_size = screen_height/no_of_grid_height # pixels, the size of the margin below/above the grid

stamp_ids = []

tracer(False)




class GridMap:
    def __init__(self, screen_width, screen_height):
        self.w = screen_width
        self.h = screen_height

    def draw(self):

        tracer(False)


        for i in range(0,no_of_grid_width + 1):
            writer.setposition(i * x_pixel_size,0)
            writer.down()
            writer.setposition(i * x_pixel_size, 800)
            writer.up()

        for i in range(0,no_of_grid_height + 1):
            writer.setposition(0, i * y_pixel_size)
            writer.down()
            writer.setposition(800,i * y_pixel_size)
            writer.up()

        stamp_ids.append(writer.stamp())

    def assign_tiles(self):

        tiles_list = []
        
        for i in range(0, no_of_grid_height):
            for j in range (0, no_of_grid_width):
                x_centre = i * x_pixel_size + x_pixel_size / 2
                y_centre = j * y_pixel_size + y_pixel_size / 2

                tiles_list.append(Tiles(x_centre, y_centre, "land", i + 1, j + 1))

        return tiles_list
    



class Tiles():

    count = 0

    def __init__ (self, x_centre, y_centre, land_type, x_cord, y_cord):
        self.placeholder = 0
        self.x_centre = x_centre
        self.y_centre = y_centre
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.tl_x_cord = x_centre - x_pixel_size / 2
        self.tl_y_cord = y_centre - y_pixel_size / 2
        self.land_type = land_type
        Tiles.count += 1
        
        if land_type == 'water':
            self.land_movable = 0
            self.water_movable = 1

        elif land_type == 'land':
            self.land_movable = 1
            self.water_movable = 0

        else:
            self.land_movable = 0
            self.water_movable = 0



        


    def assign_resources(self, resource_type):
        
        for i in range(5):
            resource_type = random.randrange(0,1999)
        
Grid = GridMap(screen_width, screen_height)

Grid.draw()
tiles_name = Grid.assign_tiles()


        

tracer(True)

for i in range(len(tiles_name)):
    instance = tiles_name[i]

    tracer(False)

    if i == 2:
        print(len(stamp_ids))
        print((no_of_grid_width * no_of_grid_height) + 1)

    if instance.land_type == "land":

        writer.goto(instance.tl_x_cord, instance.tl_y_cord)
        writer.pendown()
        writer.fillcolor("green")
        writer.begin_fill()
        
        #Draw Border
        writer.setheading(90)
        writer.forward(x_pixel_size)
        writer.setheading(0)
        writer.forward(y_pixel_size)
        writer.setheading(270)
        writer.forward(x_pixel_size)
        writer.setheading(180)
        writer.forward(y_pixel_size)
        
        #Fill it
        writer.end_fill()
        writer.penup()

        if len(stamp_ids) >= 1 and len(stamp_ids) < (no_of_grid_width * no_of_grid_height) + 1:

            stamp_ids.append(writer.stamp())


print(len(stamp_ids))

writer.clearstamp(stamp_ids[3])
        

        



'''
def main():

    map_square_size = setupmapscreen(window_grid_height, window_grid_width, cell_size)

def setupmapscreen(window_grid_height, window_grid_width, cell_size):
    
    

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
    return map_square_size



main()
'''

screen.mainloop()

print("Finished")

