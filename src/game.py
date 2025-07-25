# Peluche Express main game loop and state management
# NOTE: Plan for future support of 2-3 local players (multiplayer)

import pygame
import sys
import os
from .player import Player
from .assets import load_assets

def run_game():
    pygame.init()
    WIDTH, HEIGHT = 1280, 720
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Peluche Express')
    clock = pygame.time.Clock()

    # Load assets
    assets = load_assets(WIDTH, HEIGHT)
    font = pygame.font.SysFont(None, 48)
    def get_text(text, color=(50, 50, 200), size=48):
        font = pygame.font.SysFont(None, size)
        return font.render(text, True, color)

    # Game states
    START_SCREEN = 0
    GAME_SCREEN = 1
    state = START_SCREEN
    help_overlay = False

    # PLAYER LOGIC: For future multiplayer, use a list of Player objects
    # For now, just one player, but structure allows easy extension
    player = Player(WIDTH, HEIGHT, assets)
    # Example for future: players = [Player(...), Player(...), ...]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if state == START_SCREEN and event.key == pygame.K_SPACE:
                    state = GAME_SCREEN
                    player.reset()
                elif state == GAME_SCREEN:
                    if event.key == pygame.K_UP and player.on_ground and not player.crouching:
                        player.jump()
                    elif event.key == pygame.K_DOWN and player.on_ground:
                        player.crouching = True
                    elif event.key == pygame.K_h:
                        help_overlay = not help_overlay
            elif event.type == pygame.KEYUP:
                if state == GAME_SCREEN:
                    if event.key == pygame.K_DOWN:
                        player.crouching = False

        keys = pygame.key.get_pressed()
        if state == GAME_SCREEN:
            player.handle_input(keys)
            player.update()
            # For future: loop over all players

        # Draw
        if state == START_SCREEN:
            if assets['start_bg']:
                screen.blit(assets['start_bg'], (0, 0))
            else:
                screen.fill((240, 240, 255))
                missing_text = get_text('Missing start_bg.png', (200, 50, 50))
                screen.blit(missing_text, missing_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        elif state == GAME_SCREEN:
            screen.fill((220, 255, 220))
            player.draw(screen)
            # For future: draw all players
            pygame.draw.rect(screen, (180, 220, 180), (0, HEIGHT - 50, WIDTH, 50))
            if help_overlay:
                overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                overlay.fill((255, 255, 255, 220))
                y = 120
                spacing = 60
                controls = [
                    ("← →", "Move left/right"),
                    ("↑", "Jump"),
                    ("↓", "Duck"),
                    ("Space", "Action (talk, open, etc.)"),
                    ("H", "Show/hide this help")
                ]
                title = get_text("Controls", (50, 50, 200), 64)
                overlay.blit(title, title.get_rect(center=(WIDTH // 2, 60)))
                for key, desc in controls:
                    key_img = get_text(key, (0, 0, 0), 48)
                    desc_img = get_text(desc, (60, 60, 60), 40)
                    overlay.blit(key_img, (WIDTH // 2 - 180, y))
                    overlay.blit(desc_img, (WIDTH // 2 - 100, y + 8))
                    y += spacing
                screen.blit(overlay, (0, 0))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit() 