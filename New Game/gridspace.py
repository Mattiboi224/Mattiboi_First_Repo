
import Config as C

class Gridspace:

    def __init__(self, x, y, row_number, dist_between_lines):

        # X Y is the Top Right spot in the grid
        self.x = x
        self.y = y
        self.row_number = row_number
        self.dist_between_lines = dist_between_lines


    def centre(self):

        return self.x + C.TILE / 2, self.y + self.dist_between_lines / 2

    