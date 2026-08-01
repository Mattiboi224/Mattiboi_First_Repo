# ------------------ GAME STATE ------------------

import pygame
import util as m
from gridmap import GridMap
import random
import Config as C
from units import Unit
from building import Building
from menu import Menu
from player import Player
import json
from rubble import Rubble
from minimap import Minimap
from landmine import Landmine

class Game:
    def __init__(self):
        self.grid = GridMap()
        self.menu = Menu()
        
        self.tile_map = self.grid.assign_tiles()

        self.minimap = Minimap(self.grid, 120, 120)

        self.units = []
        self.buildings = []
        self.rubbles = []
        self.total_buildings = []
        self.total_units = []
        self.money = {t: C.INITIAL_MONEY for t in [C.PLAYER_TEAM] + C.AI_TEAMS}
        self.fuel = {t: 0 for t in [C.PLAYER_TEAM] + C.AI_TEAMS}
        self.gold = {t: 0 for t in [C.PLAYER_TEAM] + C.AI_TEAMS}

        self.help_on = False

        self.player_mat = []
        for i in [C.PLAYER_TEAM] + C.AI_TEAMS:
            if i == C.PLAYER_TEAM:
                self.player_mat.append(Player(i, human=True))
            else:
                self.player_mat.append(Player(i))

        # Place bases
        #spawns = [(1,1), (C.GRID_W-3, C.GRID_H-3), (C.GRID_W-3, 2), (2, C.GRID_H-3), (C.GRID_W//2, C.GRID_H-3)]
        if len(self.grid.spawns) != 0:
            spawns = self.grid.spawns
        random.shuffle(spawns)

        self.BUILDING_CLASSES = {
            "Land Mine": Landmine,
        }

        # Player base
        tx, ty = spawns[0]
        px, py = m.tile_center(tx, ty)
        self.player_base = self.spawn_building(C.PLAYER_TEAM, px + (C.TILE / 2), py + (C.TILE / 2), "Base", no_queue=True)
        self.spawn_building(C.PLAYER_TEAM, *m.tile_center(tx + 2, ty + 1), "Power Plant", no_queue=True)

        # AI bases
        for i, team in enumerate(C.AI_TEAMS, start=1):
            tx, ty = spawns[i % len(spawns)]
            px, py = m.tile_center(tx, ty)
            self.spawn_building(team, px + (C.TILE / 2), py + (C.TILE / 2), "Base", no_queue=True)
            self.spawn_building(team, *m.tile_center(tx + 2, ty + 1), "Power Plant", no_queue=True)

        # Selection
        self.select_start = None
        self.selection_rect = None
        self.selected_units = []

        # Camera
        self.camera_x, self.camera_y = C.CAMERA_X, C.CAMERA_Y
        self.camera_speed = C.CAMERA_SPEED

        # Modes
        self.map_edit = False
        self.paint_tile = C.T_WALL
        self.build_mode = False
        self.big_build_mode = False
        self.build_kind = "barracks"  # only building type available for now
        self.ghost_valid = False
        self.ghost_pos = (0,0)
        self.resource_mode = False
        self.sell_mode = False
        self.repair_mode = False
        self.move_mode = False
        self.attack_mode = False
        self.transfer_mode = False
        self.pause_mode = False

        # AI
        self.ai_timers = {team: 0.0 for team in C.AI_TEAMS}



    def save_game(self, filename):
        state = {
            "player": [p.to_dict() for p in self.player_mat],
            "units": [u.to_dict() for u in self.units],
            "buildings": [b.to_dict() for b in self.buildings],
            "gridmap": self.grid.to_dict(),  # handles its own tile matrix internally
            "camera": {"x": self.camera_x, "y": self.camera_y},
        }
        with open(filename, "w") as f:
            json.dump(state, f, indent=2)

    def load_game(self, filename):
        with open(filename) as f:
            state = json.load(f)
        self.player = [Player.from_dict(p) for p in state["player"]]
        self.units = [Unit.from_dict(u) for u in state["units"]]
        self.buildings = [Building.from_dict(b) for b in state["buildings"]]
        self.gridmap = GridMap.from_dict(state["gridmap"])
        self.camera_x = state["camera"]["x"]
        self.camera_y = state["camera"]["y"]

    # ---- Spawning ----
    def spawn_unit(self, team, x, y, name):
        u = Unit(team, x, y, name)
        self.units.append(u)
        self.total_units.append(u)  ## Used in End Game Stats
        self.player_mat[team].units.append(u)
        self.player_mat[team].total_units.append(u)
        return u

    def spawn_building(self, team, x, y, name, no_queue=False):
        stats = C.ENTITY_STATS[name]
        building_cls = self.BUILDING_CLASSES.get(name, Building)

        b = building_cls(
            team=team,
            x=x,
            y=y,
            name=name,
            no_queue=no_queue
        )
        b.assign_tile(self.tile_map)
        self.buildings.append(b)
        self.total_buildings.append(b)  ## Used in End Game Stats
        self.player_mat[team].buildings.append(b)
        self.player_mat[team].total_buildings.append(b)
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
            if b.team == team or b.dead or b.sold: continue
            d = m.dist(pos, b.pos())
            if within and d > within: continue
            if d < bd:
                bd = d; best = b
        return best

    def find_nearest_dropoff(self, team, pos):
        best = None
        bd = 1e9
        for b in self.buildings:
            if b.team != team or b.dead or b.sold: continue
            if b.kind in ("base","barracks"):
                d = m.dist(pos, b.pos())
                if d < bd:
                    bd = d; best = b
        
        return best

    def find_nearest_building(self, team, pos):
        b_type = [name for name, stats in C.ENTITY_STATS.items() if stats["category"] == "building"]
        b_type.remove("Construction")
        b_type.remove("Big Construction")
        b_type = tuple(b_type)
        best = None
        bd = 1e9
        for b in self.buildings:
            if b.team != team or b.dead or b.sold: continue
            if b.name in b_type:
                d = m.dist(pos, b.pos())
                if d < bd:
                    bd = d; best = b
        return best

    def find_nearest_unit(self, team, pos):
        u_type = tuple([name for name, stats in C.ENTITY_STATS.items() if stats["category"] == "unit"])
        best = None
        bd = 1e9
        for u in self.units:
            if u.team != team or u.dead: continue
            if u.name in u_type:
                d = m.dist(pos, u.pos())
                if d < bd:
                    bd = d; best = u
        
        return best

    def find_nearest_resource(self, pos):
        best = None
        bd = 1e9
        x, y = m.to_grid(pos)
        #count = 0
        for i in range(C.GRID_H):
            for j in range(C.GRID_W):
                if self.grid.tiles[i][j] == C.T_RESOURCE or self.grid.tiles[i][j] == C.T_GEMS:
                    d = m.dist((y,x), (i,j))
                    #count += 1
                    if d < bd:
                        bd = d; best = (j,i)

        return best

    def unit_at_point(self, p, team=None):
        p_list = list(p)
        p_list[0] -= C.UNIT_MENU_WIDTH
        p = tuple(p_list)
        for u in reversed(self.units):
            if u.dead: continue
            if team is not None and u.team != team: continue
            if m.dist(p, u.pos_camera(self.camera_x, self.camera_y)) <= u.radius:
                return u
        return None

    def building_at_point(self, p, team=None):
        p_list = list(p)
        p_list[0] -= C.UNIT_MENU_WIDTH
        p = tuple(p_list)
        for b in reversed(self.buildings):
            if b.dead or b.sold: continue
            if team is not None and b.team != team: continue
            if m.dist(p, b.pos_camera(self.camera_x, self.camera_y)) <= b.radius:
                return b
        return None

    def rubble_at_point(self, p):
        p_list = list(p)
        p_list[0] -= C.UNIT_MENU_WIDTH
        p = tuple(p_list)
        for r in reversed(self.rubbles):
            if m.dist(p, r.pos_camera(self.camera_x, self.camera_y)) <= r.radius:
                return r
        return None

    def occupied_tiles(self):
        
        self.unit_locs = []
        for u in self.units:
            if u.dead: continue
            self.unit_locs.append(m.to_grid(u.pos()))
        
        for b in self.buildings:
            if b.dead or b.sold: continue
            if b.name in ['Road', 'Bridge', 'Water Platform']: continue
            self.unit_locs.append(m.occupied_by_unit(b))

        self.unit_locs = [t for sublist in self.unit_locs for t in sublist]
        for w in range(len(self.tile_map)):
            for h in self.tile_map[w]:
                if h.pos() in self.unit_locs:
                    h.occupied = True
                else:
                    h.occupied = False
            
    def recalculate_storage_capacity(self, team):
        
        team.storage_money = sum(
            b.storage_amount for b in self.buildings if b.team == team.team and b.storage and not b.dead and not b.sold and b.resource_storage_type == "Minerals"
        )
        team.storage_fuel = sum(
            b.storage_amount for b in self.buildings if b.team == team.team and b.storage and not b.dead and not b.sold and b.resource_storage_type == "Fuel"
        )
        team.storage_gold = sum(
            b.storage_amount for b in self.buildings if b.team == team.team and b.storage and not b.dead and not b.sold and b.resource_storage_type == "Gold"
        )

    def recalculate_power_capacity(self, team):
        
        team.total_power = sum(
            b.power_given for b in self.buildings if b.team == team.team and not b.dead and not b.sold
        )

        team.power_usage = sum(
            b.power_used for b in self.buildings if b.team == team.team and not b.dead and not b.sold
        )

    def entity_at(self, x, y):
        for ent in self.buildings:  # or self.entities, whatever your master list is called
            tx, ty = ent.pos_grid()
            if tx == x and ty == y:
                return ent
        return None

    def effective_tile(self, x, y):
        ent = self.entity_at(x, y)
        if ent is not None and ent.name == "Bridge":
            return C.T_BRIDGE
        if ent is not None and ent.name == "Water Platform":
            return C.T_WATER_PLATFORM
        return self.grid.tiles[y][x]

    def build_effective_grid(self):
        return [
            [self.effective_tile(x, y) for x in range(C.MAP_WIDTH)]
             for y in range(C.MAP_HEIGHT)
        ]

    # ---- Commands ----
    def order_move(self, units, dest_px):
        dest_px = (dest_px[0] + self.camera_x, dest_px[1] + self.camera_y)
        gx, gy = m.to_grid(dest_px)
        for u in units:
            sx, sy = m.to_grid(u.pos())
            path = m.astar(self.build_effective_grid(), (sx, sy), (gx, gy), self.unit_locs, passable=C.PASSABLE_RULES[u.movement_type])
            if path:
                u.set_path(path)

    def order_move_grid(self, units, dest_grid):
        self.order_move(units, (dest_grid[0] * C.TILE, dest_grid[1] * C.TILE))

    def order_attack(self, units, target):
        for u in units:
            u.target = target

    # ---- Update ----
    def update(self, dt):
        roads = [b for b in self.buildings if b.name == 'Road']
        roads_loc = []
        if len(roads) > 0:
            
            for i in roads:
                roads_loc.append(i.pos_grid())

        # Update units
        for u in self.units:
            if not u.dead:
                
                if u.pos_grid() in roads_loc:
                    u.speed_modifier = 2.0
                else:
                    u.speed_modifier = 1.0
                u.update(dt, self)

        for building in self.buildings:
            if isinstance(building, Landmine):
                building.check_trigger(self)

        for u in self.units:
            if u.dead:
                self.rubbles.append(Rubble(x=u.x, y=u.y, radius=u.radius, value=u.rubble_value))

        for b in self.buildings:
            if b.dead:
                self.rubbles.append(Rubble(x=b.x, y=b.y, radius=b.radius, value=b.rubble_value))

        # Remove dead
        self.units = [u for u in self.units if not u.dead]
        self.buildings = [b for b in self.buildings if not b.dead and not b.sold]
        self.rubbles = [r for r in self.rubbles if r.work_done <= r.clear_work]

        # Update buildings
        for b in self.buildings:
            if not b.dead and not b.sold:
                b.update(dt, self)

        for i in self.player_mat:
            self.recalculate_storage_capacity(i)
            self.recalculate_power_capacity(i)

        # AI
        self.update_ai(dt)

        # Update what's occupied
        self.occupied_tiles()

        if self.selected_units:
            if self.selected_units[0].name == 'Surveyor':
                self.resource_mode = True
            else:
                self.resource_mode = False


    def update_positons(self, camera_x, camera_y):
        for u in self.units:
            u.update_position(camera_x, camera_y)
        for b in self.buildings:
            b.update_position(camera_x, camera_y)

    def update_ai(self, dt):
        for team in C.AI_TEAMS:
            self.ai_timers[team] -= dt
            if self.ai_timers[team] <= 0:
                # Simple behavior:
                # - If they have money, queue soldier at base; sometimes build barracks
                # - Command soldiers to move toward player's base
                money = self.player_mat[team].money
                base = next((b for b in self.buildings if b.team == team and b.kind=="base"), None)
                barracks = next((b for b in self.buildings if b.team == team and b.kind=="barracks"), None)
                tank_factory = next((b for b in self.buildings if b.team == team and b.kind=="tank_factory"), None)

                if base:

                    barracks_count = 1 ## Added One for Logic Reasons
                    for b in self.buildings:
                        if b.team == team and b.kind == "barracks":
                            barracks_count += 1
                    # Less Likely the more barracks you build
                    if self.player_mat[team].money >= C.COST_BARRACKS and random.random() < 1/(barracks_count/2):
                        # find a nearby free tile
                        gx, gy = m.to_grid(base.pos())
                        count = 0
                        for _ in range(10):
                            ox = random.randint(-3,3)
                            oy = random.randint(-3,3)
                            tx, ty = gx+ox, gy+oy
                            if not m.in_bounds(tx, ty): continue
                            if self.grid.tiles[ty][tx]!=C.T_GRASS: continue
                            if m.is_occupied(self.tile_map, tx, ty): continue
                            if self.grid.tiles[ty][tx] == C.T_GRASS:
                                px, py = m.tile_center(tx, ty)
                                self.spawn_building(team, px, py, "Barracks")
                                self.player_mat[team].money -= C.COST_BARRACKS
                                break
                # 30% chance to build a tank factory near base if enough money
                    if self.player_mat[team].money >= C.COST_TANK_FACTORY and random.random() < 0.3:
                        # find a nearby free tile
                        gx, gy = m.to_grid(base.pos())
                        count = 0
                        for _ in range(10):
                            ox = random.randint(-3,3)
                            oy = random.randint(-3,3)
                            tx, ty = gx+ox, gy+oy
                            if not m.in_bounds(tx, ty): continue
                            if self.grid.tiles[ty][tx]!=C.T_GRASS: continue
                            if m.is_occupied(self.tile_map, tx, ty): continue
                            if self.grid.tiles[ty][tx] == C.T_GRASS:
                                px, py = m.tile_center(tx, ty)
                                self.spawn_building(team, px, py, "Tank Factory")
                                self.player_mat[team].money -= C.COST_TANK_FACTORY
                                break

                if barracks:
                    # queue a soldier somewhere (base or any barracks)
                    target_build = random.choice([b for b in self.buildings if b.team==team and b.kind=="barracks"])
                    if self.player_mat[team].money >= C.COST_SOLDIER and random.random() < 0.3:
                        target_build.queue.append("Soldier")
                        target_build.queue_time = C.ENTITY_STATS["Soldier"]["build_time"] if len(target_build.queue)==1 else target_build.queue_time
                        self.player_mat[team].money -= C.COST_SOLDIER
                        break

                    # Rally soldiers toward player's base
                    pbase = self.player_base

                    pbase = random.choice([b for b in self.buildings if b.team==C.PLAYER_TEAM])

                    if pbase:
                        #gx, gy = m.to_grid(pbase.pos())
                        for u in self.units:
                            if u.team==team and u.kind=="soldier" and (not u.path_px):
                                choice = random.choice(["Unit", "Building"])

                                # If no Buildings pick a Unit
                                if len([b for b in self.buildings if b.team==C.PLAYER_TEAM]) == 0:
                                    choice = "Unit"

                                # If no Units pick a building
                                if len([b for b in self.units if b.team==C.PLAYER_TEAM]) == 0:
                                    choice = "Building"

                                if choice == "Unit":
                                    dest = self.find_nearest_unit(C.PLAYER_TEAM, u.pos())
                                    gx, gy = m.to_grid(dest.pos())
                                    sx, sy = m.to_grid(u.pos())
                                    path = m.astar(self.grid.tiles, (sx, sy), (gx, gy), self.unit_locs, passable=C.PASSABLE_RULES[u.movement_type])
                                    if path:
                                        u.set_path(path)
                                elif choice == "Building":
                                    dest = self.find_nearest_building(C.PLAYER_TEAM, u.pos())
                                    gx, gy = m.to_grid(dest.pos())
                                    sx, sy = m.to_grid(u.pos())
                                    path = m.astar(self.grid.tiles, (sx, sy), (gx, gy), self.unit_locs, passable=C.PASSABLE_RULES[u.movement_type])
                                    if path:
                                        u.set_path(path)
                if tank_factory:
                    # queue a soldier somewhere (base or any barracks)
                    target_build = random.choice([b for b in self.buildings if b.team==team and b.kind=="tank_factory"])
                    if self.player_mat[team].money >= C.COST_TANK:
                        target_build.queue.append("Tank")
                        target_build.queue_time = C.ENTITY_STATS["Tank"]["build_time"] if len(target_build.queue)==1 else target_build.queue_time
                        self.player_mat[team].money -= C.COST_TANK
                        break

                    # Rally soldiers toward player's base
                    pbase = self.player_base

                    pbase = random.choice([b for b in self.buildings if b.team==C.PLAYER_TEAM])

                    

                    if pbase:
                        #gx, gy = m.to_grid(pbase.pos())
                        for u in self.units:
                            if u.team==team and u.kind=="tank" and (not u.path_px):
                                choice = random.choice(["Unit", "Building"])

                                if len([b for b in self.buildings if b.team==C.PLAYER_TEAM]) == 0:
                                    choice = "Unit"

                                if len([b for b in self.units if b.team==C.PLAYER_TEAM]) == 0:
                                    choice = "Building"

                                if choice == "Unit":
                                    dest = self.find_nearest_unit(C.PLAYER_TEAM, u.pos())
                                    gx, gy = m.to_grid(dest.pos())
                                    sx, sy = m.to_grid(u.pos())
                                    path = m.astar(self.grid.tiles, (sx, sy), (gx, gy), self.unit_locs, passable=C.PASSABLE_RULES[u.movement_type])
                                    if path:
                                        u.set_path(path)
                                elif choice == "Building":
                                    dest = self.find_nearest_building(C.PLAYER_TEAM, u.pos())
                                    gx, gy = m.to_grid(dest.pos())
                                    sx, sy = m.to_grid(u.pos())
                                    path = m.astar(self.grid.tiles, (sx, sy), (gx, gy), self.unit_locs, passable=C.PASSABLE_RULES[u.movement_type])
                                    if path:
                                        u.set_path(path)
                # Re-arm timer
                self.ai_timers[team] = random.uniform(4.0, 8.0)

    # ---- Drawing ----
    def draw(self, surf, font):
        self.grid.draw(surf, self.camera_x, self.camera_y)

        self.menu.draw(surf, font)

        surf.blit(self.minimap.render(self.units, self.buildings, camera_x=self.camera_x, camera_y=self.camera_y), (4, 580))

        # Draw units
        for r in self.rubbles:
            if r.pos_camera(self.camera_x, self.camera_y)[0] < 0 or r.pos_camera(self.camera_x, self.camera_y)[0] > C.SCREEN_WIDTH or r.pos_camera(self.camera_x, self.camera_y)[1] < 0 or r.pos_camera(self.camera_x, self.camera_y)[1] > C.HEIGHT:
                continue
            r.draw(surf, font, self.camera_x, self.camera_y)

        # Draw buildings
        for b in self.buildings:
            if b.pos_camera(self.camera_x, self.camera_y)[0] < 0 or b.pos_camera(self.camera_x, self.camera_y)[0] > C.SCREEN_WIDTH or b.pos_camera(self.camera_x, self.camera_y)[1] < 0 or b.pos_camera(self.camera_x, self.camera_y)[1] > C.HEIGHT:
                continue
            if isinstance(b, Landmine):
                b.draw(surf, font, self.camera_x, self.camera_y, C.PLAYER_TEAM)
            else:
                b.draw(surf, font, self.camera_x, self.camera_y)

        # Draw units
        for u in self.units:
            if u.pos_camera(self.camera_x, self.camera_y)[0] < 0 or u.pos_camera(self.camera_x, self.camera_y)[0] > C.SCREEN_WIDTH or u.pos_camera(self.camera_x, self.camera_y)[1] < 0 or u.pos_camera(self.camera_x, self.camera_y)[1] > C.HEIGHT:
                continue
            u.draw(surf, font, self.camera_x, self.camera_y)

        # selection rectangle
        if self.selection_rect:
            pygame.draw.rect(surf, (255,255,255), self.selection_rect, 1)

        # build ghost
        if self.build_mode or self.sell_mode:
            mx, my = pygame.mouse.get_pos()
            s_mx = (mx - C.UNIT_MENU_WIDTH + self.camera_x)
            s_my = my + self.camera_y
            tx, ty = m.to_grid((mx, my))
            s_tx, s_ty = m.to_grid((s_mx, s_my))
            px, py = m.tile_center(tx, ty)
            s_px, s_py = m.tile_center(s_tx, s_ty)

            if not self.big_build_mode:

                # Square on Position
                rect = pygame.Rect(0,0,C.TILE,C.TILE)
                rect.center = (px, py)

                valid_terrain = C.ENTITY_STATS[self.build_name]["valid_terrain"]

                if s_tx >= C.MAP_WIDTH or s_tx < 0 or s_ty >= C.MAP_HEIGHT or s_ty < 0:
                    occupied_test = False
                else:
                    ent = self.entity_at(s_tx, s_ty)
                    if ent is not None and ent.name in ["Bridge", "Water Platform"]:
                        occupied_test = True
                    else:
                        occupied_test = not self.tile_map[s_tx][s_ty].occupied

                valid = m.in_bounds(s_tx, s_ty) and self.effective_tile(s_tx, s_ty) in valid_terrain and occupied_test
                self.ghost_valid = valid
                self.ghost_pos = (s_px, s_py)
                pygame.draw.rect(surf, (200,200,200) if valid else (200,80,80), rect, 2)

            elif self.big_build_mode:
                # Square on Position
                rect = pygame.Rect(0,0,C.TILE * 2, C.TILE * 2)
                rect.center = (px + (C.TILE / 2), py + (C.TILE / 2))

                valid_terrain = C.ENTITY_STATS[self.build_name]["valid_terrain"]


                if s_tx + 1 >= C.MAP_WIDTH or s_tx < 0 or s_ty + 1 >= C.MAP_HEIGHT or s_ty < 0:
                    occupied_test = False
                else:
                    ent_tf = self.entity_at(s_tx, s_ty)
                    ent_tr = self.entity_at(s_tx + 1, s_ty)
                    ent_bf = self.entity_at(s_tx, s_ty + 1)
                    ent_br = self.entity_at(s_tx + 1, s_ty + 1)

                    if (ent_tf is None or ent_tf.name in ["Water Platform"]) and \
                        (ent_tr is None or ent_tr.name in ["Water Platform"]) and \
                            (ent_bf is None or ent_bf.name in ["Water Platform"]) and \
                                (ent_br is None or ent_br.name in ["Water Platform"]):
                        occupied_test = True
                    else:
                        occupied_test = not self.tile_map[s_tx][s_ty].occupied and not self.tile_map[s_tx + 1][s_ty].occupied \
                            and not self.tile_map[s_tx][s_ty + 1].occupied and not self.tile_map[s_tx + 1][s_ty + 1].occupied

                valid = m.in_bounds(s_tx, s_ty) and m.in_bounds(s_tx + 1, s_ty) and m.in_bounds(s_tx, s_ty + 1) and m.in_bounds(s_tx + 1, s_ty + 1) \
                    and self.effective_tile(s_tx, s_ty) in valid_terrain and self.effective_tile(s_tx + 1, s_ty) in valid_terrain \
                        and self.effective_tile(s_tx, s_ty + 1) in valid_terrain and self.effective_tile(s_tx + 1, s_ty + 1) in valid_terrain \
                    and occupied_test
                
                self.ghost_valid = valid
                self.ghost_pos = (s_px + (C.TILE / 2), s_py + (C.TILE / 2))
                pygame.draw.rect(surf, (200,200,200) if valid else (200,80,80), rect, 2)



        # UI
        pygame.draw.rect(surf, (0,0,0), (0, C.HEIGHT, C.WIDTH, C.BOTTOM_MENU_HEIGHT))
        money_text = font.render(f"Money: {int(self.player_mat[C.PLAYER_TEAM].money)}/{self.player_mat[C.PLAYER_TEAM].storage_money}  "
                                 f"Fuel:  {int(self.player_mat[C.PLAYER_TEAM].fuel)}/{self.player_mat[C.PLAYER_TEAM].storage_fuel}   "
                                 f"Gold:  {int(self.player_mat[C.PLAYER_TEAM].gold)}/{self.player_mat[C.PLAYER_TEAM].storage_gold}   "
                                 f"Power: {int(self.player_mat[C.PLAYER_TEAM].power_usage)}/{self.player_mat[C.PLAYER_TEAM].total_power}", True, (255,255,255))
        surf.blit(money_text, (6, C.HEIGHT+8))

        mx, my = pygame.mouse.get_pos()
        s_mx = (mx - C.UNIT_MENU_WIDTH + self.camera_x)
        s_my = my + self.camera_y
        s_tx, s_ty = m.to_grid((s_mx, s_my))

        current_pos_text = font.render(f"({s_tx}, {s_ty})", True, (255, 255, 255))
        surf.blit(current_pos_text, (C.SCREEN_WIDTH - 6, C.HEIGHT+8))

        if self.help_on:
            self.draw_help(surf, font)

        if self.resource_mode:
            self.grid.draw_resources(surf, font, self.camera_x, self.camera_y)

        if self.pause_mode:
            pause_font = pygame.font.SysFont(None, 50)
            pause_text = pause_font.render("Game Paused", True, (255, 255, 255))
            surf.blit(pause_text, (C.SCREEN_HEIGHT / 2, C.HEIGHT / 2))


    def draw_help(self, surf, font):
        lines = [
            "Controls: Left-drag = select units | Right-click = move/attack/harvest | ESC = cancel/clear",
            f"B: place Barracks ({C.COST_BARRACKS}) | S: train Soldier at Barracks ({C.COST_SOLDIER})",
            f"W: place Tank Factory ({C.COST_TANK_FACTORY}) | T: train Tank at Tank Factory ({C.COST_TANK})",
            f"R: Show the Resource Map | C: Build Base ({C.COST_BASE}) | F1: toggle help",
        ]
        y = 6
        for line in lines:
            text = font.render(line, True, (0,0,0))
            pygame.draw.rect(surf, (255,255,255), (6, y-2, text.get_width()+8, text.get_height()+4))
            surf.blit(text, (10, y))
            y += text.get_height() + 6
