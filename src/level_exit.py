# End zone/level exit logic for Peluche Express

def check_end_zone_transition(game):
    if game.end_zone_avg_x is not None and game.players:
        player = game.players[0]
        if player.center_x >= game.end_zone_avg_x:
            print("End Zone triggered! Starting exit animation...")
            game.state = "level_exit"
            game.exit_fade = 0.0
            game.exit_fade_speed = 0.03
            game.exit_player_walk = False
            game.exit_player_offscreen = False
            game.exit_timer = 0.0
            player.input_disabled = True
            player.forced_walk = True
            game.exit_camera_pos = game.camera.position
