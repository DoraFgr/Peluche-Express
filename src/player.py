import arcade

class Player(arcade.Sprite):
    def __init__(self, image_path, scale=1.0, start_x=0, start_y=0):
        """Initialize the player sprite and animation frames."""
        super().__init__(image_path, scale)
        self.center_x = start_x
        self.center_y = start_y
        self.speed = 12
        self.jump_speed = 17
        self.is_crouching = False
        self.is_action = False
        self._crouch_pressed = False
        # Animation frames
        self.walk_textures = [
            arcade.load_texture(f"assets/images/Base pack/Player/p1_walk/PNG/p1_walk{str(i).zfill(2)}.png")
            for i in range(1, 12)
        ]
        self.walk_textures_flipped = [
            arcade.load_texture(f"assets/images/Base pack/Player/p1_walk/PNG/p1_walk{str(i).zfill(2)}.png", flipped_horizontally=True)
            for i in range(1, 12)
        ]
        self.walk_frame = 0
        self.walk_frame_delay = 3
        self.walk_frame_counter = 0
        self.jump_texture = arcade.load_texture("assets/images/Base pack/Player/p1_jump.png")
        self.jump_texture_flipped = arcade.load_texture("assets/images/Base pack/Player/p1_jump.png", flipped_horizontally=True)
        self.stand_texture = arcade.load_texture(image_path)
        self.stand_texture_flipped = arcade.load_texture(image_path, flipped_horizontally=True)
        self.crouch_texture = arcade.load_texture("assets/images/Base pack/Player/p1_duck.png")
        self.crouch_texture_flipped = arcade.load_texture("assets/images/Base pack/Player/p1_duck.png", flipped_horizontally=True)
        self.current_texture = self.stand_texture

    def update(self, physics_engine=None):
        """Update player animation and state."""
        is_jumping_now = abs(self.change_y) > 1
        previous_crouch = getattr(self, '_was_crouching', False)
        stand_height = self.stand_texture.height
        crouch_height = self.crouch_texture.height
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
                self.walk_frame = 0
                self.walk_frame_counter = 0
                self.current_texture = self.stand_texture_flipped if self.change_x < 0 else self.stand_texture

        # Only update hit box and height if major state changed
        if not hasattr(self, '_last_major_state') or self._last_major_state != major_state:
            self.texture = self.current_texture
            self.height = self.texture.height
            self.set_hit_box(self.texture.hit_box_points)
            self._last_major_state = major_state
        else:
            self.texture = self.current_texture
            self.height = self.texture.height

    def handle_input(self, key, pressed, physics_engine=None):
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
            if pressed and physics_engine and physics_engine.can_jump():
                self.change_y = self.jump_speed
        elif key == arcade.key.DOWN:
            self._crouch_pressed = pressed
        elif key == arcade.key.SPACE:
            self.is_action = pressed
