# Costs
COST_WORKER = 50
COST_SOLDIER = 60
COST_BARRACKS = 75
COST_TANK = 150
COST_TANK_FACTORY = 100
COST_BASE = 100


UNIT_STATS = {
    "Barracks": {"cost": COST_BARRACKS, "kind": "barracks"},
    "Soldier":  {"cost": COST_SOLDIER,  "kind": "soldier"},
    "Tank":     {"cost": COST_TANK,     "kind": "tank"},
    "Base":     {"cost": COST_BASE,     "kind": "base"},
    "Tank Factory":     {"cost": COST_TANK_FACTORY,     "kind": "tank_factory"},
}

if "tank" in UNIT_STATS.get("tank"):
    print("In")