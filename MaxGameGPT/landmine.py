import Config as C
from building import Building
from dataclasses import dataclass, field, KW_ONLY
from typing import ClassVar, Optional
from entity import Entity
from gridmap import GridMap
from player import Player
import util as m


@dataclass(kw_only=True)
class Landmine(Building):
    """A hidden trap building that explodes when an enemy unit gets close."""

    _id_counter: ClassVar[int] = 0

    trigger_radius: int = field(init=False)
    blast_radius: int = field(init=False)
    damage: int = field(init=False)
    hidden: bool = field(init=False, default=True)
    armed: bool = field(init=False, default=True)

    def __post_init__(self):
        super().__post_init__()  # if Building/Entity defines one
        stats = C.ENTITY_STATS["Land Mine"]
        self.trigger_radius = stats["trigger_radius"]
        self.blast_radius = stats["blast_radius"]
        self.damage = stats["damage"]
        self.hp = stats["hp"]

        Landmine._id_counter += 1
        self.id = Landmine._id_counter

    # ------------------------------------------------------------------
    # Visibility: hide from enemy draw passes unless detected/triggered
    # ------------------------------------------------------------------
    def is_visible_to(self, player) -> bool:
        if not self.hidden:
            return True
        return player is self.team

    def draw(self, surface, font, camera_x, camera_y, viewer):
        """Only render if the viewing player owns this mine or it's armed=False."""
        if not self.is_visible_to(viewer):
            return
        super().draw(surface, font, camera_x, camera_y)

    # ------------------------------------------------------------------
    # Trigger check: call this once per tick per mine, or on unit-move
    # events for efficiency (cheaper than a full-map scan every frame)
    # ------------------------------------------------------------------
    def check_trigger(self, game) -> Optional[list]:
        """Return list of units hit if triggered this tick, else None."""
        if not self.armed:
            return None

        nearby_tiles = m.locations_in_range(self.trigger_radius, self)

        for u in game.units:
            if u.pos_grid() in nearby_tiles: #and u.team != self.team:
                return self.explode(game)
        return None


    def explode(self, game) -> list:
        """Detonate: damage everything in blast_radius, then remove self."""
        self.armed = False
        blast_tiles = m.locations_in_range(self.blast_radius, self)

        hit_units = []
        for u in game.units:
            if u.pos_grid() in blast_tiles:
                u.hp -= self.damage
                hit_units.append(u)
                if u.hp <= 0:
                    u.dead = True

        self.dead = True

        return hit_units


# ----------------------------------------------------------------------
# Example integration in your main game loop / tick update:
#
#   for building in list(player.buildings):
#       if isinstance(building, Landmine):
#           hit = building.check_trigger(grid_map)
#           if hit:
#               play_explosion_effect(building.x, building.y)
# ----------------------------------------------------------------------
