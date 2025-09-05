import Config as C

class Tiles:

    count = 0

    def __init__ (self, x_cord, y_cord, land_type):
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.land_type = land_type
        Tiles.count += 1
        self.occupied = False
        
        if land_type == C.T_GRASS: ## Grass
            self.land_movable = 1
            self.water_movable = 0

        elif land_type == C.T_WALL: ## Wall
            self.land_movable = 0
            self.water_movable = 0

        elif land_type == C.T_RESOURCE: ## Ore Resource
            self.resource_health = C.ORE_RESOURCE_HEALTH
            self.harvest_timer = C.ORE_HARVEST_TIME
            self.land_movable = 1
            self.water_movable = 0

        elif land_type == C.T_GEMS: ## Gem Resource
            self.resource_health = C.GEM_RESOURCE_HEALTH
            self.harvest_timer = C.GEM_HARVEST_TIME
            self.land_movable = 1
            self.water_movable = 0

        else:
            self.land_movable = 0
            self.water_movable = 0