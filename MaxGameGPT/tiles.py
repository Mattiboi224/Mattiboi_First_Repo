import Config as C

class Tiles:

    count = 0

    def __init__ (self, x_cord, y_cord, land_type, resource_type, resource_amount):
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.land_type = land_type
        Tiles.count += 1
        self.occupied = False
        self.resource_amount = resource_amount
        
        if land_type == C.T_GRASS: ## Grass
            self.land_movable = 1
            self.water_movable = 0

        elif land_type == C.T_WALL: ## Wall
            self.land_movable = 0
            self.water_movable = 0

        else:
            self.land_movable = 0
            self.water_movable = 0

        if resource_type == C.T_RESOURCE:
            self.resource_type = 'Minerals'

        elif resource_type == C.T_FUEL:
            self.resource_type = 'Fuel'

        elif resource_type == C.T_GOLD:
            self.resource_type = 'Gold'

        else:
            self.resource_type = None
        