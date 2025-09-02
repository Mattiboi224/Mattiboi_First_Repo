# ------------------ GAME STATE ------------------

import pygame
import util as m
from gridmap import GridMap
import random
import Config as C
from units import Unit
from building import Building

class Game:
    def __init__(self):
        self.grid = GridMap(C.GRID_W, C.GRID_H)
        self.tile_map = self.grid.assign_tiles()
        self.units = []
        self.buildings = []
        self.money = {t: C.INITIAL_MONEY for t in [C.PLAYER_TEAM] + C.AI_TEAMS}
        self.help_on = True

        # Place bases
        spawns = [(2,2), (C.GRID_W-3, C.GRID_H-3), (C.GRID_W-3, 2), (2, C.GRID_H-3), (C.GRID_W//2, C.GRID_H-3)]
        random.shuffle(spawns)
        # Player base
        tx, ty = spawns[0]
        self.player_base = self.spawn_building(C.PLAYER_TEAM, *m.tile_center(tx, ty), C.BASE_IMAGE, "base")
        # Give player a worker
        self.spawn_unit(C.PLAYER_TEAM, *m.tile_center(tx+1, ty), C.WORKER_IMAGE, "worker")

        # AI bases
        for i, team in enumerate(C.AI_TEAMS, start=1):
            tx, ty = spawns[i % len(spawns)]
            self.spawn_building(team, *m.tile_center(tx, ty), C.BASE_IMAGE, "base")
            self.spawn_unit(team, *m.tile_center(tx+1, ty), C.WORKER_IMAGE, "worker")  # give AI a worker too

        # Selection
        self.select_start = None
        self.selection_rect = None
        self.selected_units = []

        # Modes
        self.map_edit = False
        self.paint_tile = C.T_WALL
        self.build_mode = False
        self.build_kind = "barracks"  # only building type available for now
        self.ghost_valid = False
        self.ghost_pos = (0,0)

        # AI
        self.ai_timers = {team: 0.0 for team in C.AI_TEAMS}

    # ---- Spawning ----
    def spawn_unit(self, team, x, y, image, kind):
        u = Unit(team, x, y, image, kind)
        self.units.append(u)
        return u

    def spawn_building(self, team, x, y, image, kind):
        b = Building(team, x, y, image, kind)
        self.buildings.append(b)
        return b

    # ---- Queries ----
    def find_nearest_enemy(self, team, pos, within=None):
        best = None
        bd = 1e9
        for u in self.units:
            if u.team == team or u.dead: continue
            d = m.dist(pos, u.pos())
            if within and d > within: continue
            if d < bd:
                bd = d; best = u
        for b in self.buildings:
            if b.team == team or b.dead: continue
            d = m.dist(pos, b.pos())
            if within and d > within: continue
            if d < bd:
                bd = d; best = b
        return best

    def find_nearest_dropoff(self, team, pos):
        best = None
        bd = 1e9
        for b in self.buildings:
            if b.team != team or b.dead: continue
            if b.kind in ("base","barracks"):
                d = m.dist(pos, b.pos())
                if d < bd:
                    bd = d; best = b
        
        return best
    
    def find_nearest_resource(self, pos):
        best = None
        bd = 1e9
        x, y = m.to_grid(pos)
        #print(x, y)
        #count = 0
        for i in range(C.GRID_H):
            for j in range(C.GRID_W):
                #print(self.grid.tiles[i][j])
                if self.grid.tiles[i][j] == 2:
                    d = m.dist((y,x), (i,j))
                    #count += 1
                    if d < bd:
                        bd = d; best = (j,i)
                        #print("bd:", bd)
                        #print(i, j)
        #print("Resource Loc:", best)
        #print(count)
        return best



    def unit_at_point(self, p, team=None):
        for u in reversed(self.units):
            if u.dead: continue
            if team is not None and u.team != team: continue
            if m.dist(p, u.pos()) <= u.radius:
                return u
        return None

    def building_at_point(self, p):
        for b in reversed(self.buildings):
            if b.dead: continue
            rect = pygame.Rect(0,0,C.TILE,C.TILE)
            rect.center = (int(b.x), int(b.y))
            if rect.collidepoint(p): return b
        return None

    # ---- Commands ----
    def order_move(self, units, dest_px):
        gx, gy = m.to_grid(dest_px)
        for u in units:
            sx, sy = m.to_grid(u.pos())
            path = m.astar(self.grid.tiles, (sx, sy), (gx, gy), passable=lambda t: t!=C.T_WALL)
            if path:
                u.set_path(path)

    def order_attack(self, units, target):
        for u in units:
            u.target = target

    def order_harvest(self, units, tile):
        tx, ty = tile
        for u in units:
            if u.kind != "worker": continue
            # path to the resource tile
            sx, sy = m.to_grid(u.pos())
            path = m.astar(self.grid.tiles, (sx, sy), (tx, ty), passable=lambda t: t!=C.T_WALL)
            if path:
                u.set_path(path)
                # when they arrive, start harvesting
                u.harvesting = True
                u.harvest_timer = C.HARVEST_TIME

    # ---- Update ----
    def update(self, dt):
        # Update units
        for u in self.units:
            if not u.dead:
                u.update(dt, self)
        # Remove dead
        self.units = [u for u in self.units if not u.dead]
        self.buildings = [b for b in self.buildings if not b.dead]

        # Update buildings
        for b in self.buildings:
            if not b.dead:
                b.update(dt, self)

        # AI
        self.update_ai(dt)

    def update_ai(self, dt):
        for team in C.AI_TEAMS:
            self.ai_timers[team] -= dt
            if self.ai_timers[team] <= 0:
                # Simple behavior:
                # - If they have money, queue soldier at base; sometimes build barracks
                # - Command soldiers to move toward player's base
                money = self.money[team]
                base = next((b for b in self.buildings if b.team == team and b.kind=="base"), None)
                if base:
                    # 30% chance to build a barracks near base if enough money
                    if money >= C.COST_BARRACKS and random.random() < 0.3:
                        # find a nearby free tile
                        gx, gy = m.to_grid(base.pos())
                        for _ in range(10):
                            ox = random.randint(-3,3)
                            oy = random.randint(-3,3)
                            tx, ty = gx+ox, gy+oy
                            if not m.in_bounds(tx, ty): continue
                            if self.grid.tiles[ty][tx] == C.T_GRASS:
                                px, py = m.tile_center(tx, ty)
                                self.spawn_building(team, px, py, C.BARRACKS_IMAGE, "barracks")
                                self.money[team] -= C.COST_BARRACKS
                                break
                    # queue a soldier somewhere (base or any barracks)
                    target_build = random.choice([b for b in self.buildings if b.team==team])
                    if money >= C.COST_SOLDIER:
                        target_build.queue.append("soldier")
                        target_build.queue_time = C.BUILD_SOLDIER_TIME if len(target_build.queue)==1 else target_build.queue_time
                        self.money[team] -= C.COST_SOLDIER

                    # Rally soldiers toward player's base
                    pbase = self.player_base
                    if pbase:
                        gx, gy = m.to_grid(pbase.pos())
                        for u in self.units:
                            if u.team==team and u.kind=="soldier" and (not u.path_px):
                                sx, sy = m.to_grid(u.pos())
                                path = m.astar(self.grid.tiles, (sx, sy), (gx, gy), passable=lambda t: t!=C.T_WALL)
                                if path:
                                    u.set_path(path)

                # Re-arm timer
                self.ai_timers[team] = random.uniform(4.0, 8.0)

    # ---- Drawing ----
    def draw(self, surf, font):
        self.grid.draw(surf)

        # Draw buildings
        for b in self.buildings:
            b.draw(surf)

        # Draw units
        for u in self.units:
            u.draw(surf)

        # selection rectangle
        if self.selection_rect:
            pygame.draw.rect(surf, (255,255,255), self.selection_rect, 1)

        # build ghost
        if self.build_mode:
            mx, my = pygame.mouse.get_pos()
            tx, ty = m.to_grid((mx, my))
            px, py = m.tile_center(tx, ty)
            rect = pygame.Rect(0,0,C.TILE,C.TILE)
            rect.center = (px, py)
            valid = m.in_bounds(tx, ty) and self.grid.tiles[ty][tx]==C.T_GRASS
            self.ghost_valid = valid
            self.ghost_pos = (px, py)
            pygame.draw.rect(surf, (200,200,200) if valid else (200,80,80), rect, 2)

        # UI
        pygame.draw.rect(surf, (0,0,0), (0, C.HEIGHT-28, C.WIDTH, 28))
        money_text = font.render(f"Money: {self.money[C.PLAYER_TEAM]}   Units: {len([u for u in self.units if u.team==C.PLAYER_TEAM])}   Buildings: {len([b for b in self.buildings if b.team==C.PLAYER_TEAM])}", True, (255,255,255))
        surf.blit(money_text, (6, C.HEIGHT-24))

        if self.help_on:
            self.draw_help(surf, font)

    def draw_help(self, surf, font):
        lines = [
            "Controls: Left-drag = select units | Right-click = move/attack/harvest | ESC = cancel/clear",
            "B: place Barracks (75) | U: train Worker at Base (50) | S: train Soldier at Barracks (60)",
            "W: place Tank Factory (100) | T: train Tank at Tank Factory (100)",
            "M: toggle Map Edit | [ / ] choose tile: Wall / Resource (paint while in Map Edit) | F1: toggle help",
        ]
        y = 6
        for line in lines:
            text = font.render(line, True, (0,0,0))
            pygame.draw.rect(surf, (255,255,255), (6, y-2, text.get_width()+8, text.get_height()+4))
            surf.blit(text, (10, y))
            y += text.get_height() + 6
