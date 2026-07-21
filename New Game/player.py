import Config as C
import random
from rider import Rider

class Player():

    def __init__(self, team, human):
        self.team = team

        self.climber_deck = C.CLIMBER_DECK.copy() * 3
        self.sprinter_deck = C.SPRINTER_DECK.copy() * 3

        random.shuffle(self.climber_deck)
        random.shuffle(self.sprinter_deck)

        self.played_climber_card = []
        self.played_sprinter_card = []

        self.CLIMBER = []


        self.climber_loc = []
        self.sprinter_loc = []

        self.colour = C.TEAM_COLORS[self.team]

    def assign_rider(self):

        self.climber = Rider(self, self.climber_loc[0], self.climber_loc[1], 'Climber')
        self.sprinter = Rider(self, self.sprinter_loc[0], self.sprinter_loc[1], 'Sprinter')

    def assign_rider_to_tile(self, tile_map):
        
        for i in range(len(tile_map)):
            
            if self.sprinter_loc[0] == i:
                for j in tile_map[i].boxes_in_tile:
                    if j.row_number == self.sprinter_loc[1]:
                        x, y = j.centre()
                        self.sprinter.x = x
                        self.sprinter.y = y
                        self.sprinter.grid_x = self.sprinter_loc[0]
                        self.sprinter.grid_y = self.sprinter_loc[1]

            if self.climber_loc[0] == i:
                for j in tile_map[i].boxes_in_tile:
                    if j.row_number == self.climber_loc[1]:
                        x, y = j.centre()
                        self.climber.x = x
                        self.climber.y = y
                        self.climber.grid_x = self.climber_loc[0]
                        self.climber.grid_y = self.climber_loc[1]

    def draw(self, surf):

        self.climber.draw(surf)
        self.sprinter.draw(surf)
