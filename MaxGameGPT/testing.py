import pygame

pygame.init()
screen = pygame.display.set_mode((500, 400))
pygame.display.set_caption("pygame.draw.rect Example")

# Colors
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Draw a filled red rectangle
pygame.draw.rect(screen, red, pygame.Rect(50, 50, 100, 80))

# Draw a green rectangle with a 5px border
pygame.draw.rect(screen, green, pygame.Rect(200, 50, 100, 80), 5)

# Draw a blue rectangle with rounded corners
pygame.draw.rect(screen, blue, (350, 50, 100, 80), border_radius=15)

pygame.display.flip()
pygame.time.wait(3000)
pygame.quit()