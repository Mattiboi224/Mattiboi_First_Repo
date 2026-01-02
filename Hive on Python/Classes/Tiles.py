import util as m
import Config as C

class Tiles():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.loc = [x,y]
        self.close_tiles = m.getlocations(self.x, self.y)
        self.radius = C.radius
        self.is_occupied = 0
        self.nearby_tiles = []



    def pos(self):
        return [self.x, self.y]
    
    def get_nearby_tiles(self, Tiles_Mat):

        for i in range(len(self.close_tiles)):

            for j in Tiles_Mat:
                
                if self.close_tiles[i] == j.loc:

                    self.nearby_tiles.append(j)
