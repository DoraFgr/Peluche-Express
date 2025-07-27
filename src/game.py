import arcade
from src.player import Player

class PelucheExpress(arcade.Window):
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
        self.tile_map = None
        self.scene = None
        self.players = []
        self.camera = arcade.Camera(screen_width, screen_height)
        self.pressed_keys = set()

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
        level = self.levels[self.current_level_id]
        self.state = "main_screen" if level["type"] == "screen" else "game"
        self.background_texture = arcade.load_texture(level["background"])
        self.map_bg_texture = None
        self.tile_map = None
        self.scene = None
        self.players = []
        if level["type"] == "level":
            self.map_bg_texture = arcade.load_texture(level["background"])
            self.tile_map = arcade.load_tilemap(level["map"], scaling=1.0)
            self.scene = arcade.Scene.from_tilemap(self.tile_map)
            # Remove any existing 'Players' layer to avoid rendering markers
            if "Players" in self.scene.name_mapping:
                self.scene.name_mapping["Players"].clear()
            # Find player spawn in object layer 'Spawns'
            if "Spawns" in self.scene.name_mapping:
                self.scene.name_mapping["Spawns"].clear()
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
            # Set up physics engine for collidable layers
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
        elif self.state == "game" and self.scene:
            self.camera.use()
            # Draw repeating static background for the map
            if self.map_bg_texture:
                if self.tile_map:
                    map_width = self.tile_map.width * self.tile_map.tile_width
                else:
                    map_width = self.width
                bg_width = self.map_bg_texture.width
                bg_height = self.map_bg_texture.height
                x = 0
                while x < map_width:
                    arcade.draw_lrwh_rectangle_textured(
                        x, 0, bg_width, bg_height, self.map_bg_texture
                    )
                    x += bg_width
            self.scene.draw()

    def on_update(self, delta_time):
        if self.state != "game":
            return
        if hasattr(self, 'physics_engine') and self.physics_engine:
            self.physics_engine.update()
        for player in self.players:
            # Prevent player from moving out of the map on the left side
            if self.tile_map and player.center_x < 0:
                player.center_x = 0
            player.update(physics_engine=self.physics_engine)
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
        if next_id:
            self.current_level_id = next_id
            self._load_current_level()