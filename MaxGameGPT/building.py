import pygame
from entity import Entity
import Config as C
import random
import math
import util as m

class Building(Entity):
    def __init__(self, team, x, y, image, kind="base"):
        super().__init__(team, x, y, image, kind, radius=16)
        self.kind = kind
        if kind == "base":
            self.hp = self.max_hp = C.BASE_HP
            self.armour = C.BASE_ARMOUR
        elif kind == "barracks":    
            self.hp = self.max_hp = C.BARRACKS_HP
            self.armour = C.BARRACKS_ARMOUR
        elif kind == "tank_factory":
            self.hp = self.max_hp = C.TANK_FACTORY_HP
            self.armour = C.TANK_FACTORY_ARMOUR

        self.queue = []     # production queue of ("worker" or "soldier")
        self.queue_time = 0.0
        self.image = pygame.image.frombytes(image.tobytes(), image.size, image.mode).convert_alpha()
        self.sold = False
        self.resupply_time = C.MINERAL_SUPPLY_TIME
        self.count = 0
        
        if kind == "small_power_plant":
            self.power_used = 10
        elif kind == "barracks":
            self.power_used = -1
        elif kind == "tank_factory":
            self.power_used = -2
        else:
            self.power_used = 0

        if kind in ('base', 'barracks', 'tank_factory'):
            self.power_on = False
        else:
            self.power_on = True

        if kind == "base":
            self.supply = True
        else:
            self.supply = False

    def pos(self):
        return (self.x, self.y)

    def grid_pos(self):
        return m.to_grid(self.pos())

    def assign_tile(self, tiles_mat):
        x, y = m.to_grid(self.pos())
        self.Tile = tiles_mat[x][y]
        self.Tile.occupied = True

    def repairing(self):
        if self.repair_mode:
            if self.hp < self.max_hp:
                self.hp += 1

    def update(self, dt, game):

        # process production queue
        if self.queue:
            self.queue_time -= dt
            if self.queue_time <= 0:
                unit_type = self.queue.pop(0)
                # spawn near the building
                r = 64
                spawn_point = True
                while spawn_point:
                    angle = random.random() * math.tau
                    px = self.x + math.cos(angle) * r
                    py = self.y + math.sin(angle) * r
                    gx, gy = m.to_grid((px, py))
                    if not m.in_bounds(gx, gy):
                        continue
                    if m.is_occupied(game.tile_map, gx, gy):
                        continue
                    if game.tile_map[gx][gy].occupied:
                        continue
                    if game.grid.tiles[gy][gx] == C.T_WALL or game.grid.tiles[gy][gx] == C.T_WATER:
                        continue
                    spawn_point = False

                # if unit_type == "worker":
                #     image_to_use = C.WORKER_IMAGE
                if unit_type == "soldier":
                    image_to_use = m.convert_image_to_team(C.SOLDIER_IMAGE, self.team, unit_type)
                elif unit_type == "tank":
                    image_to_use = m.convert_image_to_team(C.TANK_IMAGE, self.team, unit_type)
                elif unit_type == "ammo_truck":
                    image_to_use = m.convert_image_to_team(C.AMMO_TRUCK_IMAGE, self.team, unit_type)

                tx, ty = m.tile_center(gx, gy)
                game.spawn_unit(self.team, tx, ty, image_to_use, unit_type)
                # reset timer if more remain
                if self.queue:
                    if self.queue[0] == "worker":
                        self.queue_time = C.BUILD_WORKER_TIME
                    elif self.queue[0] == 'soldier':
                        self.queue_time = C.BUILD_SOLDIER_TIME
                    elif self.queue[0] == "tank":
                        self.queue_time = C.BUILD_TANK_TIME
                    elif self.queue[0] == "ammo_truck":
                        self.queue_time = C.BUILD_AMMO_TRUCK_TIME
                    else:
                        self.queue_time = C.BUILD_WORKER_TIME
        
        if self.supply:
            self.resupply_time -= dt

            # Every 10 Ticks Supply Money
            if self.resupply_time <= 0:

                #if self.count == 0 and self.team == 0:
                #    print(self.grid_pos())
            
                if self.Tile.resource_type == 'Minerals':
                    game.money[self.team] += self.Tile.resource_amount
                    self.resupply_time = C.MINERAL_SUPPLY_TIME
                    #print(self.resupply_time)
                
                elif self.Tile.resource_type == 'Fuel':
                    game.fuel[self.team] += self.Tile.resource_amount
                    self.resupply_time = 0

                elif self.Tile.resource_type == 'Gold':
                    game.gold[self.team] += self.Tile.resource_amount
                    self.resupply_time = 0


    def draw(self, surf, camera_x, camera_y):
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
          
        rect = self.image.get_rect(center=(int(screen_x), int(screen_y)))
        surf.blit(self.image, rect)

        self.draw_health_bar(surf, camera_x, camera_y)