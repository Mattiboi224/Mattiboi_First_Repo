import Config as C
import pygame
import game

pygame.init()
font = pygame.font.SysFont(None, 22)
screen = pygame.display.set_mode((C.WIDTH, C.HEIGHT+28))

game = game.Game()

running = True
while running:

    # ------------- INPUT -------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    labels = ['hp','ammo', 'shots', 'speed', 'carry']

    # ------------- DRAW -------------
    #screen.fill((30, 30, 30))
    #game.draw(screen, font)
    pygame.display.flip()

    buttons = []
    # Create button rects
    for i, label in enumerate(labels):
        rect = pygame.Rect(
            0 + 20,
            50 + i * (C.UNIT_PROP_HEIGHT + C.PADDING),
            C.UNIT_MENU_WIDTH - 40,
            C.BTN_HEIGHT
        )
        buttons.append((label, rect))

    for label, rect in buttons:
        # Draw text
        text = font.render(label, True, C.TEXT_COLOR)
        screen.blit(text, (rect.x + 20, rect.y + 15))
