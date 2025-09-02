import Constants as c

class Tiles():

    count = 0

    def __init__ (self, x_centre, y_centre, land_type, x_cord, y_cord):
        self.placeholder = 0
        self.x_centre = x_centre
        self.y_centre = y_centre
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.tl_x_cord = x_centre - c.x_pixel_size / 2
        self.tl_y_cord = y_centre - c.y_pixel_size / 2
        self.land_type = land_type
        Tiles.count += 1
        
        if land_type == 'water':
            self.land_movable = 0
            self.water_movable = 1

        elif land_type == 'land':
            self.land_movable = 1
            self.water_movable = 0

        else:
            self.land_movable = 0
            self.water_movable = 0