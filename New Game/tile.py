import Config as C
from gridspace import Gridspace

class Tile:

    def __init__(self, x, y, tile_count, number_of_lines_on_box):

        # X Y is the Top Right spot in the grid
        self.x = x
        self.y = y

        # Tile Number
        self.tile_count = tile_count

        # Number of Lines of box
        dist_between_lines = C.TILE / (number_of_lines_on_box)

        self.boxes_in_tile = []
        for k in range(number_of_lines_on_box):
            self.boxes_in_tile.append(Gridspace(x, y + k * dist_between_lines, k, dist_between_lines))


    def centre_tile(self):
        return self.x + C.TILE / 2, self.y + C.TILE / 2
