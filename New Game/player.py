import Config as C

class Player():

    def __init__(self, team, human):
        self.team = team

        self.climber_hand = C.CLIMBER_HAND
        self.sprinter_hand = C.SPRINTER_HAND

        self.CLIMBER = 0
        self.SPRINTER = 1

        self.climber_loc = []
        self.sprinter_loc = []

        self.colour = C.TEAM_COLORS[self.team]
        
    pass