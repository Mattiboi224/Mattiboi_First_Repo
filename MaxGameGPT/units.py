import pygame
import math

from entity import Entity
import Config as C
import util as m

# pyright: ignore[reportMissingImports]

class Unit(Entity):
    def __init__(self, team, x, y, image, kind="worker"):
        super().__init__(team, x, y, image, radius=12)
        self.kind = kind
        if kind == "worker":
            self.hp = self.max_hp = C.WORKER_HP
            self.atk = C.WORKER_ATK
            self.range = C.WORKER_RANGE
            self.speed = C.WORKER_SPEED
        elif kind == "tank":
            self.hp = self.max_hp = C.TANK_HP
            self.atk = C.TANK_ATK
            self.range = C.TANK_RANGE
            self.speed = C.TANK_SPEED
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
        self.old_res = None
        self.image = pygame.image.load(image).convert_alpha()

    def set_path(self, path_tiles):
        self.path = path_tiles
        # convert to centers
        self.path_px = [m.tile_center(tx, ty) for (tx,ty) in self.path]

    def update(self, dt, game):
        # Attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt

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

        #if len(self.path) > 1:
        #    tx, ty = m.to_grid(self.pos())
        #    occupied_tile = game.tile_map[tx][ty]
        #    occupied_tile.occupied = True

        # If harvesting
        if self.harvesting:
            res = game.find_nearest_resource(self.pos())
            tx, ty = m.to_grid(self.pos()) 

            if res != self.old_res and self.old_res != None:
                ux, uy = res
                path = m.astar(game.grid.tiles, m.to_grid(self.pos()), (ux, uy))
                self.set_path(path)
                

            #print(res)
            #print(tx, ty)
            #print(m.dist((tx, ty), res))
            if res and m.dist((tx, ty), res) < 2:
                self.harvest_timer -= dt
                if self.harvest_timer <= 0:

                    #print(game.tile_map[0][0])

                    affected_resource = game.tile_map[res[0]][res[1]]
                    
                    #print(affected_resource.x_cord)
                    #print(affected_resource.y_cord)
                    affected_resource.resource_health -= C.HARVEST_PER_TRIP

#                    if affected_resource.resource_health != 200:
#                        print(affected_resource.resource_health)

                    if affected_resource.resource_health == 0:
                        affected_resource.land_type = 0
                        #print(res)
                        #print("Grid:", game.grid.tiles[ty][tx])
                        game.grid.tiles[ty][tx] = 0

                    # deliver resources
                    self.carry = C.HARVEST_PER_TRIP
                    self.harvesting = False
                    # auto-return to nearest friendly building to drop off (Base or Barracks)
                    dest = game.find_nearest_dropoff(self.team, self.pos())
                    if dest:
                        tx, ty = m.to_grid(dest.pos())
                        #print(tx)
                        #print(ty)
                        path = m.astar(game.grid.tiles, m.to_grid(self.pos()), (tx, ty))
                        self.set_path(path)
                        #print("Drop-Off:", path)

            self.old_res = res
            return

        # If carrying and at a drop-off, deposit
        if self.carry > 0:
            # If near friendly building
            drop = game.find_nearest_dropoff(self.team, self.pos())
            #print(drop)
            if drop and m.dist(self.pos(), drop.pos()) < 40:
                game.money[self.team] += self.carry
                self.carry = 0
        

                dest2 = game.find_nearest_resource(self.pos())
                #print(dest2)
                if dest2 is not None:
                    #print("Going back to harvest")
                    ux, uy = dest2
                    #print("Resource:", ux)
                    #print("Resource:", uy)
                    #tx, ty = to_grid(dest2.pos())
                    path = m.astar(game.grid.tiles, m.to_grid(self.pos()), (ux, uy))
                    self.set_path(path)
                    #print("Finding Resource: ", path)
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


    def try_attack(self, enemy, dt):
        d = m.dist(self.pos(), enemy.pos())
        if d <= self.range and self.attack_cooldown <= 0:
            enemy.take_damage(self.atk)
            self.attack_cooldown = 0.8

    def draw(self, surf):
        col = C.TEAM_COLORS.get(self.team, (200,200,200))
        rect = pygame.Rect(0,0, C.TILE, C.TILE)
        rect.center = (int(self.x), int(self.y))
        pygame.draw.rect(surf, col, rect)
        #pygame.draw.circle(surf, col, (int(self.x), int(self.y)), self.radius)
        # if self.kind == "worker":
        #     pygame.draw.circle(surf, (240,240,240), (int(self.x), int(self.y)), 6)
        #     text = font.render("W", True, (0,0,0))
        #     surf.blit(text, (int(self.x) - 7, int(self.y) - 7))
        # elif self.kind == "tank":
        #     pygame.draw.circle(surf, (100,100,100), (int(self.x), int(self.y)), 6)
        #     text = font.render("T", True, (0,0,0))
        #     surf.blit(text, (int(self.x) - 7, int(self.y) - 7))
        # else:
        #     pygame.draw.circle(surf, (80,80,80), (int(self.x), int(self.y)), 6)
        #     text = font.render("S", True, (0,0,0))
        #     surf.blit(text, (int(self.x) - 7, int(self.y) - 7))
        # if self.selected:
        #     pygame.draw.circle(surf, (255,255,255), (int(self.x), int(self.y)), self.radius+2, 2)

        rect = self.image.get_rect(center=(int(self.x)+1, int(self.y)+1))
        surf.blit(self.image, rect)

        self.draw_health_bar(surf)