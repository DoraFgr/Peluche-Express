# Peluche Express main game loop and state management
# NOTE: Plan for future support of 2-3 local players (multiplayer)

import os
import arcade
import arcade.key
from .player import Player
from .assets import load_assets
from .tmxlevel import TmxLevel

class PelucheGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.START_SCREEN = 0
        self.GAME_SCREEN = 1
        self.state = self.START_SCREEN
        self.help_overlay = False
        self.player = None
        self.level = None
        self.physics_engine = None
        self.assets = None
        self.camera = None
        self.gui_camera = None

    def setup(self):
        self.camera = arcade.Camera2D()
        self.gui_camera = arcade.Camera2D()
        self.assets = load_assets(self.width, self.height)
        tmx_path = os.path.join('tilemaps', 'map1.tmx')
        self.level = TmxLevel(tmx_path)
        start_x, start_y = self.level.get_start_position()
        self.player = Player(start_x, start_y, self.assets)
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player.sprite,
            self.level.wall_list,
            gravity_constant=1.0
        )

    def on_draw(self):
        self.clear()
        if self.state == self.START_SCREEN:
            self.gui_camera.use()
            if 'start_bg' in self.assets:
                arcade.draw_lrwh_rectangle_textured(
                    0, 0, self.width, self.height, self.assets['start_bg']
                )
            else:
                arcade.draw_text(
                    "Press SPACE to start",
                    self.width / 2,
                    self.height / 2,
                    arcade.color.WHITE,
                    44,
                    anchor_x="center"
                )
        elif self.state == self.GAME_SCREEN:
            self.camera.use()
            self.level.draw()
            self.player.draw()
            self.gui_camera.use()
            if self.help_overlay:
                self._draw_help_overlay()

    def on_update(self, delta_time):
        if self.state == self.GAME_SCREEN:
            self.physics_engine.update()
            self.player.update(delta_time)
            self._center_camera_to_player()

    def on_key_press(self, key, modifiers):
        if self.state == self.START_SCREEN:
            if key == arcade.key.SPACE:
                self.state = self.GAME_SCREEN
        elif self.state == self.GAME_SCREEN:
            if key == arcade.key.UP or key == arcade.key.W:
                if self.physics_engine.can_jump():
                    self.player.jump()
            elif key == arcade.key.DOWN or key == arcade.key.S:
                self.player.crouch()
            elif key == arcade.key.LEFT or key == arcade.key.A:
                self.player.move_left()
            elif key == arcade.key.RIGHT or key == arcade.key.D:
                self.player.move_right()
            elif key == arcade.key.H:
                self.help_overlay = not self.help_overlay

    def on_key_release(self, key, modifiers):
        if self.state == self.GAME_SCREEN:
            if key in (arcade.key.LEFT, arcade.key.A, arcade.key.RIGHT, arcade.key.D):
                self.player.stop()
            elif key in (arcade.key.DOWN, arcade.key.S):
                self.player.stand()

    def _center_camera_to_player(self):
        screen_center_x = self.player.sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player.sprite.center_y - (self.camera.viewport_height / 2)
        if hasattr(self.level, 'width'):
            screen_center_x = max(screen_center_x, 0)
            screen_center_x = min(screen_center_x, self.level.width - self.camera.viewport_width)
        if hasattr(self.level, 'height'):
            screen_center_y = max(screen_center_y, 0)
            screen_center_y = min(screen_center_y, self.level.height - self.camera.viewport_height)
        camera_pos = screen_center_x, screen_center_y
        self.camera.move_to(camera_pos)

    def _draw_help_overlay(self):
        arcade.draw_rectangle_filled(
            self.width / 2,
            self.height / 2,
            self.width,
            self.height,
            (255, 255, 255, 220)
        )
        arcade.draw_text(
            "Controls",
            self.width / 2,
            self.height - 60,
            arcade.color.BLUE,
            64,
            anchor_x="center"
        )
        controls = [
            ("← →", "Move left/right"),
            ("↑", "Jump"),
            ("↓", "Duck"),
            ("Space", "Action (talk, open, etc.)"),
            ("H", "Show/hide this help")
        ]
        start_y = self.height - 120
        for i, (key, desc) in enumerate(controls):
            y = start_y - (i * 60)
            arcade.draw_text(
                key,
                self.width / 2 - 180,
                y,
                arcade.color.BLACK,
                48
            )
            arcade.draw_text(
                desc,
                self.width / 2 - 100,
                y + 8,
                arcade.color.DARK_GRAY,
                40
            )

def run_game():
    window = PelucheGame(1280, 840, "Peluche Express")
    window.setup()
    arcade.run()

__all__ = ["PelucheGame", "run_game"]