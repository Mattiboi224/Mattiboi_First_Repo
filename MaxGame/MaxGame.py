## Create a playing map
from enemy import Enemy
import pygame as pg
import Constants as c

## Initialise pygame
pg.init()

# Create Clock
clock = pg.time.Clock()



## Create Game Window
screen = pg.display.set_mode((c.SCREEN_WIDTH,c.SCREEN_HEIGHT))
pg.display.set_caption("MAX")

# Images
enemy_image = pg.image.load('assets/tank.png').convert_alpha()

# Create Groups
enemy_group = pg.sprite.Group()

enemy = Enemy((200,300), enemy_image)
enemy_group.add(enemy)

print(enemy)

# Game Loop
run = True

while run:

    clock.tick(c.FPS)

    screen.fill("grey100")

    # Update Groups
    enemy_group.update()

    # Draw Groups
    enemy_group.draw(screen)

    ## Event Handle
    for event in pg.event.get():
        ## Quit Program
        if event.type == pg.QUIT:
            run = False

    # Update Display
    pg.display.flip()

pg.quit()