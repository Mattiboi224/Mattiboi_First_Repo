import Config as C


class Player():

    def __init__(self, team, colour, human):

        self.colour = colour
        self.is_human = human
        self.team = team

        if human == 0:
            self.text = 'Comp'
        else:
            self.text = 'You'

        self.remaining_ant = C.total_ant
        self.remaining_grasshopper = C.total_grasshopper
        self.remaining_beetle = C.total_beetle
        self.remaining_spider = C.total_spider
        self.remaining_queen = C.total_queen

        self.current_bugs = []

