import Config as C

class Player:
    def __init__(self, colour, team, human):

        self.avaliable_road_pieces = C.TOTAL_ROAD_PIECES
        self.avaliable_settlement_pieces = C.TOTAL_SETTLEMENT_PIECES
        self.avaliable_city_pieces = C.TOTAL_CITY_PIECES

        self.is_human = human

        self.colour = colour

        self.resources = []
        
        self.team = team

        self.cards = []

        self.current_points = 0