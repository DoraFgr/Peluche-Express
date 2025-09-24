# Camera utility functions for Peluche Express

def update_camera(game):
    """Camera always follows Player 1."""
    if not game.players:
        return
    player = game.players[0]
    left_deadzone = game.camera.viewport_width * 0.4
    right_deadzone = game.camera.viewport_width * 0.6
    cam_left = game.camera.position[0]
    target_x = game.camera.position[0]
    if player.center_x < cam_left + left_deadzone:
        target_x = player.center_x - left_deadzone
    elif player.center_x > cam_left + right_deadzone:
        target_x = player.center_x - right_deadzone
    if game.tile_map:
        map_width = game.tile_map.width * game.tile_map.tile_width
        target_x = max(0, min(target_x, map_width - game.camera.viewport_width))
    game.camera.move_to((target_x, game.camera.position[1]), 0.2)
