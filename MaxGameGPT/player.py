
import Config as C

class Player():
    def __init__(self, team, human=False):
        
        self.human = human

        self.team = team
        self.money = C.INITIAL_MONEY
        self.fuel = C.INITIAL_FUEL
        self.gold = C.INITIAL_GOLD

        self.colour = C.TEAM_COLORS[team]

        self.storage_money = 0
        self.storage_fuel = 0
        self.storage_gold = 0

        self.units = []
        self.buildings = []
        self.total_buildings = []
        self.total_units = []
            

