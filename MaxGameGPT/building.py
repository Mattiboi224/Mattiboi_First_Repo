import pygame
from entity import Entity
import Config as C
import random
import math
import util as m

class Building(Entity):
    def __init__(self, team, x, y, image, kind="base"):
        super().__init__(team, x, y, image, radius=16)
        self.kind = kind
        if kind == "base":
            self.hp = self.max_hp = C.BASE_HP
        elif kind == "tank_factory":
            self.hp = self.max_hp = C.TANK_FACTORY_HP
        else:
            self.hp = self.max_hp = C.BARRACKS_HP
        self.queue = []     # production queue of ("worker" or "soldier")
        self.queue_time = 0.0
        self.image = pygame.image.load(image).convert_alpha()
        self.sold = False

    def pos(self):
        return (self.x, self.y)

    def grid_pos(self):
        return m.to_grid(self.pos())

    def update(self, dt, game):
        # process production queue
        if self.queue:
            self.queue_time -= dt
            if self.queue_time <= 0:
                unit_type = self.queue.pop(0)
                # spawn near the building
                r = 24
                spawn_point = True
                while spawn_point:
                    angle = random.random() * math.tau
                    px = self.x + math.cos(angle) * r
                    py = self.y + math.sin(angle) * r
                    gx, gy = m.to_grid((px, py))
                    if not m.in_bounds(gx, gy):
                        continue
                    spawn_point = False

                if unit_type == "worker":
                    image_to_use = C.WORKER_IMAGE
                elif unit_type == "soldier":
                    image_to_use = C.SOLDIER_IMAGE
                elif unit_type == "tank":
                    image_to_use = C.TANK_IMAGE
                game.spawn_unit(self.team, px, py, image_to_use, unit_type)
                # reset timer if more remain
                if self.queue:
                    self.queue_time = C.BUILD_WORKER_TIME if self.queue[0] == "worker" else C.BUILD_SOLDIER_TIME

    def draw(self, surf):
        col = C.TEAM_COLORS.get(self.team, (200,200,200))
        rect = pygame.Rect(0,0, C.TILE, C.TILE)
        rect.center = (int(self.x), int(self.y))
        pygame.draw.rect(surf, col, rect)
#        pygame.draw(surf)
        # icon
#        if self.kind == "base":
#            #pygame.draw.rect(surf, (20,20,20), rect.inflate(-10,-10))
#            self.image.get_rect()#
#
#        elif self.kind == "tank_factory":
#            pygame.draw.rect(surf, (100,100,100), rect.inflate(-10,-10))
#        else:
#            pygame.draw.rect(surf, (220,220,220), rect.inflate(-10,-10))
#        # selection ring (for player only) """

        rect = self.image.get_rect(center=(int(self.x), int(self.y)))
        surf.blit(self.image, rect)
        
        

        self.draw_health_bar(surf)