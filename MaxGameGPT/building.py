import pygame
from entity import Entity
import Config as C
import random
import math
import util as m

class Building(Entity):
    def __init__(self, team, x, y, image, kind="base", no_queue=False):
        super().__init__(team, x, y, image, kind, radius=16)
        self.kind = kind

        self.building = True

        stats = C.BUILDING_STATS[kind]
        self.hp = self.max_hp = stats["hp"]
        self.armour = stats["armour"]
        self.build_time = stats["build_time"]

        if no_queue:
            self.building = False
            self.build_time = 0.0

        build_image_convert = m.convert_image_to_team(C.CONSTRUCTION_IMAGE, team, 'construction')
        self.build_image = pygame.image.frombytes(build_image_convert.tobytes(), build_image_convert.size, build_image_convert.mode).convert_alpha()

        self.queue = []     # production queue of ("worker" or "soldier")
        self.queue_time = 0.0
        self.sold = False
        self.resupply_time = C.MINERAL_SUPPLY_TIME
        self.count = 0

        if self.building:
            self.curr_image = self.build_image
        else:
            self.curr_image = self.image

        self.selected = False


        if kind == "small_power_plant":
            self.power_used = 10
        elif kind == "barracks":
            self.power_used = -1
        elif kind == "tank_factory":
            self.power_used = -2
        else:
            self.power_used = 0

        if kind in ('small_power_plant'):
            self.power_on = True
        else:
            self.power_on = False

        if kind in ("base", "storage_unit", "fuel_tank", "gold_vault"):
            self.storage = True
        else:
            self.storage = False

        if kind == "base":
            self.supply = True
        else:
            self.supply = False

        self.local_labels = []
        if self.kind == "base":
            self.local_labels.append('Build')
        if self.storage:
            self.local_labels.append('X-fer')
        self.local_labels.append('Stop')

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

        if self.building:
            self.build_time -= dt
            if self.build_time <= 0:
                self.curr_image = self.image
                self.building = False

        # process production queue
        if not self.building:
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
                        image = C.SOLDIER_IMAGE
                    elif unit_type == "tank":
                        image = C.TANK_IMAGE
                    elif unit_type == "ammo_truck":
                        image = C.AMMO_TRUCK_IMAGE

                    tx, ty = m.tile_center(gx, gy)
                    game.spawn_unit(self.team, tx, ty, image, unit_type)
                    # reset timer if more remain
                    if self.queue:
                        if self.queue[0] == 'soldier':
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

                    if self.Tile.resource_type == 'Minerals':
                        if self.Tile.resource_amount + game.player_mat[self.team].money <= game.player_mat[self.team].storage_money:
                            game.player_mat[self.team].money += self.Tile.resource_amount
                            self.resupply_time = C.MINERAL_SUPPLY_TIME
                    
                    elif self.Tile.resource_type == 'Fuel':
                        if self.Tile.resource_amount + game.player_mat[self.team].fuel <= game.player_mat[self.team].storage_fuel:
                            game.player_mat[self.team].fuel += self.Tile.resource_amount
                            self.resupply_time = C.FUEL_SUPPLY_TIME

                    elif self.Tile.resource_type == 'Gold':
                        if self.Tile.resource_amount + game.player_mat[self.team].money <= game.player_mat[self.team].storage_gold:
                            game.player_mat[self.team].gold += self.Tile.resource_amount
                            self.resupply_time = C.GOLD_SUPPLY_TIME


    def draw(self, surf, font, camera_x, camera_y):
        screen_x = self.x - camera_x + C.UNIT_MENU_WIDTH
        screen_y = self.y - camera_y
          
        rect = self.curr_image.get_rect(center=(int(screen_x), int(screen_y)))
        surf.blit(self.curr_image, rect)

        self.draw_health_bar(surf, camera_x, camera_y)

        if self.selected:

            local_rect = pygame.Rect(screen_x + C.TILE, screen_y - C.TILE, C.TILE * 2, C.TILE * 2)
            pygame.draw.rect(surf, C.MENU_BG, local_rect)
        

            rects = []
            for i in range(len(self.local_labels)):   # or a fixed number of buttons
                rect = pygame.Rect(
                    screen_x + C.TILE,
                    screen_y - C.TILE + 5 + i * 20,
                    C.TILE * 2,
                    15
                )
                rects.append(rect)

            # Mouse position
            mx, my = pygame.mouse.get_pos()

            self.local_buttons = list(zip(self.local_labels, rects))

            for label, rect in self.local_buttons:

                color = C.BTN_HOVER if rect.collidepoint(mx, my) else C.BTN_COLOR
                pygame.draw.rect(surf, color, rect, border_radius=8)

                # Draw text
                text = font.render(label, True, C.TEXT_COLOR)
                surf.blit(text, (rect.x + 10, rect.y))
