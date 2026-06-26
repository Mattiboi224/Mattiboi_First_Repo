import pygame
import math

from entity import Entity
import Config as C
import util as m

# pyright: ignore[reportMissingImports]

class Unit(Entity):
    def __init__(self, team, x, y, image, kind="soldier"):
        super().__init__(team, x, y, image, kind, radius=12)
        self.kind = kind
        if kind == "tank":
            self.hp = self.max_hp = C.TANK_HP
            self.atk = C.TANK_ATK
            self.range = C.TANK_RANGE
            self.speed = self.max_speed =C.TANK_SPEED
            self.armour = C.TANK_ARMOUR
            self.ammo = self.max_ammo = C.TANK_AMMO
            self.shots = self.max_shots = C.TANK_SHOTS
    
        elif kind == "ammo_truck":
            self.hp = self.max_hp = C.AMMO_TRUCK_HP
            self.atk = C.AMMO_TRUCK_ATK
            self.range = C.AMMO_TRUCK_RANGE
            self.speed = self.max_speed = C.AMMO_TRUCK_SPEED
            self.armour = C.AMMO_TRUCK_ARMOUR
            self.ammo = self.max_ammo = C.AMMO_TRUCK_AMMO
            self.shots = self.max_shots = C.AMMO_TRUCK_SHOTS

        else:
            self.hp = self.max_hp = C.SOLDIER_HP
            self.atk = C.SOLDIER_ATK
            self.range = C.SOLDIER_RANGE
            self.speed = self.max_speed = C.SOLDIER_SPEED
            self.armour = C.SOLDIER_ARMOUR
            self.ammo = self.max_ammo = C.SOLDIER_AMMO
            self.shots = self.max_shots = C.SOLDIER_SHOTS

        if kind == "ammo_truck":
            self.carry_max = C.AMMO_TRUCK_CARGO
        else:
            self.carry_max = 0

        self.path = []
        self.path_px = []
        self.target = None
        self.attack_cooldown = 0.0
        self.selected = False
        # Harvesting
        self.harvesting = False
        self.harvest_timer = 0.0
        self.carry = 0
        self.old_res = None
        self.image = pygame.image.fromstring(image.tobytes(), image.size, image.mode)#.convert_alpha()

        self.labels = [f'hp: {self.hp}/{self.max_hp}',f'ammo: {self.ammo}/{self.max_ammo}', f'shots: {self.shots}/{self.max_shots}', f'speed: {self.speed}/{self.max_speed}', f'carry: {self.carry}/{self.carry_max}']

        self.rects = []
        for i in range(len(self.labels)):   # or a fixed number of buttons
            rect = pygame.Rect(
                20,
                10 + i * (C.UNIT_PROP_HEIGHT),
                C.UNIT_MENU_WIDTH - 40,
                C.BTN_HEIGHT
            )
            self.rects.append(rect)

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
            self.ammo -= 1

    def draw(self, surf, font):
        # col = C.TEAM_COLORS.get(self.team, (200,200,200))
        # rect = pygame.Rect(0,0, C.TILE, C.TILE)
        # rect.center = (int(self.x), int(self.y))
        # pygame.draw.rect(surf, col, rect)
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

        # Draw Box in top corner showing hp, speed, ammo, and carry/shots
        if self.selected:

            pygame.draw.rect(surf, C.MENU_BG, (0, 0, C.UNIT_MENU_WIDTH, C.UNIT_MENU_HEIGHT))

            if self.carry_max > 0:
                self.labels = [f'hp: {self.hp}/{self.max_hp}',f'ammo: {self.ammo}/{self.max_ammo}', f'shots: {self.shots}/{self.max_shots}', f'speed: {self.speed}/{self.max_speed}', f'carry: {self.carry}/{self.carry_max}']
            else:
                self.labels = [f'hp: {self.hp}/{self.max_hp}',f'ammo: {self.ammo}/{self.max_ammo}', f'shots: {self.shots}/{self.max_shots}', f'speed: {self.speed}/{self.max_speed}', '']
            
            buttons = list(zip(self.labels, self.rects))

            for label, rect in buttons:
                # Draw text
                text = font.render(label, True, C.TEXT_COLOR)
                surf.blit(text, (rect.x, rect.y))
            
