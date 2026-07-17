import Config as C
from dataclasses import dataclass, field, asdict
from typing import ClassVar

@dataclass
class Tiles:

    count: ClassVar = 0
    x_cord: int
    y_cord: int
    land_type: int
    resource_type: str
    resource_amount: int
    occupied: bool = field(default=False, init=False)

    def __post_init__ (self):
        Tiles.count += 1
        
        if self.land_type == C.T_GRASS: ## Grass
            self.land_movable = 1
            self.water_movable = 0

        elif self.land_type == C.T_WALL: ## Wall
            self.land_movable = 0
            self.water_movable = 0

        elif self.land_type == C.T_WATER: ## Water
            self.land_movable = 0
            self.water_movable = 1

        else:
            self.land_movable = 0
            self.water_movable = 0

        if self.resource_type == C.T_RESOURCE:
            self.resource_type = 'Minerals'

        elif self.resource_type == C.T_FUEL:
            self.resource_type = 'Fuel'

        elif self.resource_type == C.T_GOLD:
            self.resource_type = 'Gold'

        else:
            self.resource_type = None
        
    def pos(self):
        return (self.x_cord, self.y_cord)
    
    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, d):
        obj = cls(**d)
        obj.occupied = d.get("occupied", False)
        return cls(**d)