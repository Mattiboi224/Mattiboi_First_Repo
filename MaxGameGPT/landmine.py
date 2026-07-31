import Config as C
from building import Building

class Landmine(Building):

    def __init__(self):
        stats = C.ENTITY_STATS[self.name]

        self.stealth = stats.get("stealth", False)
        self.damage = stats.get("damage", 0)
        self.explosive = stats.get("explosive", False)     
        self.blast_radius = stats["blast_radius"]
        self.trigger_radius = stats["trigger_radius"]
