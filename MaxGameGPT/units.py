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
        self.image = pygame.image.frombytes(image.tobytes(), image.size, image.mode).convert_alpha()
        self.current_angle = 0

        self.local_labels = ['Move', 'Attack', 'Stop']

        if self.carry_max > 0:
            self.local_labels.append('X-fer')



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
        if not self.harvesting:
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
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y

        rotated_image = pygame.transform.rotate(self.image, self.current_angle)
        new_rect = rotated_image.get_rect(center=(int(screen_x), int(screen_y)))

        surf.blit(rotated_image, new_rect)

        self.draw_health_bar(surf, camera_x, camera_y)
        

        
        if self.selected:

            # Draw Box in top corner showing hp, speed, ammo, and carry/shots
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


            # Draw box on the top right of the unit with labels

            # Don't draw the box if the unit is moving
            if len(self.path_px) == 0:
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

