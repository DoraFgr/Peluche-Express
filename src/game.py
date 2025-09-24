# -*- coding: utf-8 -*-
import arcade
from src.player import Player
from src.resource_utils import get_resource_path

class PelucheExpress(arcade.Window):
    def _start_gameplay(self):
        """Load and initialize the actual gameplay for the current level."""
        level = self.levels[self.current_level_id]
        
        # Load the map background and tilemap
        self.map_bg_texture = arcade.load_texture(get_resource_path(level["background"]))
        self.tile_map = arcade.load_tilemap(get_resource_path(level["map"]), scaling=1.0)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        
        # Clear existing players
        if "Players" in self.scene.name_mapping:
            self.scene.name_mapping["Players"].clear()
        if "Spawns" in self.scene.name_mapping:
            self.scene.name_mapping["Spawns"].clear()
            
        # Create players from spawn points (support two players)
        self.players = []
        p1_spawn = None
        p2_spawn = None
        if "Spawns" in self.tile_map.object_lists:
            for obj in self.tile_map.object_lists["Spawns"]:
                if obj.name == "Player1":
                    p1_spawn = obj
                elif obj.name == "Player2":
                    p2_spawn = obj
        # Always spawn Player1 at Player1 spawn, Player2 at Player2 spawn (if available)
        if p1_spawn:
            p1 = Player(
                get_resource_path("assets/images/Base pack/Player/p2_stand.png"),
                scale=1.0,
                start_x=p1_spawn.shape[0],
                start_y=p1_spawn.shape[1]
            )
            self.players.append(p1)
        if p2_spawn:
            p2 = Player(
                get_resource_path("assets/images/Base pack/Player/p1_stand.png"),
                scale=1.0,
                start_x=p2_spawn.shape[0],
                start_y=p2_spawn.shape[1]
            )
            self.players.append(p2)
                    
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
                    
        self.physics_engines = []
        if self.players and collidable_layers:
            for player in self.players:
                engine = arcade.PhysicsEnginePlatformer(
                    player,
                    collidable_layers,
                    gravity_constant=1.0
                )
                self.physics_engines.append(engine)

        # Calculate average x of EndZone objects for level completion
        end_zone_xs = []
        if "EndZone" in self.tile_map.object_lists:
            for obj in self.tile_map.object_lists["EndZone"]:
                end_zone_xs.append(obj.shape[0])
        if end_zone_xs:
            self.end_zone_avg_x = sum(end_zone_xs) / len(end_zone_xs)
        else:
            self.end_zone_avg_x = None

        # Set up apple collection system
        self.apples_collected = 0
        if "Apples" in self.scene.name_mapping:
            self.total_apples = len(self.scene.name_mapping["Apples"])
        else:
            self.total_apples = 0
            
        # Switch to game state
        self.state = "game"
        
    def _check_end_zone_transition(self):
        # Detect player crossing average End Zone x
        if self.end_zone_avg_x is not None and self.players:
            player = self.players[0]
            if player.center_x >= self.end_zone_avg_x:
                print("End Zone triggered! Starting exit animation...")
                self.state = "level_exit"
                self.exit_fade = 0.0
                self.exit_fade_speed = 0.03
                self.exit_player_walk = False
                self.exit_player_offscreen = False
                self.exit_timer = 0.0
                # Disable input for player
                player.input_disabled = True
                player.forced_walk = True
                # Optionally, store camera position to freeze
                self.exit_camera_pos = self.camera.position

    def _check_apple_collection(self):
        """Check if any player collects any apples (shared counter)."""
        if not self.players or "Apples" not in self.scene.name_mapping:
            return
        apple_list = self.scene.name_mapping["Apples"]
        for player in self.players:
            collected_apples = arcade.check_for_collision_with_list(player, apple_list)
            for apple in collected_apples:
                apple.remove_from_sprite_lists()
                self.apples_collected += 1
                print(f"Apple collected! {self.apples_collected}/{self.total_apples}")

    def _draw_apple_counter(self):
        """Draw the apple collection counter with mini apple icon in the top-left corner."""
        if self.state != "game":
            return
            
        # Draw counter with camera offset so it stays in place
        camera_x = self.camera.position[0]
        
        # Calculate positions - apple icon on the right side
        text_x = camera_x + 20
        text_y = self.height - 40
        icon_x = camera_x + 80
        icon_y = self.height - 30
        
        # Draw background for better visibility
        arcade.draw_rectangle_filled(
            camera_x + 65, self.height - 30,
            100, 40,
            (0, 0, 0, 128)
        )
        
        # Draw the counter text first
        arcade.draw_text(
            f"{self.apples_collected}/{self.total_apples}",
            text_x, text_y,
            arcade.color.WHITE,
            font_size=16,
            font_name="Arial"
        )
        
        # Draw mini apple icon on the right (scaled down)
        arcade.draw_texture_rectangle(
            icon_x, icon_y,
            24, 24,  # Mini size (24x24 instead of 70x70)
            self.apple_icon_texture
        )
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
        self.pressed_keys_p1 = set()
        self.pressed_keys_p2 = set()
        self.end_zone_sprites = None
        
        # Apple collection system
        self.apples_collected = 0
        self.total_apples = 0
        # Load mini apple icon for counter display
        self.apple_icon_texture = arcade.load_texture(get_resource_path("assets/images/Candy expansion/Tiles/cherry.png"))

    def _load_levels_config(self):
        import json
        
        config_path = get_resource_path("config/levels.json")
        with open(config_path, "r", encoding="utf-8") as f:
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
            self.background_texture = arcade.load_texture(get_resource_path(level["background"]))
            self._reset_gameplay_state()
            
        elif level["type"] == "level":
            # Game level - show transition screen first, then load the actual level
            self.transition_text = level.get("Description", "")
            assert "Description" in level, "Level must have a Description for transition text"
            background_path = level.get("background")
            assert background_path, "Background texture must be specified"
            
            self.background_texture = arcade.load_texture(get_resource_path(background_path))
                    
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
        # Reset apple collection counters
        self.apples_collected = 0
        self.total_apples = 0

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
        """Camera always follows Player 1."""
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
        # Draw apple counter
        self._draw_apple_counter()

    def on_draw(self):
        self.clear()
        
        if self.state == "main_screen":
            self._draw_main_screen()
        elif self.state == "transition_screen":
            self._draw_transition_screen()
        elif self.state == "game":
            self._draw_game_screen()
        elif self.state == "level_exit":
            # Draw game as usual, but freeze camera
            if not self.exit_camera_pos:
                self.exit_camera_pos = self.camera.position
            self.camera.move_to(self.exit_camera_pos, 1.0)
            self._draw_game_screen()
            # Fade out overlay
            if hasattr(self, 'exit_fade') and self.exit_fade > 0.0:
                arcade.draw_lrtb_rectangle_filled(0, self.width, self.height, 0, (0,0,0,int(255*self.exit_fade)))

    def on_update(self, delta_time):
        # Handle transition screen logic
        if self.state == "transition_screen":
            self.transition_timer += delta_time
            
            if self.transition_timer < 3.0:
                return
            # After 3 seconds, start gameplay
            self._start_gameplay()
            return

        # Only run game logic if in game state or level_exit
        if self.state not in ("game", "level_exit"):
            return

        # Main game update logic
        if hasattr(self, 'physics_engines') and self.physics_engines:
            for engine in self.physics_engines:
                engine.update()
        for idx, player in enumerate(self.players):
            # Prevent player from moving out of the map on the left side
            if self.tile_map and player.center_x < 0:
                player.center_x = 0
            engine = self.physics_engines[idx] if idx < len(self.physics_engines) else None
            player.update(physics_engine=engine)

        if self.state == "game":
            self._check_end_zone_transition()
            self._check_apple_collection()
            self._update_camera()
        elif self.state == "level_exit":
            player = self.players[0]
            # Let player land if in air
            if abs(player.change_y) > 1:
                pass  # Wait until landed
            else:
                # Start forced walk if not already
                if not self.exit_player_walk:
                    player.forced_walk = True
                    player.input_disabled = True
                    self.exit_player_walk = True
                # Move player right
                # Camera stays frozen at exit_camera_pos
                # Check if player is off screen
                if player.center_x > self.camera.position[0] + self.camera.viewport_width:
                    self.exit_player_offscreen = True
            # Fade out after offscreen
            if self.exit_player_offscreen:
                self.exit_fade += self.exit_fade_speed
                if self.exit_fade >= 1.0:
                    self._go_to_next_level()
            # Don't update camera (freeze)

    def on_key_press(self, key, modifiers):
        if self.state == "main_screen" and key == arcade.key.SPACE:
            self._go_to_next_level()
        elif self.state == "game":
            # Arrow keys for Player1, AWSD for Player2
            if key in (arcade.key.LEFT, arcade.key.RIGHT, arcade.key.UP, arcade.key.DOWN, arcade.key.SPACE):
                self.pressed_keys_p1.add(key)
            if key in (arcade.key.A, arcade.key.D, arcade.key.W, arcade.key.S, arcade.key.E):
                self.pressed_keys_p2.add(key)
            self._update_player_movement()

    def on_key_release(self, key, modifiers):
        if self.state == "game":
            if key in (arcade.key.LEFT, arcade.key.RIGHT, arcade.key.UP, arcade.key.DOWN, arcade.key.SPACE):
                self.pressed_keys_p1.discard(key)
            if key in (arcade.key.A, arcade.key.D, arcade.key.W, arcade.key.S, arcade.key.E):
                self.pressed_keys_p2.discard(key)
            self._update_player_movement()

    def _update_player_movement(self):
        # Player 1: Arrow keys
        if len(self.players) > 0:
            p1 = self.players[0]
            engine1 = self.physics_engines[0] if len(self.physics_engines) > 0 else None
            # Horizontal movement
            if arcade.key.LEFT in self.pressed_keys_p1 and arcade.key.RIGHT in self.pressed_keys_p1:
                p1.change_x = 0
            elif arcade.key.LEFT in self.pressed_keys_p1:
                p1.handle_input(arcade.key.LEFT, True, physics_engine=engine1)
            elif arcade.key.RIGHT in self.pressed_keys_p1:
                p1.handle_input(arcade.key.RIGHT, True, physics_engine=engine1)
            else:
                p1.handle_input(arcade.key.LEFT, False, physics_engine=engine1)
                p1.handle_input(arcade.key.RIGHT, False, physics_engine=engine1)
            # Vertical movement
            p1.handle_input(arcade.key.UP, arcade.key.UP in self.pressed_keys_p1, physics_engine=engine1)
            p1.handle_input(arcade.key.DOWN, arcade.key.DOWN in self.pressed_keys_p1, physics_engine=engine1)
            # Action key
            p1.handle_input(arcade.key.SPACE, arcade.key.SPACE in self.pressed_keys_p1, physics_engine=engine1)

        # Player 2: AWSD
        if len(self.players) > 1:
            p2 = self.players[1]
            engine2 = self.physics_engines[1] if len(self.physics_engines) > 1 else None
            # Horizontal movement
            if arcade.key.A in self.pressed_keys_p2 and arcade.key.D in self.pressed_keys_p2:
                p2.change_x = 0
            elif arcade.key.A in self.pressed_keys_p2:
                p2.handle_input(arcade.key.LEFT, True, physics_engine=engine2)
            elif arcade.key.D in self.pressed_keys_p2:
                p2.handle_input(arcade.key.RIGHT, True, physics_engine=engine2)
            else:
                p2.handle_input(arcade.key.LEFT, False, physics_engine=engine2)
                p2.handle_input(arcade.key.RIGHT, False, physics_engine=engine2)
            # Vertical movement (map W to UP for jump)
            p2.handle_input(arcade.key.UP, arcade.key.W in self.pressed_keys_p2, physics_engine=engine2)
            p2.handle_input(arcade.key.DOWN, arcade.key.S in self.pressed_keys_p2, physics_engine=engine2)
            # Action key (E)
            p2.handle_input(arcade.key.SPACE, arcade.key.E in self.pressed_keys_p2, physics_engine=engine2)

    def _go_to_next_level(self):
        # Advance to next level/screen using config
        current = self.levels[self.current_level_id]
        next_id = current.get("next")
        if next_id:
            self.current_level_id = next_id
            self._load_current_level()