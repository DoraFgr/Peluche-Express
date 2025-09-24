# UI drawing helpers for Peluche Express
import arcade

def draw_apple_counter(game):
    """Draw the apple collection counter with mini apple icon in the top-left corner."""
    if game.state != "game":
        return
    camera_x = game.camera.position[0]
    text_x = camera_x + 20
    text_y = game.height - 40
    icon_x = camera_x + 80
    icon_y = game.height - 30
    arcade.draw_rectangle_filled(
        camera_x + 65, game.height - 30,
        100, 40,
        (0, 0, 0, 128)
    )
    arcade.draw_text(
        f"{game.apples_collected}/{game.total_apples}",
        text_x, text_y,
        arcade.color.WHITE,
        font_size=16,
        font_name="Arial"
    )
    arcade.draw_texture_rectangle(
        icon_x, icon_y,
        24, 24,
        game.apple_icon_texture
    )

def draw_transition_text(game):
    if not game.transition_text:
        return
    arcade.draw_rectangle_filled(
        game.width // 2,
        game.height // 2,
        len(game.transition_text) * 25,
        60,
        (0, 0, 0, 128)
    )
    arcade.draw_text(
        game.transition_text,
        game.width // 2,
        game.height // 2,
        arcade.color.WHITE,
        font_size=36,
        anchor_x="center",
        anchor_y="center",
        font_name="Arial"
    )

def draw_repeating_background(texture, width, height):
    if not texture:
        return
    scale_y = height / texture.height
    scaled_width = texture.width * scale_y
    scaled_height = height
    x = 0
    while x < width:
        arcade.draw_lrwh_rectangle_textured(
            x, 0, scaled_width, scaled_height, texture
        )
        x += scaled_width

def draw_main_screen(game):
    game.camera.use()
    if game.background_texture:
        draw_repeating_background(game.background_texture, game.width, game.height)

def draw_transition_screen(game):
    ui_camera = arcade.Camera(game.width, game.height)
    ui_camera.move_to((0, 0), 1.0)
    ui_camera.use()
    draw_repeating_background(game.background_texture, game.width, game.height)
    draw_transition_text(game)

def draw_game_screen(game):
    if not game.scene:
        return
    game.camera.use()
    if game.map_bg_texture:
        if game.tile_map:
            map_width = game.tile_map.width * game.tile_map.tile_width
            map_height = game.tile_map.height * game.tile_map.tile_height
        else:
            map_width = game.width
            map_height = game.height
        draw_repeating_background(game.map_bg_texture, map_width, map_height)
    game.scene.draw()
    if game.end_zone_sprites:
        game.end_zone_sprites.draw()
    draw_apple_counter(game)
