import pygame
import json
import os
from .tmx_parser import TMXParser

class Level:
    def __init__(self, config_path, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.camera_x = 0
        
        # Check if config_path is a TMX file
        if config_path.endswith('.tmx'):
            self._load_tmx_level(config_path)
        else:
            self._load_json_level(config_path)
    
    def _load_tmx_level(self, tmx_path):
        """Load a TMX-based level."""
        self.tmx_parser = TMXParser(tmx_path)
        self.level_length_px = self.tmx_parser.map_width_px
        self.tile_width = self.tmx_parser.tile_width
        self.tile_height = self.tmx_parser.tile_height
        self.ground_y = self.screen_height - 100  # Default ground level
        
        # Set background to sky blue
        self.background = None
        self.background_color = (120, 200, 255)  # sky blue
        
        # Load a default ground tile for areas without TMX tiles
        ground_path = os.path.join('assets', 'images', 'Mushroom expansion', 'PNG', 'shroomTanMid.png')
        if os.path.exists(ground_path):
            self.ground_tile = pygame.image.load(ground_path).convert_alpha()
        else:
            self.ground_tile = None
    
    def _load_json_level(self, config_path):
        """Load a JSON-based level (legacy support)."""
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.level_length_px = self.config['level_length_screens'] * self.screen_width
        self.ground_y = self.config['ground_y']
        self.tile_width = self.config['tile_width']
        self.tile_height = self.config['tile_height']
        
        # Load background
        bg_path = os.path.join('assets', 'images', self.config['background'])
        if os.path.exists(bg_path):
            self.background = pygame.image.load(bg_path).convert()
        else:
            self.background = None
            
        # Load ground tile
        ground_path = os.path.join('assets', 'images', self.config['ground_tile'])
        if os.path.exists(ground_path):
            self.ground_tile = pygame.image.load(ground_path).convert_alpha()
        else:
            self.ground_tile = None
        
        self.tmx_parser = None

    def update_camera(self, player_x):
        # Center camera on player, but clamp to level bounds
        target_x = player_x - self.screen_width // 2
        self.camera_x = max(0, min(target_x, self.level_length_px - self.screen_width))

    def check_collision(self, player_rect):
        """Check collision between player and level tiles."""
        if not self.tmx_parser:
            # Legacy JSON level - simple ground collision
            return player_rect.bottom >= self.ground_y
        
        # TMX level - check against solid tiles
        # Convert player rect to tile coordinates
        left_tile_x, top_tile_y = self.tmx_parser.world_to_tile(player_rect.left, player_rect.top)
        right_tile_x, bottom_tile_y = self.tmx_parser.world_to_tile(player_rect.right, player_rect.bottom)
        
        print(f"Checking collision: player_rect={player_rect}, tile_coords=({left_tile_x},{top_tile_y}) to ({right_tile_x},{bottom_tile_y})")
        
        # Check all tiles the player might be touching
        for tile_y in range(top_tile_y, bottom_tile_y + 1):
            for tile_x in range(left_tile_x, right_tile_x + 1):
                if self.tmx_parser.is_solid_tile(tile_x, tile_y):
                    tile_rect = pygame.Rect(
                        tile_x * self.tmx_parser.tile_width,
                        tile_y * self.tmx_parser.tile_height,
                        self.tmx_parser.tile_width,
                        self.tmx_parser.tile_height
                    )
                    print(f"Solid tile at ({tile_x}, {tile_y}): {tile_rect}")
                    if player_rect.colliderect(tile_rect):
                        print(f"Collision with tile at ({tile_x}, {tile_y})")
                        return True
        
        return False
    
    def get_ground_y_at(self, x):
        """Get the ground Y position at a specific X coordinate."""
        if not self.tmx_parser:
            return self.ground_y
        
        # Find the highest solid tile at this X position
        tile_x = int(x // self.tmx_parser.tile_width)
        for tile_y in range(self.tmx_parser.map_height):
            if self.tmx_parser.is_solid_tile(tile_x, tile_y):
                return tile_y * self.tmx_parser.tile_height
        
        return self.screen_height  # No ground found
    
    def get_start_position(self):
        """Get the player start position."""
        if self.tmx_parser:
            return self.tmx_parser.get_start_position()
        else:
            return (100, self.ground_y - 100)  # Default for JSON levels

    def draw(self, screen):
        # Always fill the screen with a sky color first
        if self.tmx_parser:
            screen.fill(self.background_color)
        else:
            screen.fill((120, 200, 255))  # sky blue
        
        if self.tmx_parser:
            # Draw TMX level
            self._draw_tmx_level(screen)
        else:
            # Draw JSON level (legacy)
            self._draw_json_level(screen)
    
    def _draw_tmx_level(self, screen):
        """Draw a TMX-based level."""
        # Draw background layer
        if self.tmx_parser.background_layer:
            bg_surface = self.tmx_parser.render_layer('background', self.camera_x, self.screen_width)
            screen.blit(bg_surface, (0, 0))
        
        # Draw ground layer
        if self.tmx_parser.ground_layer:
            ground_surface = self.tmx_parser.render_layer('ground', self.camera_x, self.screen_width)
            screen.blit(ground_surface, (0, 0))
        
        # Fill any remaining space below the map with a solid color
        map_bottom = self.tmx_parser.map_height_px
        if map_bottom < self.screen_height:
            pygame.draw.rect(screen, (139, 69, 19), 
                           (0, map_bottom, self.screen_width, self.screen_height - map_bottom))
    
    def _draw_json_level(self, screen):
        """Draw a JSON-based level (legacy)."""
        # Draw background (tiled horizontally, stretched vertically)
        if self.background:
            bg_width = self.background.get_width()
            bg_height = self.background.get_height()
            scaled_bg = pygame.transform.scale(self.background, (bg_width, self.screen_height))
            for i in range((self.screen_width // bg_width) + 2):
                x = i * bg_width - (self.camera_x % bg_width)
                screen.blit(scaled_bg, (x, 0))
        
        # Fill under the ground with a solid color (brown)
        pygame.draw.rect(screen, (139, 69, 19), 
                        (0, self.ground_y, self.screen_width, self.screen_height - self.ground_y))
        
        # Draw ground (tile horizontally and fill vertically to bottom)
        if self.ground_tile:
            num_tiles_x = (self.level_length_px // self.tile_width) + 2
            for i in range(num_tiles_x):
                x = i * self.tile_width - self.camera_x
                if 0 - self.tile_width < x < self.screen_width:
                    y = self.ground_y
                    while y < self.screen_height:
                        screen.blit(self.ground_tile, (x, y))
                        y += self.tile_height 