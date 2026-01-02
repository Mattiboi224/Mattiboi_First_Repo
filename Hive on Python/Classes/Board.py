import turtle
import util as m
from collections import deque
import Config as C
from Tiles import Tiles as T


class Board():
    def __init__(self):
        self.all_locs = self.build_the_board()


    # Build the board
    def build_the_board(self):
        turtle.tracer(False)
        position = m.getlocations(0, 0)
        position = [tuple(inner_list) for inner_list in position]
        
        visited = set()
        queue = deque([(0, 0)] + position)
        
        final_loc = []
        self.Tiles_Mat = []
        
        while queue:
            current = queue.popleft()
            
            if current in visited:
                continue
            
            m.hexagon_shape(current[0], current[1], 'Board')
            final_loc.append([current[0], current[1]])
            self.Tiles_Mat.append(T(current[0], current[1]))
            
            visited.add(current)
            
            neighbors = m.getlocations(current[0], current[1])
            neighbors = [tuple(inner_list) for inner_list in neighbors]
            
            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.append(neighbor)
            
            if len(final_loc) == 91:
                break
        
        turtle.tracer(True)
        return final_loc
    



        # Drawing Announcers
    def draw_board(self, color, x, y, label):
        C.board_turtle.color(color)
        C.board_turtle.begin_fill()
        m.draw_rectangle(x, y, 150, 50, 'Board')
        C.board_turtle.end_fill()
        
        turtle.tracer(False)
        C.board_turtle.color('white')
        C.board_turtle.goto(x + 75, y + 10)
        C.board_turtle.write(label, False, align="center", font=("Arial", 20, "normal"))
        
        C.board_turtle.color(color)
        y_positions = [385, 370, 355, 340, 325]
        labels = ["Queen remaining: ", "Ants remaining: ", "Grasshoppers remaining: ", "Spiders remaining: ", "Beetles remaining: "]
        
        for i in range(len(y_positions)):
            C.board_turtle.goto(x + (0 if label == "Comp" else 145), y_positions[i])
            C.board_turtle.write(labels[i], False, align=("left" if label == "Comp" else "right"), font=("Arial", 10, "normal"))
        
        turtle.tracer(True)