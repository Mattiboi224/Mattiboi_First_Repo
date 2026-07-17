import pygame
import math
from dataclasses import dataclass, field, asdict

from entity import Entity
import Config as C
import util as m

@dataclass(eq=False)  # eq=False: keep default identity comparison, don't
                       # let dataclass generate __eq__ from pygame Surfaces/Rects
class Unit(Entity):
    name: str = "Soldier"

    # --- Runtime-only fields (not part of the constructor call) ---
    path: list = field(default_factory=list, init=False)
    path_px: list = field(default_factory=list, init=False)
    target: object = field(default=None, init=False)
    attack_cooldown: float = field(default=0.0, init=False)
    selected: bool = field(default=False, init=False)
 
    harvesting: bool = field(default=False, init=False)
    harvest_timer: float = field(default=0.0, init=False)
    carry: int = field(default=0, init=False)
    old_res: object = field(default=None, init=False)
    current_angle: float = field(default=0, init=False)

    def __post_init__(self):
        super().__post_init__()

        stats = C.ENTITY_STATS[self.name]
        self.attacking_unit = stats.get("attacking_unit", False)
        self.building_unit = stats.get("building_unit", False)
        self.transfer_unit = stats.get("transfer_unit", False)
        self.speed = self.max_speed = stats["speed"]

        self.labels = [f'hp: {self.hp}/{self.max_hp}', f'speed: {self.speed}/{self.max_speed}']

        if self.attacking_unit:
            self.atk = stats["atk"]
            self.range = stats["range"]
            # Range feels better
            self.range += 5
            self.ammo = self.max_ammo = stats["ammo"]
            self.shots = self.max_shots = stats["shots"]
            self.labels.append(f'ammo: {self.ammo}/{self.max_ammo}')
            self.labels.append(f'shots: {self.shots}/{self.max_shots}')

        self.carry_max = stats.get("cargo", 0)

        self.local_labels = ['Move', 'Stop']

        if self.attacking_unit:
            self.local_labels.append('Attack')

        if self.transfer_unit > 0:
            self.local_labels.append('X-fer')
            self.labels.append(f'carry: {self.carry}/{self.carry_max}')
        
        if self.building_unit:
            self.local_labels.append('Build')

        self.rects = []
        for i in range(len(self.labels)):   # or a fixed number of buttons
            rect = pygame.Rect(
                20,
                40 + 10 + i * (C.UNIT_PROP_HEIGHT),
                C.UNIT_MENU_WIDTH - 40,
                C.BTN_HEIGHT
            )
            self.rects.append(rect)

    def set_path(self, path_tiles):
        self.path = path_tiles
        # convert to centers
        self.path_px = [m.tile_center(tx, ty) for (tx,ty) in self.path]

    def calculate_angle(self):
        if len(self.path_px) >= 1:
            tx, ty = self.path_px[0]
            dx = tx - self.x
            dy = ty - self.y
            self.current_angle = math.degrees(math.atan2(-dy, dx))  # negative dy because y-axis is inverted in Pygame

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
        if not self.harvesting and self.attacking_unit:
            enemy = game.find_nearest_enemy(self.team, self.pos(), within=self.range)
            if enemy:
                self.try_attack(enemy, dt)

                return
        
        self.calculate_angle()


    def try_attack(self, enemy, dt):
        d = m.dist(self.pos(), enemy.pos())
        if d <= self.range and self.attack_cooldown <= 0:
            enemy.take_damage(self.atk)
            self.attack_cooldown = 0.8
            self.ammo -= 1

    def draw(self, surf, font, camera_x, camera_y):
        
        # Calculate screen position
        screen_x = self.x - camera_x + C.UNIT_MENU_WIDTH
        screen_y = self.y - camera_y

        rotated_image = pygame.transform.rotate(self.image, self.current_angle)
        new_rect = rotated_image.get_rect(center=(int(screen_x), int(screen_y)))

        surf.blit(rotated_image, new_rect)

        self.draw_health_bar(surf, camera_x, camera_y)
        

        
        if self.selected:

            # Box Around Unit to show what's selected
            rect = pygame.Rect(0,0,C.TILE,C.TILE)
            rect.center = (screen_x, screen_y)
            pygame.draw.rect(surf, (200,200,200), rect, 2)

            # Draw Box in top corner showing hp, speed, ammo, and carry/shots
            pygame.draw.rect(surf, C.MENU_BG, (0, 40, C.UNIT_MENU_WIDTH, C.UNIT_MENU_HEIGHT))
            
            buttons = list(zip(self.labels, self.rects))

            for label, rect in buttons:
                # Draw text
                text = font.render(label, True, C.TEXT_COLOR)
                surf.blit(text, (rect.x, rect.y))


            # Draw box on the top right of the unit with labels

            # Don't draw the box if the unit is moving
            if len(self.path_px) == 0:

                # Menu on the side
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

