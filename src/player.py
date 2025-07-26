import arcade
from typing import Optional, List

class Player:
    def __init__(self, x: float, y: float, assets: dict):
        # Create the sprite
        self.sprite = arcade.Sprite()
        
        # Set initial position
        self.sprite.center_x = x
        self.sprite.center_y = y
        
        # Constants
        self.SPEED = 7
        self.JUMP_SPEED = 18
        self.PLAYER_SCALING = 1.0
        
        # State
        self.facing_right = True
        self.crouching = False
        
        # Assets and animation
        self.stand_right_texture: Optional[arcade.Texture] = None
        self.stand_left_texture: Optional[arcade.Texture] = None
        self.jump_right_texture: Optional[arcade.Texture] = None
        self.jump_left_texture: Optional[arcade.Texture] = None
        self.crouch_right_texture: Optional[arcade.Texture] = None
        self.crouch_left_texture: Optional[arcade.Texture] = None
        self.walk_right_textures: List[arcade.Texture] = []
        self.walk_left_textures: List[arcade.Texture] = []
        
        # Load textures
        self._load_textures(assets)
        
        # Animation state
        self.walk_frame_idx = 0
        self.walk_anim_timer = 0
        self.walk_anim_speed = 6  # frames per animation update
        
        # Set initial texture
        if self.stand_right_texture:
            self.sprite.texture = self.stand_right_texture
            self.sprite.set_hit_box(self.sprite.texture.hit_box_points)

    def _load_textures(self, assets: dict):
        """Load all textures and create left/right pairs."""
        # Standing
        if 'player' in assets and 'player_path' in assets and assets['player_path']:
            self.stand_right_texture = assets['player']
            self.stand_left_texture = arcade.load_texture(
                assets['player_path'], flipped_horizontally=True)

        # Jumping
        if 'player_jump' in assets and 'player_jump_path' in assets and assets['player_jump_path']:
            self.jump_right_texture = assets['player_jump']
            self.jump_left_texture = arcade.load_texture(
                assets['player_jump_path'], flipped_horizontally=True)

        # Crouching
        if 'player_crouch' in assets and 'player_crouch_path' in assets and assets['player_crouch_path']:
            self.crouch_right_texture = assets['player_crouch']
            self.crouch_left_texture = arcade.load_texture(
                assets['player_crouch_path'], flipped_horizontally=True)

        # Walking animations
        if 'player_walk' in assets:
            for tex in assets['player_walk']:
                right_tex, left_tex = arcade.load_texture_pair(tex)
                self.walk_right_textures.append(right_tex)
                self.walk_left_textures.append(left_tex)

    def update(self, delta_time: float = 1/60):
        """Update the sprite's animation."""
        # Figure out if we need to flip face left or right
        if self.sprite.change_x < 0 and self.facing_right:
            self.facing_right = False
        elif self.sprite.change_x > 0 and not self.facing_right:
            self.facing_right = True

        # Get the appropriate texture lists for current direction
        walk_textures = self.walk_right_textures if self.facing_right else self.walk_left_textures
        stand_texture = self.stand_right_texture if self.facing_right else self.stand_left_texture
        jump_texture = self.jump_right_texture if self.facing_right else self.jump_left_texture
        crouch_texture = self.crouch_right_texture if self.facing_right else self.crouch_left_texture

        # Choose the appropriate texture based on state
        if self.sprite.change_y > 0 and jump_texture:
            # Jumping
            self.sprite.texture = jump_texture
        elif self.crouching and crouch_texture:
            # Crouching
            self.sprite.texture = crouch_texture
            # Adjust hit box for crouching if needed
            if self.sprite.texture != self.sprite.cur_texture_name:
                self.sprite.set_hit_box(crouch_texture.hit_box_points)
        elif self.sprite.change_x != 0 and walk_textures:
            # Walking
            self.walk_anim_timer += 1
            if self.walk_anim_timer >= self.walk_anim_speed:
                self.walk_anim_timer = 0
                self.walk_frame_idx = (self.walk_frame_idx + 1) % len(walk_textures)
                self.sprite.texture = walk_textures[self.walk_frame_idx]
        elif stand_texture:
            # Standing still
            if self.sprite.texture != stand_texture:
                self.sprite.texture = stand_texture
                self.sprite.set_hit_box(stand_texture.hit_box_points)

    def draw(self):
        """Draw the player sprite."""
        self.sprite.draw()

    def jump(self):
        """Make the player jump."""
        self.sprite.change_y = self.JUMP_SPEED

    def crouch(self):
        """Make the player crouch."""
        self.crouching = True

    def stand(self):
        """Make the player stand up from crouching."""
        self.crouching = False

    def move_left(self):
        """Move the player left."""
        self.sprite.change_x = -self.SPEED

    def move_right(self):
        """Move the player right."""
        self.sprite.change_x = self.SPEED

    def stop(self):
        """Stop the player's horizontal movement."""
        self.sprite.change_x = 0

    def reset(self, x: float, y: float):
        """Reset the player to starting position."""
        self.sprite.center_x = x
        self.sprite.center_y = y
        self.sprite.change_x = 0
        self.sprite.change_y = 0
        self.crouching = False
        self.walk_frame_idx = 0
        self.walk_anim_timer = 0
        self.facing_right = True
        if self.stand_right_texture:
            self.sprite.texture = self.stand_right_texture