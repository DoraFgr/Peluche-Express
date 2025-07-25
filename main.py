import pygame
import sys

pygame.init()

# Window settings
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Peluche Express')

# Font settings
font = pygame.font.SysFont(None, 48)
text = font.render('Hello, World', True, (50, 50, 200))
text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((240, 240, 255))  # Soft background color
    screen.blit(text, text_rect)
    pygame.display.flip()

pygame.quit()
sys.exit() 