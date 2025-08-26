import pygame
import math

from entity import Entity
import Config as C
import util as m

class Unit(Entity):
    def __init__(self, team, x, y, kind="worker"):
        super().__init__(team, x, y, radius=12)
        self.kind = kind
        if kind == "worker":
            self.hp = self.max_hp = C.WORKER_HP
            self.atk = C.WORKER_ATK
            self.range = C.WORKER_RANGE
            self.speed = C.WORKER_SPEED
        else:
            self.hp = self.max_hp = C.SOLDIER_HP
            self.atk = C.SOLDIER_ATK
            self.range = C.SOLDIER_RANGE
            self.speed = C.SOLDIER_SPEED
        self.path = []
        self.path_px = []
        self.target = None
        self.attack_cooldown = 0.0
        self.selected = False
        # Harvesting
        self.harvesting = False
        self.harvest_timer = 0.0
        self.carry = 0
        self.carry_max = C.HARVEST_PER_TRIP

    def set_path(self, path_tiles):
        self.path = path_tiles
        # convert to centers
        self.path_px = [m.tile_center(tx, ty) for (tx,ty) in self.path]

    def update(self, dt, game):
        # Attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt

        # If harvesting
        if self.harvesting:
            self.harvest_timer -= dt
            if self.harvest_timer <= 0:
                # deliver resources
                self.carry = C.HARVEST_PER_TRIP
                self.harvesting = False
                # auto-return to nearest friendly building to drop off (Base or Barracks)
                dest = game.find_nearest_dropoff(self.team, self.pos())
                if dest:
                    tx, ty = m.to_grid(dest.pos())
                    path = m.astar(game.grid.tiles, m.to_grid(self.pos()), (tx, ty))
                    self.set_path(path)

            return

        # If carrying and at a drop-off, deposit
        if self.carry > 0:
            # If near friendly building
            drop = game.find_nearest_dropoff(self.team, self.pos())
            if drop and m.dist(self.pos(), drop.pos()) < 40:
                game.money[self.team] += self.carry
                self.carry = 0

            dest2 = game.find_nearest_resource(self.pos())
            #print(dest2)
            if dest2 is not None:
                #print("Going back to harvest")
                ux, uy = dest2
                #tx, ty = to_grid(dest2.pos())
                path = m.astar(game.grid.tiles, m.to_grid(self.pos()), (ux, uy))
                self.set_path(path)
                self.harvesting = True
                self.harvest_timer = C.HARVEST_TIME
                #print("finish")
                #print(self.carry)
                return


        # Auto-target enemies in range
        if not self.harvesting:
            enemy = game.find_nearest_enemy(self.team, self.pos(), within=self.range)
            if enemy:
                self.try_attack(enemy, dt)
                return

        # Move along path
        if self.path_px:
            tx, ty = self.path_px[0]
            dx = tx - self.x
            dy = ty - self.y
            d = math.hypot(dx, dy)
            if d < 4:
                self.path_px.pop(0)
            else:
                vx = dx / d * self.speed
                vy = dy / d * self.speed
                self.x += vx * dt
                self.y += vy * dt

    def try_attack(self, enemy, dt):
        d = m.dist(self.pos(), enemy.pos())
        if d <= self.range and self.attack_cooldown <= 0:
            enemy.take_damage(self.atk)
            self.attack_cooldown = 0.8

    def draw(self, surf):
        col = C.TEAM_COLORS.get(self.team, (200,200,200))
        pygame.draw.circle(surf, col, (int(self.x), int(self.y)), self.radius)
        if self.kind == "worker":
            pygame.draw.circle(surf, (240,240,240), (int(self.x), int(self.y)), 6)
        else:
            pygame.draw.circle(surf, (80,80,80), (int(self.x), int(self.y)), 6)
        if self.selected:
            pygame.draw.circle(surf, (255,255,255), (int(self.x), int(self.y)), self.radius+2, 2)
        self.draw_health_bar(surf)