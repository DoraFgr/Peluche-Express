# Input handling for Peluche Express
import arcade

def update_player_movement(game):
    # Player 1: Arrow keys
    if len(game.players) > 0:
        p1 = game.players[0]
        engine1 = game.physics_engines[0] if len(game.physics_engines) > 0 else None
        if arcade.key.LEFT in game.pressed_keys_p1 and arcade.key.RIGHT in game.pressed_keys_p1:
            p1.change_x = 0
        elif arcade.key.LEFT in game.pressed_keys_p1:
            p1.handle_input(arcade.key.LEFT, True, physics_engine=engine1)
        elif arcade.key.RIGHT in game.pressed_keys_p1:
            p1.handle_input(arcade.key.RIGHT, True, physics_engine=engine1)
        else:
            p1.handle_input(arcade.key.LEFT, False, physics_engine=engine1)
            p1.handle_input(arcade.key.RIGHT, False, physics_engine=engine1)
        p1.handle_input(arcade.key.UP, arcade.key.UP in game.pressed_keys_p1, physics_engine=engine1)
        p1.handle_input(arcade.key.DOWN, arcade.key.DOWN in game.pressed_keys_p1, physics_engine=engine1)
        p1.handle_input(arcade.key.SPACE, arcade.key.SPACE in game.pressed_keys_p1, physics_engine=engine1)
    if len(game.players) > 1:
        p2 = game.players[1]
        engine2 = game.physics_engines[1] if len(game.physics_engines) > 1 else None
        if arcade.key.A in game.pressed_keys_p2 and arcade.key.D in game.pressed_keys_p2:
            p2.change_x = 0
        elif arcade.key.A in game.pressed_keys_p2:
            p2.handle_input(arcade.key.LEFT, True, physics_engine=engine2)
        elif arcade.key.D in game.pressed_keys_p2:
            p2.handle_input(arcade.key.RIGHT, True, physics_engine=engine2)
        else:
            p2.handle_input(arcade.key.LEFT, False, physics_engine=engine2)
            p2.handle_input(arcade.key.RIGHT, False, physics_engine=engine2)
        p2.handle_input(arcade.key.UP, arcade.key.W in game.pressed_keys_p2, physics_engine=engine2)
        p2.handle_input(arcade.key.DOWN, arcade.key.S in game.pressed_keys_p2, physics_engine=engine2)
        p2.handle_input(arcade.key.SPACE, arcade.key.E in game.pressed_keys_p2, physics_engine=engine2)
