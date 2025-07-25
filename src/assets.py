import pygame
import os

def load_assets(width, height):
    assets = {}
    # Paths
    START_BG_PATH = os.path.join('assets', 'images', 'start_bg.png')
    PLAYER_SPRITE_PATH = os.path.join('assets', 'images', 'Base pack', 'Player', 'p1_stand.png')
    PLAYER_CROUCH_PATH = os.path.join('assets', 'images', 'Base pack', 'Player', 'p1_duck.png')
    PLAYER_JUMP_PATH = os.path.join('assets', 'images', 'Base pack', 'Player', 'p1_jump.png')
    PLAYER_WALK_DIR = os.path.join('assets', 'images', 'Base pack', 'Player', 'p1_walk', 'PNG')
    # Load images
    if os.path.exists(START_BG_PATH):
        img = pygame.image.load(START_BG_PATH).convert()
        assets['start_bg'] = pygame.transform.scale(img, (width, height))
    else:
        assets['start_bg'] = None
    if os.path.exists(PLAYER_SPRITE_PATH):
        assets['player'] = pygame.image.load(PLAYER_SPRITE_PATH).convert_alpha()
    else:
        assets['player'] = None
    if os.path.exists(PLAYER_CROUCH_PATH):
        assets['player_crouch'] = pygame.image.load(PLAYER_CROUCH_PATH).convert_alpha()
    else:
        assets['player_crouch'] = None
    if os.path.exists(PLAYER_JUMP_PATH):
        assets['player_jump'] = pygame.image.load(PLAYER_JUMP_PATH).convert_alpha()
    else:
        assets['player_jump'] = None
    # Load walk animation frames
    walk_frames = []
    for i in range(1, 12):
        frame_name = f"p1_walk{str(i).zfill(2)}.png"
        frame_path = os.path.join(PLAYER_WALK_DIR, frame_name)
        if os.path.exists(frame_path):
            walk_frames.append(pygame.image.load(frame_path).convert_alpha())
    assets['player_walk'] = walk_frames if walk_frames else None
    return assets 