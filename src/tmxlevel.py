import os
import xml.etree.ElementTree as ET
import pygame

class TmxLevel:
    def __init__(self, tmx_path, screen_width=1260, screen_height=840):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.tmx_path = tmx_path
        self.tile_width = 70
        self.tile_height = 70
        self.map_width = 0
        self.map_height = 0
        self.ground_layer = []
        self.background_layer = []
        self.object_layers = {}  # Store object layers
        self.tile_images = {}
        self.background = None
        self._load_tmx()

    def _load_tmx(self):
        tree = ET.parse(self.tmx_path)
        root = tree.getroot()
        self.tile_width = int(root.attrib['tilewidth'])
        self.tile_height = int(root.attrib['tileheight'])
        self.map_width = int(root.attrib['width'])
        self.map_height = int(root.attrib['height'])
        # Load default background
        bg_path = os.path.join('assets', 'images', 'Mushroom expansion', 'Backgrounds', 'bg_grasslands.png')
        if os.path.exists(bg_path):
            self.background = pygame.image.load(bg_path).convert()
        # Load tileset
        tileset = None
        for ts in root.findall('tileset'):
            tsx_path = os.path.join(os.path.dirname(self.tmx_path), ts.attrib['source'])
            tileset = ET.parse(tsx_path).getroot()
            break
        if tileset:
            for tile in tileset.findall('tile'):
                tid = int(tile.attrib['id'])
                img = tile.find('image')
                img_path = os.path.normpath(os.path.join(os.path.dirname(tsx_path), img.attrib['source']))
                if os.path.exists(img_path):
                    self.tile_images[tid+1] = pygame.image.load(img_path).convert_alpha()
        # Load layers
        for layer in root.findall('layer'):
            name = layer.attrib['name']
            data = layer.find('data').text.strip().replace('\n', '')
            values = [int(x) for x in data.split(',') if x.strip()]
            if name == 'ground':
                self.ground_layer = values
            elif name == 'background':
                self.background_layer = values
        
        # Load object layers
        for objgroup in root.findall('objectgroup'):
            name = objgroup.attrib['name']
            objects = []
            for obj in objgroup.findall('object'):
                obj_data = {
                    'id': int(obj.attrib.get('id', 0)),
                    'name': obj.attrib.get('name', ''),
                    'x': float(obj.attrib.get('x', 0)),
                    'y': float(obj.attrib.get('y', 0)),
                    'width': float(obj.attrib.get('width', 0)),
                    'height': float(obj.attrib.get('height', 0)),
                    'gid': int(obj.attrib.get('gid', 0))  # Global tile ID for tile objects
                }
                objects.append(obj_data)
            self.object_layers[name] = objects
            print(f"[TMX] Loaded object layer '{name}' with {len(objects)} objects")
            for obj in objects:
                print(f"[TMX]   - Object: {obj['name']} (ID: {obj['id']}) at ({obj['x']}, {obj['y']}) GID: {obj['gid']}")

    def get_layer(self, name):
        if name == 'ground':
            return self.ground_layer
        elif name == 'background':
            return self.background_layer
        return []

    def get_object_layer(self, name):
        """Get objects from a specific object layer."""
        return self.object_layers.get(name, [])

    def get_all_object_layers(self):
        """Get all object layers."""
        return self.object_layers

    def get_tile_image(self, tid):
        return self.tile_images.get(tid)

    def get_default_background(self):
        return self.background

    def check_collision(self, rect):
        """Check if rect collides with any solid ground tile."""
        # Check if the rect is within the level bounds
        if rect.right < 0 or rect.left > self.map_width * self.tile_width:
            return False
        if rect.bottom < 0 or rect.top > self.map_height * self.tile_height:
            return False
        
        # Calculate which tiles the rect overlaps
        start_x = max(0, rect.left // self.tile_width)
        end_x = min(self.map_width - 1, rect.right // self.tile_width)
        start_y = max(0, rect.top // self.tile_height)
        end_y = min(self.map_height - 1, rect.bottom // self.tile_height)
        
        # Check each tile in the overlap area
        for y in range(start_y, end_y + 1):
            for x in range(start_x, end_x + 1):
                idx = y * self.map_width + x
                if idx < len(self.ground_layer):
                    tid = self.ground_layer[idx]
                    if tid > 0:  # If there's a ground tile here
                        tile_rect = pygame.Rect(x * self.tile_width, y * self.tile_height, 
                                              self.tile_width, self.tile_height)
                        if rect.colliderect(tile_rect):
                            return True
        return False

    def draw_object_layer(self, screen, layer_name, camera_x=0, camera_y=0):
        """Draw a specific object layer."""
        if layer_name not in self.object_layers:
            return
        
        for obj in self.object_layers[layer_name]:
            if obj['gid'] > 0:  # This is a tile object
                tile_image = self.get_tile_image(obj['gid'])
                if tile_image:
                    # TMX uses bottom-left coordinates for tile objects, convert to top-left
                    render_x = obj['x'] - camera_x
                    render_y = obj['y'] - obj['height'] - camera_y  # Subtract height to get top-left
                    screen.blit(tile_image, (render_x, render_y))
            else:  # This is a regular object (rectangle, etc.)
                # Draw as a colored rectangle for now
                pygame.draw.rect(screen, (255, 255, 0), 
                               (obj['x'] - camera_x, obj['y'] - camera_y, obj['width'], obj['height']), 2)

    def draw_all_object_layers(self, screen, camera_x=0, camera_y=0):
        """Draw all object layers."""
        for layer_name in self.object_layers:
            self.draw_object_layer(screen, layer_name, camera_x, camera_y)
