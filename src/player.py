import arcade

class Player(arcade.Sprite):
    def __init__(self, image_path, scale=1.0, start_x=0, start_y=0):
        super().__init__(image_path, scale)
        self.center_x = start_x
        self.center_y = start_y
        self.speed = 5
        self.jump_speed = 12
        self.is_crouching = False
        self.is_action = False
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
        self.walk_frame_delay = 3  # Number of updates per frame
        self.walk_frame_counter = 0
        self.jump_texture = arcade.load_texture("assets/images/Base pack/Player/p1_jump.png")
        self.jump_texture_flipped = arcade.load_texture("assets/images/Base pack/Player/p1_jump.png", flipped_horizontally=True)
        self.stand_texture = arcade.load_texture(image_path)
        self.stand_texture_flipped = arcade.load_texture(image_path, flipped_horizontally=True)
        self.crouch_texture = arcade.load_texture("assets/images/Base pack/Player/p1_duck.png")
        self.crouch_texture_flipped = arcade.load_texture("assets/images/Base pack/Player/p1_duck.png", flipped_horizontally=True)
        self.current_texture = self.stand_texture

    def update(self):
        # Animation logic
        is_jumping_now = abs(self.change_y) > 1
        if is_jumping_now:
            self.current_texture = self.jump_texture_flipped if self.change_x < 0 else self.jump_texture
        elif self.is_crouching:
            self.current_texture = self.crouch_texture_flipped if self.change_x < 0 else self.crouch_texture
        elif self.change_x != 0:
            self.walk_frame_counter += 1
            if self.walk_frame_counter >= self.walk_frame_delay:
                self.walk_frame_counter = 0
                self.walk_frame = (self.walk_frame + 1) % len(self.walk_textures)
            self.current_texture = self.walk_textures_flipped[self.walk_frame] if self.change_x < 0 else self.walk_textures[self.walk_frame]
        else:
            self.walk_frame = 0
            self.walk_frame_counter = 0
            self.current_texture = self.stand_texture_flipped if self.change_x < 0 else self.stand_texture
        self.texture = self.current_texture

    def handle_input(self, key, pressed, physics_engine=None):
        # Handle key input for this player
        if key == arcade.key.LEFT:
            self.change_x = -self.speed if pressed else 0
        elif key == arcade.key.RIGHT:
            self.change_x = self.speed if pressed else 0
        elif key == arcade.key.UP:
            if pressed and physics_engine and physics_engine.can_jump():
                self.change_y = self.jump_speed
        elif key == arcade.key.DOWN:
            self.is_crouching = pressed
        elif key == arcade.key.SPACE:
            self.is_action = pressed
