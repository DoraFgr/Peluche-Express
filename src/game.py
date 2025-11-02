# -*- coding: utf-8 -*-
import arcade
from src.player import Player
from src.resource_utils import get_resource_path
from src.apple_manager import check_apple_collection
from src.camera_utils import update_camera
from src.ui_draw import draw_apple_counter, draw_transition_text, draw_repeating_background, draw_main_screen, draw_transition_screen, draw_game_screen
from src.level_manager import load_levels_config, reset_gameplay_state, load_current_level, go_to_next_level
from src.level_exit import check_end_zone_transition
from src.input_handler import update_player_movement
from src.state_manager import handle_level_exit_update

class PelucheExpress(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, screen_width, screen_height, screen_title):
        super().__init__(screen_width, screen_height, screen_title)
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)
        self.levels = load_levels_config()
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

    def setup(self):
        """Set up the game. Call to restart."""
        self.current_level_id = "start"
        load_current_level(self)

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
                scale=0.96,
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
        
    def on_draw(self):
        self.clear()
        
        if self.state == "main_screen":
            draw_main_screen(self)
        elif self.state == "transition_screen":
            draw_transition_screen(self)
        elif self.state == "game":
            draw_game_screen(self)
        elif self.state == "level_exit":
            # Draw game as usual, but freeze camera
            if not self.exit_camera_pos:
                self.exit_camera_pos = self.camera.position
            self.camera.move_to(self.exit_camera_pos, 1.0)
            draw_game_screen(self)
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
            check_end_zone_transition(self)
            check_apple_collection(self)
            update_camera(self)
        elif self.state == "level_exit":
            handle_level_exit_update(self, delta_time)

    def on_key_press(self, key, modifiers):
        if self.state == "main_screen" and key == arcade.key.SPACE:
            go_to_next_level(self)
        elif self.state == "game":
            # Arrow keys for Player1, AWSD for Player2
            if key in (arcade.key.LEFT, arcade.key.RIGHT, arcade.key.UP, arcade.key.DOWN, arcade.key.SPACE):
                self.pressed_keys_p1.add(key)
            if key in (arcade.key.A, arcade.key.D, arcade.key.W, arcade.key.S, arcade.key.E):
                self.pressed_keys_p2.add(key)
            update_player_movement(self)

    def on_key_release(self, key, modifiers):
        if self.state == "game":
            if key in (arcade.key.LEFT, arcade.key.RIGHT, arcade.key.UP, arcade.key.DOWN, arcade.key.SPACE):
                self.pressed_keys_p1.discard(key)
            if key in (arcade.key.A, arcade.key.D, arcade.key.W, arcade.key.S, arcade.key.E):
                self.pressed_keys_p2.discard(key)
            update_player_movement(self)