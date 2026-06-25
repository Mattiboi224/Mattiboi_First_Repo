

import Config as C
import pygame

class Menu:
    def __init__(self):

        # Menu buttons
        self.buildings_labels = ["Base", "Barracks", "Tank Factory"]
        self.unit_labels = ["Soldier", "Tank", "Ammo Truck"]
        self.helpful_labels = ["Sell", "Repair"]
        self.labels = self.buildings_labels + self.unit_labels + self.helpful_labels

        self.buttons = []
    
        # Create button rects
        for i, label in enumerate(self.labels):
            rect = pygame.Rect(
                C.WIDTH - C.MENU_WIDTH + 20,
                50 + i * (C.BTN_HEIGHT + C.PADDING),
                C.MENU_WIDTH - 40,
                C.BTN_HEIGHT
            )
            self.buttons.append((label, rect))

    def draw(self, screen, font):
        pygame.draw.rect(screen, C.MENU_BG, (C.WIDTH - C.MENU_WIDTH, 0, C.MENU_WIDTH, C.HEIGHT))

        # Mouse position
        mx, my = pygame.mouse.get_pos()
        
        for label, rect in self.buttons:
            # Hover effect
            color = C.BTN_HOVER if rect.collidepoint(mx, my) else C.BTN_COLOR
            pygame.draw.rect(screen, color, rect, border_radius=8)

            # Draw text
            text = font.render(label, True, C.TEXT_COLOR)
            screen.blit(text, (rect.x + 20, rect.y + 15))

            # If it has a cost add it
            if label in C.UNIT_STATS:
                text = font.render(str(C.UNIT_STATS[label]["cost"]), True, C.TEXT_COLOR)
                screen.blit(text, (rect.x + C.MENU_WIDTH - 70, rect.y + 10))