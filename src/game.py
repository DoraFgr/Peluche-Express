import arcade
from src.player import Player

class PelucheExpress(arcade.Window):
    def _start_gameplay(self):
        level = self.levels[self.current_level_id]
        self.map_bg_texture = arcade.load_texture(level["background"])
        self.tile_map = arcade.load_tilemap(level["map"], scaling=1.0)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        if "Players" in self.scene.name_mapping:
            self.scene.name_mapping["Players"].clear()
        if "Spawns" in self.scene.name_mapping:
            self.scene.name_mapping["Spawns"].clear()
        self.players = []
        if "Spawns" in self.tile_map.object_lists:
            for obj in self.tile_map.object_lists["Spawns"]:
                if obj.name == "Player1":
                    p1 = Player(
                        "assets/images/Base pack/Player/p1_stand.png",
                        scale=1.0,
                        start_x=obj.shape[0],
                        start_y=obj.shape[1]
                    )
                    self.players.append(p1)
        if "Players" not in self.scene.name_mapping:
            self.scene.add_sprite_list("Players")
        for player in self.players:
            self.scene.add_sprite("Players", player)
        collidable_layers = []
        for layer in self.tile_map.tiled_map.layers:
            if hasattr(layer, "properties") and layer.properties and layer.properties.get("collides", False):
                layer_name = layer.name
                if layer_name in self.scene.name_mapping:
                    collidable_layers.append(self.scene.name_mapping[layer_name])
        self.physics_engine = None
        if self.players and collidable_layers:
            self.physics_engine = arcade.PhysicsEnginePlatformer(
                self.players[0],
                collidable_layers,
                gravity_constant=1.0
            )

        # Calculate average x of EndZone objects
        end_zone_xs = []
        if "EndZone" in self.tile_map.object_lists:
            for obj in self.tile_map.object_lists["EndZone"]:
                # Use shape[0] for x coordinate
                end_zone_xs.append(obj.shape[0])
        if end_zone_xs:
            self.end_zone_avg_x = sum(end_zone_xs) / len(end_zone_xs)
        else:
            self.end_zone_avg_x = None
        self.state = "game"
        
    def _check_end_zone_transition(self):
        # Detect player crossing average End Zone x
        if self.end_zone_avg_x is not None and not self.transitioning and self.players:
            player = self.players[0]
            print(f"[EndZoneCheck] Player x={player.center_x:.2f} | EndZone avg x={self.end_zone_avg_x:.2f}")
            if player.center_x >= self.end_zone_avg_x:
                print("End Zone triggered! Going to next level...")
                self.transitioning = True
                self._go_to_next_level()
    """
    Main application class.
    """

    def __init__(self, screen_width, screen_height, screen_title):
        import json
        super().__init__(screen_width, screen_height, screen_title)
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)
        self.levels = self._load_levels_config()
        self.current_level_id = None
        self.background_texture = None
        self.map_bg_texture = None
        self.state = "main_screen"
        self.transition_text = None
        self.transition_timer = 0
        self.tile_map = None
        self.scene = None
        self.players = []
        self.camera = arcade.Camera(screen_width, screen_height)
        self.pressed_keys = set()
        self.end_zone_sprites = None
        self.transitioning = False

    def _load_levels_config(self):
        import json
        with open("config/levels.json", "r") as f:
            levels_list = json.load(f)
        # Convert to dict for fast lookup by id
        return {level["id"]: level for level in levels_list}

    def setup(self):
        """Set up the game. Call to restart."""
        self.current_level_id = "start"
        self._load_current_level()
    def _load_current_level(self):
        self.end_zone_sprites = arcade.SpriteList()
        self.end_zone_avg_x = None
        level = self.levels[self.current_level_id]
        bg_path = level["background"]
        if level["type"] == "screen":
            self.state = "main_screen"
            print(f"[DEBUG] Loading main_screen background: {bg_path}")
            self.background_texture = arcade.load_texture(bg_path)
            self.map_bg_texture = None
            self.tile_map = None
            self.scene = None
            self.players = []
        elif level["type"] == "level":
            # Show transition screen first
            self.state = "transition_screen"
            self.transition_text = level.get("Description", "")
            self.transition_timer = 0
            print(f"[DEBUG] Loading transition_screen background: {bg_path}")
            self.background_texture = arcade.load_texture(bg_path)
            self.map_bg_texture = None
            self.tile_map = None
            self.scene = None
            self.players = []

    def on_draw(self):
        self.clear()
        if self.state == "main_screen" and self.background_texture:
            scale_x = self.width / self.background_texture.width
            scale_y = self.height / self.background_texture.height
            arcade.draw_texture_rectangle(
                self.width // 2,
                self.height // 2,
                self.background_texture.width * scale_x,
                self.background_texture.height * scale_y,
                self.background_texture
            )
        elif self.state == "transition_screen" and self.background_texture:
            # Draw background and transition text
            scale_x = self.width / self.background_texture.width
            scale_y = self.height / self.background_texture.height
            arcade.draw_texture_rectangle(
                self.width // 2,
                self.height // 2,
                self.background_texture.width * scale_x,
                self.background_texture.height * scale_y,
                self.background_texture
            )
            if self.transition_text:
                arcade.draw_text(
                    self.transition_text,
                    self.width // 2,
                    self.height // 2,
                    arcade.color.WHITE,
                    font_size=36,
                    font_name="Comic Sans MS",
                    anchor_x="center",
                    anchor_y="center"
                )
        elif self.state == "game" and self.scene:
            self.camera.use()
            # Draw repeating static background for the map, starting from the top
            if self.map_bg_texture:
                if self.tile_map:
                    map_width = self.tile_map.width * self.tile_map.tile_width
                    map_height = self.tile_map.height * self.tile_map.tile_height
                else:
                    map_width = self.width
                    map_height = self.height
                bg_width = self.map_bg_texture.width
                bg_height = self.map_bg_texture.height
                x = 0
                y = map_height - bg_height  # Start from the top
                while x < map_width:
                    arcade.draw_lrwh_rectangle_textured(
                        x, y, bg_width, bg_height, self.map_bg_texture
                    )
                    x += bg_width
            self.scene.draw()
            # Draw End Zone sprites
            if self.end_zone_sprites:
                self.end_zone_sprites.draw()

    def on_update(self, delta_time):
        # Handle transition screen logic
        if self.state == "transition_screen":
            self.transition_timer += delta_time
            if self.transition_timer < 3.0:
                return
            # After 3 seconds, start gameplay
            self._start_gameplay()
            return

        # Only run game logic if in game state
        if self.state != "game":
            return

        # Main game update logic
        if hasattr(self, 'physics_engine') and self.physics_engine:
            self.physics_engine.update()
        for player in self.players:
            # Prevent player from moving out of the map on the left side
            if self.tile_map and player.center_x < 0:
                player.center_x = 0
            player.update(physics_engine=self.physics_engine)
        self._check_end_zone_transition()
        # Camera deadzone logic
        if self.players:
            player = self.players[0]
            left_deadzone = self.camera.viewport_width * 0.4
            right_deadzone = self.camera.viewport_width * 0.6
            cam_left = self.camera.position[0]
            target_x = self.camera.position[0]
            if player.center_x < cam_left + left_deadzone:
                target_x = player.center_x - left_deadzone
            elif player.center_x > cam_left + right_deadzone:
                target_x = player.center_x - right_deadzone
            if self.tile_map:
                map_width = self.tile_map.width * self.tile_map.tile_width
                target_x = max(0, min(target_x, map_width - self.camera.viewport_width))
            self.camera.move_to((target_x, self.camera.position[1]), 0.2)

    def on_key_press(self, key, modifiers):
        if self.state == "main_screen" and key == arcade.key.SPACE:
            self._go_to_next_level()
        elif self.state == "game":
            self.pressed_keys.add(key)
            self._update_player_movement()

    def on_key_release(self, key, modifiers):
        if self.state == "game":
            self.pressed_keys.discard(key)
            self._update_player_movement()

    def _update_player_movement(self):
        for player in self.players:
            # Horizontal movement
            if arcade.key.LEFT in self.pressed_keys and arcade.key.RIGHT in self.pressed_keys:
                player.change_x = 0
            elif arcade.key.LEFT in self.pressed_keys:
                player.handle_input(arcade.key.LEFT, True, physics_engine=self.physics_engine)
            elif arcade.key.RIGHT in self.pressed_keys:
                player.handle_input(arcade.key.RIGHT, True, physics_engine=self.physics_engine)
            else:
                player.handle_input(arcade.key.LEFT, False, physics_engine=self.physics_engine)
                player.handle_input(arcade.key.RIGHT, False, physics_engine=self.physics_engine)
            # Vertical movement
            player.handle_input(arcade.key.UP, arcade.key.UP in self.pressed_keys, physics_engine=self.physics_engine)
            player.handle_input(arcade.key.DOWN, arcade.key.DOWN in self.pressed_keys, physics_engine=self.physics_engine)
            # Action key
            player.handle_input(arcade.key.SPACE, arcade.key.SPACE in self.pressed_keys, physics_engine=self.physics_engine)

    def _go_to_next_level(self):
        # Advance to next level/screen using config
        current = self.levels[self.current_level_id]
        next_id = current.get("next")
        print(f"Transitioning from {self.current_level_id} to {next_id}")
        if next_id:
            self.current_level_id = next_id
            self._load_current_level()