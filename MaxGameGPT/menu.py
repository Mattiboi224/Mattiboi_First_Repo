

import Config as C
import pygame

class Menu:
    def __init__(self):

        # Menu buttons
        self.buildings_labels = [name for name, stats in C.ENTITY_STATS.items() if stats["category"] == "building"]
        self.buildings_labels.remove("Construction")
        self.unit_labels = [name for name, stats in C.ENTITY_STATS.items() if stats["category"] == "unit"]
        self.helpful_labels = ["Sell", "Repair"]
        self.labels = self.buildings_labels + self.unit_labels + self.helpful_labels

        BTN_HEIGHT = ((C.HEIGHT - 20)// len(self.labels)) - C.PADDING

        #Button height = (Height / no_of_buttons) - padding

        self.buttons = []
    
        # Create button rects
        for i, label in enumerate(self.labels):
            rect = pygame.Rect(
                C.WIDTH - C.MENU_WIDTH + 20,
                20 + (BTN_HEIGHT + C.PADDING) * i,
                C.MENU_WIDTH - 40,
                BTN_HEIGHT
            )
            self.buttons.append((label, rect))

    # Options for the Units
    def unit_options(self):
        unit_options = ["Move", "Attack", "Stop"]

    # When select a unit, show the properties of that unit
    def unit_properties_menu(self, screen):

        pygame.draw.rect(screen, C.UNIT_MENU_BG, (0, 0, C.UNIT_MENU_WIDTH, C.HEIGHT))
        


    def right_side_menu(self, screen, font):
        pygame.draw.rect(screen, C.MENU_BG, (C.WIDTH - C.MENU_WIDTH, 0, C.MENU_WIDTH, C.HEIGHT))

        # Mouse position
        mx, my = pygame.mouse.get_pos()
        
        for label, rect in self.buttons:
            # Hover effect
            color = C.BTN_HOVER if rect.collidepoint(mx, my) else C.BTN_COLOR
            pygame.draw.rect(screen, color, rect, border_radius=8)

            # Draw text
            text = font.render(label, True, C.TEXT_COLOR)
            screen.blit(text, (rect.x + 25, rect.y + 15))

            # If it has a cost add it
            if label in C.ENTITY_STATS:
                text = font.render(str(C.ENTITY_STATS[label]["cost"]), True, C.TEXT_COLOR)
                screen.blit(text, (rect.x + C.MENU_WIDTH - 70, rect.y + 10))
    
    def draw(self, screen, font):
        self.right_side_menu(screen, font)

        self.unit_properties_menu(screen)
