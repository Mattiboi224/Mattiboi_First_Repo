import Config
import pygame
import util as m

# ------------------ ENTITIES ------------------
NEXT_ID = 1
def gen_id():
    global NEXT_ID
    i = NEXT_ID
    NEXT_ID += 1
    return i

class Entity(pygame.sprite.Sprite):
    def __init__(self, team, x, y, image, radius=12):
        self.id = gen_id()
        self.team = team
        self.x = x
        self.y = y
        self.radius = radius
        self.hp = 1
        self.max_hp = 1
        self.image = image
        self.dead = False

    def pos(self):
        return (self.x, self.y)

    def take_damage(self, dmg):
        self.hp -= dmg
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

