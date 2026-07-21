import Config as C
from player import Player
import random
import util as m
import pygame
from tile import Tile

class Game:

    def __init__(self):
        player_list = []

        total_teams = 1 + C.NO_OF_AI_PLAYERS

        # Create the Teams
        for i in range(total_teams):
            if i == C.PLAYER_TEAM:
                player_list.append(Player(i, True))
            else:
                player_list.append(Player(i, False))

        self.player_list = player_list

        self.tile_map = []

        self._draw_cache = []  # precomputed geometry, built once

        self.generate_map()

        for i in range(C.MAP_LENGTH):
            number_of_lines_on_box = len(self.grid_map[i])
            dist_between_lines = C.TILE / number_of_lines_on_box

            colour = m.get_colour(i)
            x, y, row, col = m.tile_position(i, C.tiles_per_row, C.TILE, C.TILE)

            self.tile_map.append(Tile(x, y, i, number_of_lines_on_box))

            main_rect = pygame.Rect(x, y, C.TILE, C.TILE)
            main_lines = [
                [(x, y + (k + 1) * dist_between_lines),
                (x + C.TILE, y + (k + 1) * dist_between_lines)]
                for k in range(number_of_lines_on_box - 1)
            ]

            is_last_in_row = (
                (row % 2 == 0 and col == C.tiles_per_row - 1) or
                (row % 2 == 1 and col == 0)
            )

            connector = None
            if is_last_in_row and i + 1 < C.MAP_LENGTH:
                connector_rect = pygame.Rect(x, y + C.TILE, C.TILE, C.TILE)
                connector_lines = [
                    [(x + (k + 1) * dist_between_lines, y + C.TILE),
                    (x + (k + 1) * dist_between_lines, y + C.TILE + C.TILE)]
                    for k in range(number_of_lines_on_box - 1)
                ]
                connector = (connector_rect, connector_lines)

            self._draw_cache.append({
                "colour": colour,
                "main_rect": main_rect,
                "main_lines": main_lines,
                "connector": connector,
            })

        
        self.generate_stating_positions()

        for i in self.player_list:
            i.assign_rider()
            i.assign_rider_to_tile(self.tile_map)

    def move_racer(self, entity, rider_type):

        colour = entity.colour
        if rider_type == 'Climber':
            loc = entity.climber_loc
            deck = entity.climber_deck
            played = entity.played_climber_card

        elif rider_type == 'Sprinter':
            loc = entity.sprinter_loc
            deck = entity.sprinter_deck
            played = entity.played_sprinter_card

        self.grid_map[loc[0]][loc[1]] = ''  # clear old spot

        card = deck.pop(0)
        played.append(card)
        loc[0] += card

        # find first empty column in the new row, else stay one row back
        row = self.grid_map[loc[0]]
        index = next((j for j, cell in enumerate(row) if cell == ''), None)
        if index is None:
            loc[0] -= 1
        else:
            loc[1] = index

        self.grid_map[loc[0]][loc[1]] = colour

        entity.assign_rider_to_tile(self.tile_map)

    def assess_slip_streaming(self):

        all_rider_locs = []
        for i in self.player_list:
            all_rider_locs.append(i.sprinter_loc)
            all_rider_locs.append(i.climber_loc)

        sorted_rider_locs = sorted(all_rider_locs, key=lambda x: (-x[0], x[1]))

        orig = 0
        slip_steaming = False
        for i in range(len(sorted_rider_locs)):
            
            if i == 0:
                orig = i[0]
                continue

            # Turn off slip streaming if not in slip stream range
            if orig - i[0] > 2:
                orig = i[0]
                slip_steaming = False

            if orig - i[0]== 2 or slip_steaming == True:
                orig = i[0]
                # Apply Slip streaming
                slip_steaming = True
                i[0] += 1

                
                




    def generate_map(self):

        # Map is a matrix
        # Then each row is the row in which you can go
        # Total Length is about 50
        # Create the map
        grid_map = []

        for i in range(C.MAP_LENGTH):
            j = random.randint(0,1)

            if i <= C.STARTING_LENGTH:
                j = 2
            blank_list = ["" for _ in range(2)]
            grid_map.append(blank_list)

        self.grid_map = grid_map

    def generate_stating_positions(self):
        # Determine starting positions
        for i in range(len(self.player_list * 2)):

            # First Round Randomly pick the ride
            if i <= len(self.player_list):
                choose_the_rider = random.choice([0,1])

            if i >= len(self.player_list):
                i -= len(self.player_list)
                if not self.player_list[i].climber_loc:
                    choose_the_rider = self.player_list[i].CLIMBER

                else:
                    choose_the_rider = self.player_list[i].SPRINTER

            building = True
            while building:
                starting_row = random.randint(0,C.STARTING_LENGTH)
                start_position_on_row = random.randint(0, len(self.grid_map[starting_row]) - 1)

                if not self.grid_map[starting_row][start_position_on_row]:
                    self.grid_map[starting_row][start_position_on_row] = self.player_list[i].colour
                    building = False

            if choose_the_rider == self.player_list[i].CLIMBER:
                self.player_list[i].climber_loc = [starting_row, start_position_on_row]
            else:
                self.player_list[i].sprinter_loc = [starting_row, start_position_on_row]




    def draw(self, surface):


        for entry in self._draw_cache:
            colour = entry["colour"]
            rect = entry["main_rect"]

            pygame.draw.rect(surface, colour, rect, border_radius=8)
            pygame.draw.rect(surface, C.border_colour, rect, 2, border_radius=8)

            for points in entry["main_lines"]:
                pygame.draw.lines(surface, C.border_colour, False, points, 3)

            if entry["connector"] is not None:
                connector_rect, connector_lines = entry["connector"]
                pygame.draw.rect(surface, colour, connector_rect, border_radius=8)
                pygame.draw.rect(surface, C.border_colour, connector_rect, 2, border_radius=8)
                for points in connector_lines:
                    pygame.draw.lines(surface, C.border_colour, False, points, 3)

        for i in self.player_list:
            i.draw(surface)
