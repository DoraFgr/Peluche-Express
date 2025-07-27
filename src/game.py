# -*- coding: utf-8 -*-
import arcade
from src.player import Player

class PelucheExpress(arcade.Window):
    def _start_gameplay(self):
        """Load and initialize the actual gameplay for the current level."""
        level = self.levels[self.current_level_id]
        
        # Load the map background and tilemap
        self.map_bg_texture = arcade.load_texture(level["background"])
        self.tile_map = arcade.load_tilemap(level["map"], scaling=1.0)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        
        # Clear existing players
        if "Players" in self.scene.name_mapping:
            self.scene.name_mapping["Players"].clear()
        if "Spawns" in self.scene.name_mapping:
            self.scene.name_mapping["Spawns"].clear()
            
        # Create players from spawn points
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
                    
        # Add players to scene
        if "Players" not in self.scene.name_mapping:
            self.scene.add_sprite_list("Players")
        for player in self.players:
            self.scene.add_sprite("Players", player)
            
        # Set up physics
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

        # Calculate average x of EndZone objects for level completion
        end_zone_xs = []
        if "EndZone" in self.tile_map.object_lists:
            for obj in self.tile_map.object_lists["EndZone"]:
                end_zone_xs.append(obj.shape[0])
        if end_zone_xs:
            self.end_zone_avg_x = sum(end_zone_xs) / len(end_zone_xs)
        else:
            self.end_zone_avg_x = None
            
        # Switch to game state
        self.state = "game"
        
    def _check_end_zone_transition(self):
        # Detect player crossing average End Zone x
        if self.end_zone_avg_x is not None and self.players:
            player = self.players[0]
            if player.center_x >= self.end_zone_avg_x:
                print("End Zone triggered! Going to next level...")
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

    def _load_levels_config(self):
        import json
        with open("config/levels.json", "r", encoding="utf-8") as f:
            levels_list = json.load(f)
        # Convert to dict for fast lookup by id
        return {level["id"]: level for level in levels_list}

    def setup(self):
        """Set up the game. Call to restart."""
        self.current_level_id = "start"
        self._load_current_level()
        
    def _load_current_level(self):
        """Set up the current level based on its type."""
        self.end_zone_sprites = arcade.SpriteList()
        self.end_zone_avg_x = None
        
        level = self.levels[self.current_level_id]
        
        if level["type"] == "screen":
            # Main menu screen
            self.state = "main_screen"
            self.background_texture = arcade.load_texture(level["background"])
            self._reset_gameplay_state()
            
        elif level["type"] == "level":
            # Game level - show transition screen first, then load the actual level
            self.transition_text = level.get("Description", "")
            assert "Description" in level, "Level must have a Description for transition text"
            background_path = level.get("background")
            assert background_path, "Background texture must be specified"
            
            self.background_texture = arcade.load_texture(background_path)
                    
            self.state = "transition_screen"
            self.transition_timer = 0  # Reset timer
            
            # Reset camera position for transition screen
            self.camera.move_to((0, 0), 1.0)
            
            self._reset_gameplay_state()
    
    def _reset_gameplay_state(self):
        """Reset all gameplay-related state."""
        self.map_bg_texture = None
        self.tile_map = None
        self.scene = None
        self.players = []
        self.physics_engine = None

    def _draw_repeating_background(self, texture, width, height):
        """Draw a background texture stretched to full height and repeated horizontally."""
        if not texture:
            return
            
        # Stretch to full height and repeat horizontally
        scale_y = height / texture.height
        scaled_width = texture.width * scale_y
        scaled_height = height
        
        # Draw repeating background to cover full width
        x = 0
        while x < width:
            arcade.draw_lrwh_rectangle_textured(
                x, 0, scaled_width, scaled_height, texture
            )
            x += scaled_width

    def _draw_transition_text(self):
        """Draw the transition text with semi-transparent background."""
        if not self.transition_text:
            return
            
        # Draw with a semi-transparent background for better visibility
        arcade.draw_rectangle_filled(
            self.width // 2,
            self.height // 2,
            len(self.transition_text) * 25,
            60,
            (0, 0, 0, 128)
        )
        # Use explicit font name for better Unicode support
        arcade.draw_text(
            self.transition_text,
            self.width // 2,
            self.height // 2,
            arcade.color.WHITE,
            font_size=36,
            anchor_x="center",
            anchor_y="center",
            font_name="Arial"
        )

    def _update_camera(self):
        """Update camera position based on player position with deadzone logic."""
        if not self.players:
            return
            
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

    def _draw_main_screen(self):
        """Draw the main menu screen."""
        if self.background_texture:
            self._draw_repeating_background(self.background_texture, self.width, self.height)

    def _draw_transition_screen(self):
        """Draw the transition screen with background and text."""
        # Create a fresh UI camera for transition screen rendering
        ui_camera = arcade.Camera(self.width, self.height)
        ui_camera.move_to((0, 0), 1.0)
        ui_camera.use()
        
        # Draw the transition background
        self._draw_repeating_background(self.background_texture, self.width, self.height)
        
        # Draw the transition text
        self._draw_transition_text()

    def _draw_game_screen(self):
        """Draw the game screen with background, scene, and sprites."""
        if not self.scene:
            return
            
        self.camera.use()
        # Draw repeating static background for the map, stretched to full height
        if self.map_bg_texture:
            if self.tile_map:
                map_width = self.tile_map.width * self.tile_map.tile_width
                map_height = self.tile_map.height * self.tile_map.tile_height
            else:
                map_width = self.width
                map_height = self.height
            
            self._draw_repeating_background(self.map_bg_texture, map_width, map_height)
        self.scene.draw()
        # Draw End Zone sprites
        if self.end_zone_sprites:
            self.end_zone_sprites.draw()

    def on_draw(self):
        self.clear()
        
        if self.state == "main_screen":
            self._draw_main_screen()
        elif self.state == "transition_screen":
            self._draw_transition_screen()
        elif self.state == "game":
            self._draw_game_screen()

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
        self._update_camera()

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