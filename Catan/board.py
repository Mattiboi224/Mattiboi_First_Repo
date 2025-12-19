import turtle
import util as m
from collections import deque
import Config as C
from tiles import Tiles as Ti
from corner import Corner as Co
from road import Road as R
import random

class Board():
    def __init__(self):
        self.ava_numbers = C.NUMBER
        self.Tiles_Mat = []
        self.corner_mat_class = []
        self.road_mat_class = []

        self.build_the_border()
        self.all_locs = self.build_the_board()
        self.assign_corners()
        self.give_tile_mat()
        self.give_corner_mat()

        
        

    # Build the board
    def build_the_board(self):
        turtle.tracer(False)
        position = m.getlocations(0, 0)
        position = [tuple(inner_list) for inner_list in position]
        
        visited = set()
        queue = deque([(0, 0)] + position)
        
        final_loc = []
        Tiles_Mat = []
        
        while queue:
            current = queue.popleft()
            
            if current in visited:
                continue
            
            
            final_loc.append([current[0], current[1]])
            
            if current[0] == 0 and current[1] == 0:
                tile_type = 'Sand'
            else:
                counter = 0
                while counter == 0:
                    var = random.randint(0,4)
                    if var == 0 and Ti.count_wood != C.TOTAL_WOOD:
                        tile_type = 'Wood'
                        break
                    elif var == 1 and Ti.count_brick != C.TOTAL_BRICK:
                        tile_type = 'Brick' 
                        break
                    elif var == 2 and Ti.count_wheat != C.TOTAL_WHEAT:
                        tile_type = 'Wheat' 
                        break
                    elif var == 3 and Ti.count_stone != C.TOTAL_STONE:
                        tile_type = 'Stone'
                        break
                    elif var == 4 and Ti.count_sheep != C.TOTAL_SHEEP:
                        tile_type = 'Sheep'
                        break
                    else:
                        counter = 0

            var = random.randint(0, len(self.ava_numbers)-1)

            if tile_type == 'Sand':
                number = 0
            else:
                number = self.ava_numbers[var]
                self.ava_numbers.pop(var)

            a = Ti(current[0], current[1], tile_type, number)

            if tile_type == 'Sand':
                a.is_robber = 1
            #print(a.number)
            Tiles_Mat.append(a)

            a.draw('Board')

            visited.add(current)
            
            neighbors = m.getlocations(current[0], current[1])
            neighbors = [tuple(inner_list) for inner_list in neighbors]
            
            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.append(neighbor)
            
            if len(final_loc) == 19:
                break
        
        turtle.tracer(True)

        self.Tiles_Mat = Tiles_Mat
        return final_loc
    
    def build_the_border(self):
        m.hexagon_shape(0,0,'Board', 'Blue', 240, 'On', 'Yes')

    def assign_corners(self):

        corner_mat_class = []
        temp_mat = []
        temp_mat_2 = []
        road_mat = []
        temp_mat_3 = []
        road_mat_class = []

        for i in self.Tiles_Mat:
            temp_mat.append(i.corner_mat)

            for j in range(len(i.corner_mat)):
                road_mat.append([i.corner_mat[j-1], i.corner_mat[j]])
        
        for sub in road_mat:
        #for item in sub:
            if sub not in temp_mat_3 and [sub[1], sub[0]] not in temp_mat_3:
                temp_mat_3.append(sub)

        for i in range(len(temp_mat_3)):
            road_mat_class.append(R(temp_mat_3[i]))

        self.road_mat_class = road_mat_class


        for sub in temp_mat:
            for item in sub:
                if item not in temp_mat_2:
                    temp_mat_2.append(item)


        for i in temp_mat_2:
            corner_mat_class.append(Co(i[0], i[1]))

        self.corner_mat_class = corner_mat_class

        for i in corner_mat_class:
            i.nearby_corners(self.Tiles_Mat)

        for i in road_mat_class:
            i.nearby_roads(self.road_mat_class)
            i.nearby_corners(self.corner_mat_class)

    def draw_current_board(self, team_class):

        for j in team_class:

            for i in self.road_mat_class:

                if i.is_occupied == 1:
                    i.draw(j.colour)

            for i in self.corner_mat_class:
                if i.is_occupied == 1:
                    i.draw(j.colour)

    # Assign Corner Mat's to Tiles
    def give_tile_mat(self):
        
        for i in self.Tiles_Mat:

            for k in range(len(i.corner_mat)):
                for j in self.corner_mat_class:
                    #print(i.corner_mat[j][0])

                    if j.x == i.corner_mat[k][0] and j.y == i.corner_mat[k][1]:
                        i.corner_mat_class.append(j)

    # Assign Corner Mat's to Tiles
    def give_corner_mat(self):
        
        for i in self.corner_mat_class:

            for k in range(len(i.nearby_corners_mat)):
                for j in self.corner_mat_class:
                    #print(i.corner_mat[j][0])

                    if j.x == i.nearby_corners_mat[k][0] and j.y == i.nearby_corners_mat[k][1]:
                        i.nearby_corners_mat_class.append(j)

    def draw_game_options(self):

        m.draw_rectangle(200, 200, 40, 50)

        