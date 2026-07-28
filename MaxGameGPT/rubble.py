import Config as C
from dataclasses import dataclass, field
import util as m
import pygame

@dataclass
class Rubble:
    value: int = 0
    clear_work: int= 100
    work_done: int= 0
    x: int = 0
    y: int = 0
    radius: int = 0

    def __post_init__(self):

        if self.radius == C.TILE / 2:
            self.name = 'Rubble'
        elif self.radius == C.TILE:
            self.name = 'Big Rubble'
        stats = C.ENTITY_STATS[self.name]

        image_path = stats['image']

        self.rubble_image = pygame.image.load(image_path).convert_alpha()


    def pos(self):
        return (self.x, self.y)
    
    def pos_grid(self):
        self.grid_x, self.grid_y = m.to_grid(self.pos())
        return (self.grid_x, self.grid_y)

    def pos_camera(self, camera_x, camera_y):
        return (self.x - camera_x, self.y - camera_y)

    def draw(self, surf, font, camera_x, camera_y):
        screen_x = self.x - camera_x + C.UNIT_MENU_WIDTH
        screen_y = self.y - camera_y

        rect = self.rubble_image.get_rect(center=(int(screen_x), int(screen_y)))
        surf.blit(self.rubble_image, rect)

