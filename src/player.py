import arcade
from src.resource_utils import get_resource_path

class Player(arcade.Sprite):
    def __init__(self, image_path, scale=1.0, start_x=0, start_y=0):
        """Initialize the player sprite and animation frames."""
        super().__init__(image_path, scale)
        self.center_x = start_x
        self.center_y = start_y
        self.speed = 10
        self.jump_speed = 18
        self.is_crouching = False
        self.is_action = False
        self._crouch_pressed = False
        self._jump_pressed = False  # Track if jump key is being held
        self.input_disabled = False
        self.forced_walk = False

        # Detect if this is Player 1 by image_path
        if "p1_stand.png" in image_path:
            # Use seahorse sprites from shp2 folder
            shp2_path = "assets/images/advanced/Player/shp2/"
            self.stand_texture = arcade.load_texture(get_resource_path(f"{shp2_path}face.png"))
            self.stand_texture_flipped = arcade.load_texture(get_resource_path(f"{shp2_path}face.png"), flipped_horizontally=True)
            # Crouch uses stand texture (no crouch sprite available)
            self.crouch_texture = self.stand_texture
            self.crouch_texture_flipped = self.stand_texture_flipped
            # Alternate between glide and side images for walk and jump animations
            glide_img = arcade.load_texture(get_resource_path(f"{shp2_path}glide.png"))
            glide_img_flipped = arcade.load_texture(get_resource_path(f"{shp2_path}glide.png"), flipped_horizontally=True)
            side_img = arcade.load_texture(get_resource_path(f"{shp2_path}side.png"))
            side_img_flipped = arcade.load_texture(get_resource_path(f"{shp2_path}side.png"), flipped_horizontally=True)
            self.walk_textures = [glide_img, side_img]
            self.walk_textures_flipped = [glide_img_flipped, side_img_flipped]
            self.jump_textures = [glide_img, side_img]
            self.jump_textures_flipped = [glide_img_flipped, side_img_flipped]
            # Use first frame for jump state
            self.jump_texture = self.jump_textures[0]
            self.jump_texture_flipped = self.jump_textures_flipped[0]
        else:
            # Use seahorse sprites from shp1 folder
            shp1_path = "assets/images/advanced/Player/shp1/"
            self.stand_texture = arcade.load_texture(get_resource_path(f"{shp1_path}face.png"))
            self.stand_texture_flipped = arcade.load_texture(get_resource_path(f"{shp1_path}face.png"), flipped_horizontally=True)
            # Crouch uses stand texture (no crouch sprite available)
            self.crouch_texture = self.stand_texture
            self.crouch_texture_flipped = self.stand_texture_flipped
            # Alternate between glide and side images for walk and jump animations
            glide_img = arcade.load_texture(get_resource_path(f"{shp1_path}glide.png"))
            glide_img_flipped = arcade.load_texture(get_resource_path(f"{shp1_path}glide.png"), flipped_horizontally=True)
            side_img = arcade.load_texture(get_resource_path(f"{shp1_path}side.png"))
            side_img_flipped = arcade.load_texture(get_resource_path(f"{shp1_path}side.png"), flipped_horizontally=True)
            self.walk_textures = [glide_img, side_img]
            self.walk_textures_flipped = [glide_img_flipped, side_img_flipped]
            self.jump_textures = [glide_img, side_img]
            self.jump_textures_flipped = [glide_img_flipped, side_img_flipped]
            # Use first frame for jump state
            self.jump_texture = self.jump_textures[0]
            self.jump_texture_flipped = self.jump_textures_flipped[0]
        self.walk_frame = 0
        self.walk_frame_delay = 8  # Slower pulse for walk animation
        self.walk_frame_counter = 0
        self.current_texture = self.stand_texture

    def update(self, physics_engine=None):
        # Forced walk logic for exit animation
        if getattr(self, 'forced_walk', False):
            self.change_x = abs(self.speed)

        """Update player animation and state."""
        is_jumping_now = abs(self.change_y) > 1
        previous_crouch = getattr(self, '_was_crouching', False)
        # Use scaled heights so adjustments remain correct when sprite.scale != 1
        stand_height = self.stand_texture.height * getattr(self, 'scale', 1)
        crouch_height = self.crouch_texture.height * getattr(self, 'scale', 1)
        # Adjust center_y so top stays fixed when crouching/standing
        if self.is_crouching != previous_crouch:
            offset = (stand_height - crouch_height) / 2
            self.center_y += -offset if self.is_crouching else offset
        self._was_crouching = self.is_crouching

        # Only crouch when on ground, but allow crouch to trigger after landing
        if self._crouch_pressed:
            if physics_engine and physics_engine.can_jump():
                self.is_crouching = True
        else:
            self.is_crouching = False

        # Animation state
        if is_jumping_now:
            major_state = 'jump'
            self.current_texture = self.jump_texture_flipped if self.change_x < 0 else self.jump_texture
        elif self.is_crouching:
            major_state = 'crouch'
            self.current_texture = self.crouch_texture_flipped if self.change_x < 0 else self.crouch_texture
        else:
            major_state = 'stand'
            if self.change_x != 0:
                self.walk_frame_counter += 1
                if self.walk_frame_counter >= self.walk_frame_delay:
                    self.walk_frame_counter = 0
                    self.walk_frame = (self.walk_frame + 1) % len(self.walk_textures)
                self.current_texture = self.walk_textures_flipped[self.walk_frame] if self.change_x < 0 else self.walk_textures[self.walk_frame]
            else:
                # Always show stand sprite when idle
                self.walk_frame = 0
                self.walk_frame_counter = 0
                self.current_texture = self.stand_texture_flipped if self.change_x < 0 else self.stand_texture

        # Only update hit box and height if major state changed
        if not hasattr(self, '_last_major_state') or self._last_major_state != major_state:
            self.texture = self.current_texture
            # Use scaled texture height to keep physical size consistent
            self.height = self.texture.height * getattr(self, 'scale', 1)
            # Scale hit box points so collisions match the drawn size
            if hasattr(self.texture, 'hit_box_points') and self.texture.hit_box_points:
                scaled_hit_box = [(x * getattr(self, 'scale', 1), y * getattr(self, 'scale', 1)) for x, y in self.texture.hit_box_points]
                self.set_hit_box(scaled_hit_box)
            self._last_major_state = major_state
        else:
            self.texture = self.current_texture
            # Keep using scaled height even when texture unchanged
            self.height = self.texture.height * getattr(self, 'scale', 1)

    def handle_input(self, key, pressed, physics_engine=None):
        if getattr(self, 'input_disabled', False):
            return
        """Handle key input for player movement and actions."""
        if key == arcade.key.LEFT:
            if not self.is_crouching:
                self.change_x = -self.speed if pressed else 0
            else:
                self.change_x = 0
        elif key == arcade.key.RIGHT:
            if not self.is_crouching:
                self.change_x = self.speed if pressed else 0
            else:
                self.change_x = 0
        elif key == arcade.key.UP:
            if pressed:
                # Only jump if we weren't already holding the jump key and can jump
                if not self._jump_pressed and physics_engine and physics_engine.can_jump():
                    self.change_y = self.jump_speed
                self._jump_pressed = True
            else:
                self._jump_pressed = False
        elif key == arcade.key.DOWN:
            self._crouch_pressed = pressed
        elif key == arcade.key.SPACE:
            self.is_action = pressed
