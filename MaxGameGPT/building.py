import pygame
from entity import Entity
import Config as C
import random
import math
import util as m
from dataclasses import dataclass, field

@dataclass(eq=False)  # eq=False: keep default identity comparison, don't
                       # let dataclass generate __eq__ from pygame Surfaces/Rects
class Building(Entity):
    name: str = "base"

    no_queue: bool = False

    # --- Runtime-only fields ---
    queue: list = field(default_factory=list, init=False)
    queue_time: float = field(default=0.0, init=False)
    sold: bool = field(default=False, init=False)
    count: int = field(default=0, init=False)
    selected: bool = field(default=False, init=False)

    def __post_init__(self):
        
        super().__post_init__()

        self.building = True

        stats = C.ENTITY_STATS[self.name]
        self.build_time = stats["build_time"]
        self.power_used = stats.get("power_used", 0)
        self.power_given = stats.get("power_given", 0)
        self.power_required = stats.get("power_required", False)
        self.depletion_time = stats.get("depletion_time", 0)
        self.power_supply = stats.get("power_supply", False)
        self.resource_used = stats.get("resource_used", 0)
        self.attacking_building = stats.get("attacking_building", False)

        self.stat_fields = ['name', 'hp']

        if self.power_required:
            self.stat_fields.append('power used')
        if self.power_supply:
            self.stat_fields.append('power supplied')
        if self.attacking_building:
            self.stat_fields += ['ammo', 'shots']

        if self.no_queue:
            self.building = False
            self.build_time = 0.0

        if self.attacking_building:
            barrel_image_path = C.entity_image_path(stats["kind"] + "_barrel", stats["category"])
            self.barrel_image = pygame.image.load(barrel_image_path).convert_alpha()
            self.atk = stats["atk"]
            self.range = stats["range"]
            # Range feels better
            self.range += 5
            self.ammo = self.max_ammo = stats["ammo"]
            self.shots = self.max_shots = stats["shots"]
            self.current_angle = 0
            self.attack_cooldown = 0.0

        if self.radius == C.TILE / 2:
            build_image_convert = m.convert_image_to_team(self.team, 'Construction')
            self.build_image = pygame.image.frombytes(build_image_convert.tobytes(), build_image_convert.size, build_image_convert.mode).convert_alpha()
            rubble_image_convert = m.convert_image_to_team(self.team, 'Rubble')
            self.rubble_image = pygame.image.frombytes(rubble_image_convert.tobytes(), rubble_image_convert.size, rubble_image_convert.mode).convert_alpha()
        elif self.radius == C.TILE:
            build_image_convert = m.convert_image_to_team(self.team, 'Big Construction')
            self.build_image = pygame.image.frombytes(build_image_convert.tobytes(), build_image_convert.size, build_image_convert.mode).convert_alpha()
            rubble_image_convert = m.convert_image_to_team(self.team, 'Big Rubble')
            self.rubble_image = pygame.image.frombytes(rubble_image_convert.tobytes(), rubble_image_convert.size, rubble_image_convert.mode).convert_alpha()    
        

        self.resupply_time = C.MINERAL_SUPPLY_TIME

        if self.building:
            self.curr_image = self.build_image
        else:
            self.curr_image = self.image

        if self.kind in ("base", "storage_unit", "fuel_tank", "gold_vault"):
            self.storage = True
            self.storage_amount = 0
            self.resource_storage_type = stats["resource_storage_type"]
        else:
            self.storage = False

        if self.kind == "base":
            self.supply = True
        else:
            self.supply = False

        self.local_labels = []
        if self.kind == "base":
            self.local_labels.append('Build')
        if self.storage:
            self.local_labels.append('X-fer')
        if self.attacking_building:
            self.local_labels.append('Attack')
        self.local_labels.append('Stop')

        self.rects = []
        for i in range(len(self.stat_fields)):   # or a fixed number of buttons
            rect = pygame.Rect(
                10,
                40 + 10 + i * (C.UNIT_PROP_HEIGHT),
                C.UNIT_MENU_WIDTH - 40,
                C.BTN_HEIGHT
            )
            self.rects.append(rect)

    def pos(self):
        return (self.x, self.y)

    def grid_pos(self):
        return m.to_grid(self.pos())

    def assign_tile(self, tiles_mat):
        self.Tile = []

        if self.radius == C.TILE / 2:
            x, y = m.to_grid(self.pos())
            self.Tile.append(tiles_mat[x][y])
        elif self.radius == C.TILE:
            points = m.occupied_by_unit(self)
            for x,y in points:
                self.Tile.append(tiles_mat[x][y])

    @property
    def provides_storage(self):
        return self.storage_amount

    def try_attack(self, enemy, dt):
        d = m.dist(self.pos(), enemy.pos())
        if d <= self.range and self.attack_cooldown <= 0:
            enemy.take_damage(self.atk)
            self.attack_cooldown = 0.8
            self.ammo -= 1

    def calculate_angle(self, enemy):
        
        tx, ty = enemy.pos()

        dx = tx - self.x
        dy = ty - self.y
        self.current_angle = math.degrees(math.atan2(-dy, dx))  # negative dy because y-axis is inverted in Pygame

    def get_labels(self):
        text_map = {
            'name': f'name: {self.name}',
            'hp': f'hp: {self.hp}/{self.max_hp}',
            'power used': f'power used: {getattr(self, "power_used", 0)}',
            'power supplied': f'power supplied: {getattr(self, "power_given", 0)}',
            'ammo': f'ammo: {getattr(self, "ammo", 0)}/{getattr(self, "max_ammo", 0)}',
            'shots': f'shots: {getattr(self, "shots", 0)}/{getattr(self, "max_shots", 0)}',
        }
        return [text_map[f] for f in self.stat_fields]

    def update(self, dt, game):

        if self.building:
            self.power_given = 0
            self.build_time -= dt
            if self.storage:
                self.storage_amount = 0
            if self.build_time <= 0:
                self.curr_image = self.image
                self.building = False

        if self.dead and not self.cleaned:
            self.curr_image = self.rubble_image
        
        # Use Fuel to keep power running
        if not self.building and self.power_supply:
            self.depletion_time -= dt
            if self.depletion_time < 0:
                
                # If you have enough everything is good
                if game.player_mat[self.team].fuel > self.resource_used:
                    game.player_mat[self.team].fuel -= self.resource_used
                    self.depletion_time = C.ENTITY_STATS[self.name]["depletion_time"]
                    self.power_given = C.ENTITY_STATS[self.name]["power_given"]

                else:
                    self.power_given = 0

        # Auto-target enemies in range
        
        if self.attacking_building and not self.building:
            # Attack cooldown
            if self.attack_cooldown > 0:
                self.attack_cooldown -= dt

            enemy = game.find_nearest_enemy(self.team, self.pos(), within=self.range)
            
            if enemy:
                self.calculate_angle(enemy)
                self.try_attack(enemy, dt)

                return
            

        # process production queue
        # When not constructing the building and when power isn't required or if power is required and it's online
        if not self.building and (not self.power_required or (self.power_required and game.player_mat[self.team].power_balance >= 0)):
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

                    tx, ty = m.tile_center(gx, gy)
                    game.spawn_unit(self.team, tx, ty, unit_type)
                    # reset timer if more remain
                    if self.queue:
                        self.queue_time = C.ENTITY_STATS[self.queue[0]]["build_time"]
        
            if self.supply:
                self.resupply_time -= dt

                # Every 10 Ticks Supply Money
                if self.resupply_time <= 0:

                    for t in self.Tile:

                        if t.resource_type == 'Minerals':
                            if t.resource_amount + game.player_mat[self.team].money <= game.player_mat[self.team].storage_money:
                                game.player_mat[self.team].money += t.resource_amount
                                self.resupply_time = C.MINERAL_SUPPLY_TIME
                        
                        elif t.resource_type == 'Fuel':
                            if t.resource_amount + game.player_mat[self.team].fuel <= game.player_mat[self.team].storage_fuel:
                                game.player_mat[self.team].fuel += t.resource_amount
                                self.resupply_time = C.FUEL_SUPPLY_TIME

                        elif t.resource_type == 'Gold':
                            if t.resource_amount + game.player_mat[self.team].money <= game.player_mat[self.team].storage_gold:
                                game.player_mat[self.team].gold += t.resource_amount
                                self.resupply_time = C.GOLD_SUPPLY_TIME

            count_1 = 0
            if self.storage and self.storage_amount == 0 and count_1 == 0:
                self.storage_amount = C.ENTITY_STATS[self.name]["storage_amount"]
                count_1 = 1

            count_2 = 0
            if self.storage and self.no_queue and count_2 == 0:
                self.storage_amount = C.ENTITY_STATS[self.name]["storage_amount"]
                count_2 = 1


    def draw(self, surf, font, camera_x, camera_y):
        screen_x = self.x - camera_x + C.UNIT_MENU_WIDTH
        screen_y = self.y - camera_y


        
        rect = self.curr_image.get_rect(center=(int(screen_x), int(screen_y)))
        surf.blit(self.curr_image, rect)


        if not self.dead:
            self.draw_health_bar(surf, camera_x, camera_y)

            if self.attacking_building and not self.building:

                rect = self.barrel_image.get_rect(center=(int(screen_x), int(screen_y)))

                # Rotate Barrel
                rotated_image = pygame.transform.rotate(self.barrel_image, self.current_angle)
                new_rect = rotated_image.get_rect(center=(int(screen_x), int(screen_y)))

                surf.blit(rotated_image, new_rect)

            if self.selected:

                if self.radius == C.TILE / 2:

                    # Box Around Unit to show what's selected
                    rect = pygame.Rect(0,0,C.TILE,C.TILE)
                    rect.center = (screen_x, screen_y)
                    pygame.draw.rect(surf, (200,200,200), rect, 2)

                elif self.radius == C.TILE:
                    rect = pygame.Rect(0,0,C.TILE * 2,C.TILE * 2)
                    rect.center = (screen_x, screen_y)
                    pygame.draw.rect(surf, (200,200,200), rect, 2)

                # Draw Box in top corner showing hp, speed, ammo, and carry/shots
                pygame.draw.rect(surf, C.MENU_BG, (0, 40, C.UNIT_MENU_WIDTH, C.UNIT_MENU_HEIGHT))
                
                buttons = list(zip(self.get_labels(), self.rects))

                for label, rect in buttons:
                    # Draw text
                    text = font.render(label, True, C.TEXT_COLOR)
                    surf.blit(text, (rect.x, rect.y))

                # Draw a local box
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
