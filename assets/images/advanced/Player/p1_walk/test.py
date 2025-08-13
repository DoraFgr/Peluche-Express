import os
from PIL import Image

def slice_walk_grid(sprite_path, output_dir):
    if not os.path.exists(sprite_path):
        print(f"Sprite sheet not found: {sprite_path}")
        return
    if not os.path.exists(output_dir):
        print(f"Output directory not found: {output_dir}")
        return
    img = Image.open(sprite_path)
    frame_w = img.width // 3
    frame_h = img.height // 3
    frame_num = 1
    for row in range(3):
        for col in range(3):
            left = col * frame_w
            upper = row * frame_h
            right = left + frame_w
            lower = upper + frame_h
            frame = img.crop((left, upper, right, lower))
            out_path = f"{output_dir}/walk{frame_num}.png"
            frame.save(out_path)
            print(f"Saved {out_path}")
            frame_num += 1

# Example usage:
if __name__ == "__main__":
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sprite_path = os.path.join(current_dir, "p1_walk_spritesheet.png")
    output_dir = current_dir
    slice_walk_grid(sprite_path, output_dir)