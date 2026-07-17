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

    options_labels = ["Pause", "Save", "Load", "Exit"]
    options_buttons = []

    # Create options rects
    for i, label in enumerate(options_labels):
        rect = pygame.Rect(
            0 + i * (30 + 7),
            5,
            30,
            20
        )
        options_buttons.append((label, rect))


    #pygame.draw.rect(screen, C.MENU_BG, (0, 0, C.UNIT_MENU_WIDTH, C.OPTIONS_MENU_HEIGHT))

    font = pygame.font.SysFont(None, 14)

    # Mouse position
    mx, my = pygame.mouse.get_pos()

    for label, rect in options_buttons:
        # Hover effect
        color = C.BTN_HOVER if rect.collidepoint(mx, my) else (100, 100, 100)
        pygame.draw.rect(screen, color, rect, border_radius=3)

        # Draw text
        text = font.render(label, True, C.TEXT_COLOR)
        screen.blit(text, (rect.x + 4, rect.y + 4))