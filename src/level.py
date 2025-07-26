import pygame
import json
import os

class Level:
    def __init__(self, config_path, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.camera_x = 0
        
        # Load JSON-based level
        self._load_json_level(config_path)
    
    def _load_json_level(self, config_path):
        """Load a JSON-based level."""
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

    def update_camera(self, player_x):
        # Center camera on player, but clamp to level bounds
        target_x = player_x - self.screen_width // 2
        self.camera_x = max(0, min(target_x, self.level_length_px - self.screen_width))

    def check_collision(self, player_rect):
        """Check collision between player and level tiles."""
        # Simple ground collision
        return player_rect.bottom >= self.ground_y
    
    def get_ground_y_at(self, x):
        """Get the ground Y position at a specific X coordinate."""
        return self.ground_y
    
    def get_start_position(self):
        """Get the player start position."""
        return (100, self.ground_y - 100)  # Default start position

    def draw(self, screen):
        # Always fill the screen with a sky color first
        screen.fill((120, 200, 255))  # sky blue
        
        # Draw JSON level
        self._draw_json_level(screen)
    
    def _draw_json_level(self, screen):
        """Draw a JSON-based level."""
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