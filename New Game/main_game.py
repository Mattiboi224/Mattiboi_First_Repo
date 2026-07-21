
import Config as C
import random
from game import Game as Game
import pygame

pygame.init()
screen = pygame.display.set_mode((C.WIDTH, C.HEIGHT+28))
pygame.display.set_caption("La Flamme Rouge")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 22)

game = Game()

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left

                #rider_locs = []
                for i in game.player_list:

                    game.move_racer(i, 'Climber')
                    game.move_racer(i, 'Sprinter')

                game.assess_slip_streaming()


    screen.fill((30, 30, 30))
    game.draw(screen)

    # Update the display
    pygame.display.flip()


pygame.quit()

    


