import pygame
from entity import Entity
import Config as C
import random
import math
import util as m

class Building(Entity):
    def __init__(self, team, x, y, kind="base"):
        super().__init__(team, x, y, radius=16)
        self.kind = kind
        if kind == "base":
            self.hp = self.max_hp = C.BASE_HP
        else:
            self.hp = self.max_hp = C.BARRACKS_HP
        self.queue = []     # production queue of ("worker" or "soldier")
        self.queue_time = 0.0

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
                angle = random.random() * math.tau
                r = 24
                px = self.x + math.cos(angle) * r
                py = self.y + math.sin(angle) * r
                game.spawn_unit(self.team, px, py, unit_type)
                # reset timer if more remain
                if self.queue:
                    self.queue_time = C.BUILD_WORKER_TIME if self.queue[0] == "worker" else C.BUILD_SOLDIER_TIME

    def draw(self, surf):
        col = C.TEAM_COLORS.get(self.team, (200,200,200))
        rect = pygame.Rect(0,0, C.TILE, C.TILE)
        rect.center = (int(self.x), int(self.y))
        pygame.draw.rect(surf, col, rect)
        # icon
        if self.kind == "base":
            pygame.draw.rect(surf, (20,20,20), rect.inflate(-10,-10))
        else:
            pygame.draw.rect(surf, (220,220,220), rect.inflate(-10,-10))
        # selection ring (for player only)
        self.draw_health_bar(surf)