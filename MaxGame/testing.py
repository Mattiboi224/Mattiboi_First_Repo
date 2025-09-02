from turtle import *
import random

screen = Screen()
writer = Turtle()

screen_width = 800
screen_height = 800
no_of_grid_width = 40
no_of_grid_height = 40
#cell_size = 10 # pixels (default is 100)
x_pixel_size = screen_width/no_of_grid_width # pixels, the size of the margin left/right of the grid
y_pixel_size = screen_height/no_of_grid_height # pixels, the size of the margin below/above the grid

#screensize(830,830)
window_width = 800
window_height = 800
margin = 2
screen.screensize(  # despite the name, screensize() does not change window/screen's size
    canvwidth=window_width - margin,  # named parameters give a hint of method's real goal
    canvheight=window_height - margin)  # canvas has to be smaller than window
screen.setup(window_width, window_height)  # setup() will change window/screen's size

screen.setworldcoordinates(0,805,805,0)


stamp_ids = []

tracer(False)

for i in range(0,no_of_grid_width + 1):
    writer.setposition(i * x_pixel_size,0)
    writer.down()
    writer.setposition(i * x_pixel_size, 800)
    writer.up()

    stamp_ids.append(writer.stamp())


for i in range(0,no_of_grid_height + 1):
    writer.setposition(0, i * y_pixel_size)
    writer.down()
    writer.setposition(800,i * y_pixel_size)
    writer.up()

    if i >= 38:
        tracer(True)

    stamp_ids.append(writer.stamp())


print(stamp_ids)

writer.clearstamp(stamp_ids[3])

screen.mainloop()