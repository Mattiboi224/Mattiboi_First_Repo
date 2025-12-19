import turtle
import Config as C

class Corner:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_occupied = 0
        self.nearby_corners_mat = []
        self.nearby_corners_mat_class = []
        self.nearby_tiles = []
        self.nearby_roads_mat = []
        self.building = None
        self.team = None
        self.radius = 10

    def pos(self):
        return [self.x, self.y]



    def nearby_corners(self, Tiles_mat):
        
        for i in Tiles_mat:
            if [self.x, self.y] in i.corner_mat:

                self.nearby_tiles.append(i)

                middle_index = i.corner_mat.index([self.x, self.y])

                if i.corner_mat[middle_index - 1] not in self.nearby_corners_mat:
                    self.nearby_corners_mat.append(i.corner_mat[middle_index - 1])

                if middle_index + 1 == len(i.corner_mat):
                    second_val = 0
                else:
                    second_val = middle_index + 1

                if i.corner_mat[second_val] not in self.nearby_corners_mat:
                    self.nearby_corners_mat.append(i.corner_mat[second_val])
        
        self.nearby_roads_mat = []

        for i in range(len(self.nearby_corners_mat)):
            self.nearby_roads_mat.append([self.nearby_corners_mat[i-1], [self.nearby_corners_mat[i]]])

    def draw(self, team_colour):

        #print(team_colour)
        #print(self.building)
        #print(self.x)
        #print(self.y)
        
        # Draw a rectangle
        if self.building == 'Settlement':
            turtle.tracer(False)
            C.main_turtle.pencolor('Black')
            C.main_turtle.fillcolor(team_colour)

            C.main_turtle.up()
                        
            C.main_turtle.goto(self.x - 10, self.y - 10)
            C.main_turtle.right(C.main_turtle.heading())

            C.main_turtle.down()
            C.main_turtle.begin_fill()

            for _ in range(2):
                C.main_turtle.forward(20)
                C.main_turtle.left(90)
                C.main_turtle.forward(20)
                C.main_turtle.left(90)

            C.main_turtle.end_fill()
            C.main_turtle.up()
            turtle.tracer(True)

        # Draw a rectangle
        elif self.building == 'City':
            turtle.tracer(False)
            C.main_turtle.up()
            C.main_turtle.goto(self.x, self.y)
            C.main_turtle.pencolor(team_colour)
            C.main_turtle.dot(20)


    def draw_midpoint(self):

        C.main_turtle.pencolor('Black')
        C.main_turtle.goto(self.x, self.y)
        C.main_turtle.dot(12)
