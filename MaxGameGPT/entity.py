import Config
import pygame
import util as m
import Config as C

# ------------------ ENTITIES ------------------
NEXT_ID = 1
def gen_id():
    global NEXT_ID
    i = NEXT_ID
    NEXT_ID += 1
    return i

class Entity(pygame.sprite.Sprite):
    def __init__(self, team, x, y, image, name, radius=12):

        
        self.id = gen_id()
        self.team = team
        self.x = x
        self.y = y
        self.name = name
        self.radius = radius

        stats = C.ENTITY_STATS[name]

        self.hp = self.max_hp = stats["hp"]
        self.armour = stats["armour"]
        self.kind = stats["kind"]


        self.dead = False

        

        converted_image = m.convert_image_to_team(image, self.team, self.kind)
        self.image = pygame.image.frombytes(converted_image.tobytes(), converted_image.size, converted_image.mode).convert_alpha()
        
        

        

    def pos(self):
        return (self.x, self.y)
    
    def pos_grid(self):
        self.grid_x, self.grid_y = m.to_grid(self.pos())
        return (self.grid_x, self.grid_y)

    def take_damage(self, dmg):
        self.hp -= (dmg - self.armour)
        if self.hp <= 0:
            self.dead = True

    def pos_camera(self, camera_x, camera_y):
        return (self.x - camera_x, self.y - camera_y)

    def update_position(self, camera_x, camera_y):
        self.x = self.x - camera_x
        self.y = self.y - camera_y

    def draw_health_bar(self, surf, camera_x, camera_y):
        if self.hp >= self.max_hp: return
        w = 24
        h = 4
        x = self.x - camera_x - w//2 + C.UNIT_MENU_WIDTH
        y = self.y - camera_y - self.radius - 8
        pct = m.clamp(self.hp / self.max_hp, 0, 1)
        pygame.draw.rect(surf, (0,0,0), (x-1, y-1, w+2, h+2))
        pygame.draw.rect(surf, (180,30,30), (x, y, w, h))
        pygame.draw.rect(surf, (30,180,30), (x, y, int(w*pct), h))

