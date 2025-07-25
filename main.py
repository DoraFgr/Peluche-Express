import pygame
import sys
import os

pygame.init()

# Window settings
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Peluche Express')

# Asset paths
START_BG_PATH = os.path.join('assets', 'images', 'start_bg.png')

# Load start screen background
if os.path.exists(START_BG_PATH):
    start_bg = pygame.image.load(START_BG_PATH).convert()
    start_bg = pygame.transform.scale(start_bg, (WIDTH, HEIGHT))
else:
    start_bg = None

# Font settings for placeholder
font = pygame.font.SysFont(None, 48)
game_started_text = font.render('Game Started!', True, (50, 50, 200))
game_started_rect = game_started_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

# Game states
START_SCREEN = 0
GAME_SCREEN = 1
state = START_SCREEN

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if state == START_SCREEN and event.key == pygame.K_SPACE:
                state = GAME_SCREEN

    if state == START_SCREEN:
        if start_bg:
            screen.blit(start_bg, (0, 0))
        else:
            screen.fill((240, 240, 255))
            # Optionally display a message if image is missing
            missing_text = font.render('Missing start_bg.png', True, (200, 50, 50))
            screen.blit(missing_text, missing_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
    elif state == GAME_SCREEN:
        screen.fill((220, 255, 220))  # Placeholder game screen color
        screen.blit(game_started_text, game_started_rect)

    pygame.display.flip()

pygame.quit()
sys.exit() 