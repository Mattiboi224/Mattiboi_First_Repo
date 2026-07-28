from dataclasses import dataclass, asdict, fields
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

@dataclass(eq=False)  # eq=False: keep default identity comparison, don't let
                       # dataclass generate __eq__/__hash__ from pygame Surfaces/Rects
class Entity(pygame.sprite.Sprite):
    team: int
    x: float
    y: float
    name: str

 
    def __post_init__(self):

        pygame.sprite.Sprite.__init__(self)
        
        self.id = gen_id()

        stats = C.ENTITY_STATS[self.name]

        self.hp = self.max_hp = stats["hp"]
        self.armour = stats["armour"]
        self.kind = stats["kind"]
        self.image = stats["image"]
        self.radius = stats["radius"]
        self.rubble_value = stats["rubble_value"]

        self.dead = False
        self.unit_repair_mode = False
        self.cleaned = False

        converted_image = m.convert_image_to_team(self.team, self.name)
        self.image = pygame.image.frombytes(converted_image.tobytes(), converted_image.size, converted_image.mode).convert_alpha()

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, d):
        # Split fields into init-accepted vs init=False
        init_fields = {f.name for f in fields(cls) if f.init}
        non_init_fields = [f.name for f in fields(cls) if not f.init]

        # Build the object using only what __init__ accepts
        filtered = {k: v for k, v in d.items() if k in init_fields}
        obj = cls(**filtered)

        # Restore whatever __post_init__ would've computed, using saved values instead
        for name in non_init_fields:
            if name in d:
                setattr(obj, name, d[name])

        return obj

    def pos(self):
        return (self.x, self.y)
    
    def pos_grid(self):
        self.grid_x, self.grid_y = m.to_grid(self.pos())
        return (self.grid_x, self.grid_y)

    def take_damage(self, dmg):
        self.hp -= (dmg - self.armour)
        if self.hp <= 0:
            self.dead = True

    def repairing(self):
        if self.unit_repair_mode:
            if self.hp < self.max_hp:
                self.hp += 1

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

