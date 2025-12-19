import turtle
import Config as C

class Road:
    def __init__(self, road_value):

        if road_value[0][0] == -0.0:
            road_value[0][0] = 0.0

        if road_value[0][1] == -0.0:
            road_value[0][1] = 0.0

        if road_value[1][0] == -0.0:
            road_value[1][0] = 0.0

        if road_value[1][1] == -0.0:
            road_value[1][1] = 0.0

        self.x1 = road_value[0][0]
        self.y1 = road_value[0][1]
        self.p1 = [self.x1, self.y1]
        self.x2 = road_value[1][0]
        self.y2 = road_value[1][1]
        self.p2 = [self.x2, self.y2]
        self.nearby_corners_mat = [self.p1, self.p2]
        self.nearby_roads_mat_class = []
        self.nearby_corners_mat_class = []

        # Midpoint of the road
        self.x = (self.x1 + self.x2) / 2
        self.y = (self.y1 + self.y2) / 2

        self.is_occupied = 0
        self.team = None
        self.radius = 15

    def pos(self):
        return [self.x, self.y]

    def nearby_roads(self, roads_mat_class):

        for i in roads_mat_class:

            # If the corners exist in any of the roads + remove itself
            if (self.p1 == i.p1 or self.p1 == i.p2 or self.p2 == i.p1 or self.p2 == i.p2) and not (self.p1 == i.p1 and self.p2 == i.p2):
                self.nearby_roads_mat_class.append(i)

            # if self.p1 == [-20.0, 103.923] and self.p2 == [20.0, 103.923]:
            #     #print(self.p1, self.p2)
            #     #print(i.p1, i.p2)

            #     if self.p1 == i.p1 or self.p1 == i.p2 or self.p2 == i.p1 or self.p2 == i.p2:
            #         print('Pass')
            #         print(self.p1, self.p2)
            #         print(i.p1, i.p2)

            #         if not (self.p1 == i.p1 and self.p2 == i.p2):
            #             print('Failed')
            #             print(self.p1 == i.p1, self.p1 == i.p2, self.p2 == i.p1, self.p2 == i.p2)

                #print(self.p1 == i.p1, self.p1 == i.p2, self.p2 == i.p1, self.p2 == i.p2)

        # if self.p1 == [-20.0, 103.923] and self.p2 == [20.0, 103.923]:

        #     print(self.p1, self.p2)
            

        #     for i in self.nearby_roads_mat_class:
        #         print('nearby_points ', i.p1, i.p2)
        #         i.draw_midpoint()


    def nearby_corners(self, corners_mat_class):

        for i in corners_mat_class:
            if (i.x == self.x1 and i.y == self.y1) or (i.x == self.x2 and i.y == self.y2):
                self.nearby_corners_mat_class.append(i)


    def draw(self, team_colour):

        turtle.tracer(False)
        C.main_turtle.pencolor(team_colour)
        
        C.main_turtle.width(10)
        C.main_turtle.up()
        C.main_turtle.goto(self.x1, self.y1)
        C.main_turtle.down()
        C.main_turtle.goto(self.x2, self.y2)
        C.main_turtle.up()

        C.main_turtle.width(1)

        turtle.tracer(True)

    def draw_midpoint(self):

        C.main_turtle.pencolor('Black')
        C.main_turtle.goto(self.x, self.y)
        C.main_turtle.dot(12)
