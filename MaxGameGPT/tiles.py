import Config as C

class Tiles:

    count = 0

    def __init__ (self, x_cord, y_cord, land_type):
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.land_type = land_type
        Tiles.count += 1
        self.occupied = False
        
        if land_type == 0: ## Grass
            self.land_movable = 1
            self.water_movable = 0

        elif land_type == 1: ## Wall
            self.land_movable = 0
            self.water_movable = 0

        elif land_type == 2: ## Resource
            self.resource_health = C.RESOURCE_HEALTH
            self.land_movable = 1
            self.water_movable = 0
        
        else:
            self.land_movable = 0
            self.water_movable = 0