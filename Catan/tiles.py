import util as m
import Config as C
import turtle

class Tiles:

    count_wood = 0
    count_brick = 0
    count_wheat = 0
    count_stone = 0
    count_sheep = 0

    def __init__(self, x, y, tile_type, number):
        self.x = x
        self.y = y
        self.close_tiles = m.getlocations(self.x, self.y)
        self.tile_type = tile_type
        self.number = number
        self.colour = None
        self.corner_mat = m.get_corners(self.x, self.y, 'Main')
        self.corner_mat_class = []
        self.is_robber = 0
        self.radius = 12

        if tile_type == 'Wood':
            Tiles.count_wood += 1
            self.colour = 'Green'
        elif tile_type == 'Brick':
            Tiles.count_brick += 1
            self.colour = 'Red'
        elif tile_type == 'Wheat':
            Tiles.count_wheat += 1
            self.colour = 'Orange'
        elif tile_type == 'Stone':
            Tiles.count_stone += 1
            self.colour = 'Grey'
        elif tile_type == 'Sheep':
            Tiles.count_sheep += 1
            self.colour = 'Cyan'
        elif tile_type == 'Sand':
            self.colour = 'Yellow'

    def pos(self):
        return [self.x, self.y]

    def draw(self, turtle_type):

        if self.number >= 0:
            m.hexagon_shape(self.x, self.y, turtle_type, self.colour, C.side_length, 'On', 'No')

            self.draw_number()

        else:
            m.draw_shipping(self.x, self.y, self.number, self.tile_type)

    def draw_number(self):

        turtle.tracer(False)

        C.number_turtle.goto(self.x, self.y)

        if self.number not in (0, 6, 8):
            C.number_turtle.dot(30,"White")
            C.number_turtle.goto(self.x, self.y-8)
            C.number_turtle.color('Black')
            C.number_turtle.write(self.number, False, align="center", font=("Arial", 10, "normal"))

        elif self.number in (6, 8):
            C.number_turtle.dot(30,"White")
            C.number_turtle.color('Red')
            C.number_turtle.goto(self.x, self.y-8)
            C.number_turtle.write(self.number, False, align="center", font=("Arial", 10, "normal"))

        elif self.number == 0:
            C.number_turtle.dot(30,"Grey")

        turtle.tracer(True)