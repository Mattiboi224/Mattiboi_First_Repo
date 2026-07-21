import util as m
import pygame
import Config as C

NEXT_ID = 1
def gen_id():
    global NEXT_ID
    i = NEXT_ID
    NEXT_ID += 1
    return i

class Rider(pygame.sprite.Sprite):

    def __init__(self, team, x, y, rider_type):
        
        self.id = gen_id()

        self.team = team
        self.grid_x = x
        self.grid_y = y
        self.rider_type = rider_type

        self.x = 0
        self.y = 0

        self.colour = team.colour

        converted_image = m.convert_image_to_team(self.team, self.rider_type)
        self.image = pygame.image.frombytes(converted_image.tobytes(), converted_image.size, converted_image.mode).convert_alpha()
        

    def draw(self, surf):
        
        rect = self.image.get_rect(center=(self.x, self.y))
        surf.blit(self.image, rect)


