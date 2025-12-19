import util as m

class Tiles():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.close_tiles = m.getlocations(self.x, self.y)
        