import arcade

def main():
    # Load the tilemap
    tile_map = arcade.load_tilemap("tilemaps/map1.tmx", scaling=1.0)
    print("--- Object Layers and Objects ---")
    print(tile_map.object_lists.keys())
    for layer_name, obj_list in tile_map.object_lists.items():
        print(f"Layer: {layer_name}")
        for obj in obj_list:
            print(f"  x={getattr(obj, 'x', None)} y={getattr(obj, 'y', None)} width={getattr(obj, 'width', None)} height={getattr(obj, 'height', None)} gid={getattr(obj, 'gid', None)} name={getattr(obj, 'name', None)} type={getattr(obj, 'type', None)} shape={getattr(obj, 'shape', None)} properties={getattr(obj, 'properties', None)}")
    print("--- End Object Dump ---")

if __name__ == "__main__":
    main()
