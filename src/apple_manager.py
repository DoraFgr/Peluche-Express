import arcade

# Apple collection logic for Peluche Express

def check_apple_collection(game):
    """Check if any player collects any apples (shared counter)."""
    if not game.players or "Apples" not in game.scene.name_mapping:
        return
    apple_list = game.scene.name_mapping["Apples"]
    for player in game.players:
        collected_apples = arcade.check_for_collision_with_list(player, apple_list)
        for apple in collected_apples:
            apple.remove_from_sprite_lists()
            game.apples_collected += 1
            print(f"Apple collected! {game.apples_collected}/{game.total_apples}")
