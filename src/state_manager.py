from src.level_manager import go_to_next_level

# State management and transition helpers for Peluche Express

def handle_level_exit_update(game, delta_time):
    player = game.players[0]
    # Let player land if in air
    if abs(player.change_y) > 1:
        pass  # Wait until landed
    else:
        if not game.exit_player_walk:
            player.forced_walk = True
            player.input_disabled = True
            game.exit_player_walk = True
        if player.center_x > game.camera.position[0] + game.camera.viewport_width:
            game.exit_player_offscreen = True
    if game.exit_player_offscreen:
        game.exit_fade += game.exit_fade_speed
        if game.exit_fade >= 1.0:
            go_to_next_level(game)
    # Don't update camera (freeze)
