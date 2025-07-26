import arcade
import os

class TmxLevel(arcade.Scene):
    def __init__(self, tmx_path):
        super().__init__()
        
        # Create the scene
        layer_options = {
            "background": {
                "use_spatial_hash": False  # Decorative layer, no collisions
            },
            "ground": {
                "use_spatial_hash": True  # Enable spatial hashing for collision detection
            }
        }
        
        # Load the tilemap with our layer options
        self.tile_map = arcade.load_tilemap(
            tmx_path,
            scaling=1.0,
            layer_options=layer_options
        )
        
        # Set the boundaries
        self.width = self.tile_map.width * self.tile_map.tile_width
        self.height = self.tile_map.height * self.tile_map.tile_height
        
        # Get the tile layers - using the actual names from the TMX file
        self.background_list = self.tile_map.sprite_lists["background"]
        self.wall_list = self.tile_map.sprite_lists["ground"]  # This is our collision layer
        
        # Add sprite lists to the scene
        self.add_sprite_list("background", sprite_list=self.background_list)
        self.add_sprite_list("ground", sprite_list=self.wall_list, use_spatial_hash=True)
        
        # Set up the physics engine boundaries
        # Physics engine should be created in the main game class, not here
    
    def get_start_position(self):
        """Get the player start position from the goals layer or use default."""
        # Look for a clock object in the goals layer as the starting point
        if hasattr(self.tile_map, "object_lists") and "goals" in self.tile_map.object_lists:
            for obj in self.tile_map.object_lists["goals"]:
                if obj.name == "clock":
                    return obj.location
        
        # If no specific start position is found, start at a safe position
        return 100, self.height - 200  # Default starting position above ground level
