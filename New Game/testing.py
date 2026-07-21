import Config as C
import random
from player import Player
import pygame
import math
from game import Game as Game
import util as m
#import pygame
from tile import Tile

game = Game()
# Initialize Pygame
pygame.init()

# Set up display
surface = pygame.display.set_mode((C.WIDTH, C.HEIGHT+28))


for i in range(C.MAP_LENGTH):

    number_of_lines_on_box = len(game.grid_map[i])

    dist_between_lines = C.TILE / (number_of_lines_on_box)


    colour = m.get_colour(i)
    x, y, row, col = m.tile_position(i, C.tiles_per_row, C.TILE, C.TILE)

    game.tile_map.append(Tile(x, y, i, number_of_lines_on_box))
    

    pygame.draw.rect(surface, colour, pygame.Rect(x, y, C.TILE, C.TILE), border_radius=8)
    rect = pygame.Rect(x,y, C.TILE, C.TILE)
    pygame.draw.rect(surface, C.border_colour, rect, 2, border_radius=8)

    for k in range(number_of_lines_on_box - 1):
        points = [(x, y + (k + 1) * dist_between_lines), (x + C.TILE, y + (k + 1) * dist_between_lines)]
        pygame.draw.lines(surface, C.border_colour, False, points, 3)


    # Is this tile the last one in its row (i.e. the turning point)?
    is_last_in_row = (
        (row % 2 == 0 and col == C.tiles_per_row - 1) or
        (row % 2 == 1 and col == 0)
    )


    if is_last_in_row and i + 1 < C.MAP_LENGTH:
        # Fill the gap with a square connector, same x/width as this tile,
        # spanning down into the start of the next row.
        pygame.draw.rect(
            surface,
            colour,  # or get_colour(i + 1) if you want it to match the next tile instead
            pygame.Rect(x, y + C.TILE, C.TILE, C.TILE),
            border_radius=8
        )
        rect = pygame.Rect(x,y + C.TILE, C.TILE, C.TILE)
        pygame.draw.rect(surface, C.border_colour, rect, 2, border_radius=8)

        for k in range(number_of_lines_on_box - 1):
            points = [(x + (k + 1) * dist_between_lines, y + C.TILE), (x + (k + 1) * dist_between_lines, y + C.TILE + C.TILE)]
            pygame.draw.lines(surface, C.border_colour, False, points, 3)

# Update the display
pygame.display.flip()

# Keep the window open until closed by the user
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()

