from dataclasses import dataclass, field, asdict, fields
import Config as C

@dataclass
class Player():
    team: int
    human: bool = False
    storage_money: int = field(default=0, init=False)
    storage_fuel: int = field(default=0, init=False)
    storage_gold: int = field(default=0, init=False)

    units: list = field(default_factory=list, init=False)
    buildings: list = field(default_factory=list, init=False)
    total_buildings: list = field(default_factory=list, init=False)
    total_units: list = field(default_factory=list, init=False)

    total_power: int = field(default=0, init=False)
    power_usage: int = field(default=0, init=False)

    def __post_init__(self):
    
        self.money = C.INITIAL_MONEY
        self.fuel = C.INITIAL_FUEL
        self.gold = C.INITIAL_GOLD

        self.colour = C.TEAM_COLORS[self.team]

    @property
    def power_balance(self):
        return self.total_power - self.power_usage

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, d):
            # Split fields into init-accepted vs init=False
        init_fields = {f.name for f in fields(cls) if f.init}
        non_init_fields = [f.name for f in fields(cls) if not f.init]

        # Build the object using only what __init__ accepts
        filtered = {k: v for k, v in d.items() if k in init_fields}
        obj = cls(**filtered)

        # Restore whatever __post_init__ would've computed, using saved values instead
        for name in non_init_fields:
            if name in d:
                setattr(obj, name, d[name])