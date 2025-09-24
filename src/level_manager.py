# Level management for Peluche Express
import arcade
import json
from src.resource_utils import get_resource_path
from src.player import Player

def load_levels_config():
    config_path = get_resource_path("config/levels.json")
    with open(config_path, "r", encoding="utf-8") as f:
        levels_list = json.load(f)
    return {level["id"]: level for level in levels_list}

def reset_gameplay_state(game):
    game.map_bg_texture = None
    game.tile_map = None
    game.scene = None
    game.players = []
    game.physics_engines = []
    game.end_zone_sprites = None
    game.end_zone_avg_x = None
    game.apples_collected = 0
    game.total_apples = 0
    game.pressed_keys_p1.clear()
    game.pressed_keys_p2.clear()

def load_current_level(game):
    game.end_zone_sprites = arcade.SpriteList()
    game.end_zone_avg_x = None
    level = game.levels[game.current_level_id]
    if level["type"] == "screen":
        game.state = "main_screen"
        game.background_texture = arcade.load_texture(get_resource_path(level["background"]))
        game.camera.move_to((0, 0), 1.0)
        reset_gameplay_state(game)
    elif level["type"] == "level":
        game.transition_text = level.get("Description", "")
        assert "Description" in level, "Level must have a Description for transition text"
        background_path = level.get("background")
        assert background_path, "Background texture must be specified"
        game.background_texture = arcade.load_texture(get_resource_path(background_path))
        game.state = "transition_screen"
        game.transition_timer = 0
        game.camera.move_to((0, 0), 1.0)
        reset_gameplay_state(game)

def go_to_next_level(game):
    current = game.levels[game.current_level_id]
    next_id = current.get("next")
    if next_id:
        game.current_level_id = next_id
        load_current_level(game)
