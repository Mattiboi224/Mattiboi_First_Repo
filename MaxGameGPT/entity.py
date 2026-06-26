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
    def __init__(self, team, x, y, image, kind, radius=12):
        self.id = gen_id()
        self.team = team
        self.x = x
        self.y = y
        self.kind = kind
        self.radius = radius
        self.hp = 1
        self.max_hp = 1
        self.image = image
        self.dead = False
        
        if kind == "tank":
            self.armour = C.SOLDIER_ARMOUR
        elif kind == "tank":
            self.armour = C.TANK_ARMOUR
        elif kind == "ammo_truck":
            self.armour = C.AMMO_TRUCK_ARMOUR
        elif kind == "base":
            self.armour = C.BASE_ARMOUR
        elif kind == "barracks":
            self.armour = C.BARRACKS_ARMOUR
        elif kind == "tank_factory":
            self.armour = C.TANK_FACTORY_ARMOUR

    def pos(self):
        return (self.x, self.y)

    def take_damage(self, dmg):
        self.hp -= dmg - self.armour
        if self.hp <= 0:
            self.dead = True

    def draw_health_bar(self, surf):
        if self.hp >= self.max_hp: return
        w = 24
        h = 4
        x = self.x - w//2
        y = self.y - self.radius - 8
        pct = m.clamp(self.hp / self.max_hp, 0, 1)
        pygame.draw.rect(surf, (0,0,0), (x-1, y-1, w+2, h+2))
        pygame.draw.rect(surf, (180,30,30), (x, y, w, h))
        pygame.draw.rect(surf, (30,180,30), (x, y, int(w*pct), h))

