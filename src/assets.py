import arcade
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
        assets['start_bg'] = arcade.load_texture(START_BG_PATH)
    else:
        assets['start_bg'] = None


    # Load player textures and store file paths
    if os.path.exists(PLAYER_SPRITE_PATH):
        assets['player'] = arcade.load_texture(PLAYER_SPRITE_PATH)
        assets['player_path'] = PLAYER_SPRITE_PATH
    else:
        assets['player'] = None
        assets['player_path'] = None

    if os.path.exists(PLAYER_CROUCH_PATH):
        assets['player_crouch'] = arcade.load_texture(PLAYER_CROUCH_PATH)
        assets['player_crouch_path'] = PLAYER_CROUCH_PATH
    else:
        assets['player_crouch'] = None
        assets['player_crouch_path'] = None

    if os.path.exists(PLAYER_JUMP_PATH):
        assets['player_jump'] = arcade.load_texture(PLAYER_JUMP_PATH)
        assets['player_jump_path'] = PLAYER_JUMP_PATH
    else:
        assets['player_jump'] = None
        assets['player_jump_path'] = None

    # Load walk animation frames
    walk_frames = []
    for i in range(1, 12):
        frame_name = f"p1_walk{str(i).zfill(2)}.png"
        frame_path = os.path.join(PLAYER_WALK_DIR, frame_name)
        if os.path.exists(frame_path):
            walk_frames.append(arcade.load_texture(frame_path))
    assets['player_walk'] = walk_frames if walk_frames else None

    return assets 