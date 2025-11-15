"""
Shift green hues toward blue for images in shp2 while preserving yellows and reds.
This script:
 - makes a backup of shp2 images into assets/backup/shp2
 - processes PNG images in assets/images/advanced/Player/shp2
 - converts pixels from RGB to HSV, and for hues in the green range, shifts hue toward blue
 - writes modified images back to the shp2 folder

Tune parameters GREEN_HUE_RANGE and SHIFT_DEGREES to adjust behavior.
"""
from PIL import Image
import os
import shutil
import math

# Project root is the parent of the script directory
ROOT = os.path.dirname(os.path.dirname(__file__))
SHP2_DIR = os.path.join(ROOT, 'assets', 'images', 'advanced', 'Player', 'shp2')
BACKUP_DIR = os.path.join(ROOT, 'assets', 'backup', 'shp2')

# Hue ranges are in degrees (0-360)
# We'll treat green roughly 80-160 deg, teal/sea-green ~150-200, yellow ~40-80, red <40 or >320
GREEN_MIN = 80
GREEN_MAX = 160
# Teal is between green and blue; we treat it separately to apply a different (usually smaller) shift
TEAL_MIN = 150
TEAL_MAX = 200

# Shift how many degrees toward blue (blue around 200-260). Positive shifts increase hue value.
SHIFT_DEGREES = 80
# Smaller shift for teal so it becomes more blue without over-saturating
SHIFT_DEGREES_TEAL = 48

def rgb_to_hsv(r, g, b):
    r_, g_, b_ = r/255.0, g/255.0, b/255.0
    mx = max(r_, g_, b_)
    mn = min(r_, g_, b_)
    diff = mx - mn
    # hue
    if diff == 0:
        h = 0
    elif mx == r_:
        h = (60 * ((g_ - b_) / diff) + 360) % 360
    elif mx == g_:
        h = (60 * ((b_ - r_) / diff) + 120) % 360
    else:
        h = (60 * ((r_ - g_) / diff) + 240) % 360
    # saturation
    s = 0 if mx == 0 else diff / mx
    v = mx
    return h, s, v

def hsv_to_rgb(h, s, v):
    c = v * s
    x = c * (1 - abs(((h / 60.0) % 2) - 1))
    m = v - c
    if 0 <= h < 60:
        r1, g1, b1 = c, x, 0
    elif 60 <= h < 120:
        r1, g1, b1 = x, c, 0
    elif 120 <= h < 180:
        r1, g1, b1 = 0, c, x
    elif 180 <= h < 240:
        r1, g1, b1 = 0, x, c
    elif 240 <= h < 300:
        r1, g1, b1 = x, 0, c
    else:
        r1, g1, b1 = c, 0, x
    r, g, b = int((r1 + m) * 255), int((g1 + m) * 255), int((b1 + m) * 255)
    return r, g, b


def shift_hue(h, degrees):
    return (h + degrees) % 360


def get_shift_for_hue(h):
    """Return the shift degrees for hue h, or 0 if we shouldn't modify.

    Priority: if hue falls in GREEN range -> use SHIFT_DEGREES.
    Else if hue falls in TEAL range -> use SHIFT_DEGREES_TEAL.
    Otherwise return 0 (no change).
    """
    if GREEN_MIN <= h <= GREEN_MAX:
        return SHIFT_DEGREES
    if TEAL_MIN <= h <= TEAL_MAX:
        return SHIFT_DEGREES_TEAL
    return 0


def process_image(path):
    img = Image.open(path).convert('RGBA')
    px = img.load()
    w, h = img.size
    changed = False
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            # skip fully transparent
            if a == 0:
                continue
            hue, sat, val = rgb_to_hsv(r, g, b)
            shift_amt = get_shift_for_hue(hue)
            if shift_amt:
                # shift hue toward blue by shift_amt
                new_h = shift_hue(hue, shift_amt)
                # Keep saturation/brightness to preserve yellow/red unaffected areas
                nr, ng, nb = hsv_to_rgb(new_h, sat, val)
                px[x, y] = (nr, ng, nb, a)
                changed = True
    if changed:
        img.save(path)
    return changed


def main():
    if not os.path.isdir(SHP2_DIR):
        print('shp2 directory not found:', SHP2_DIR)
        return
    os.makedirs(BACKUP_DIR, exist_ok=True)
    # Backup files
    for fname in os.listdir(SHP2_DIR):
        if not (fname.lower().endswith('.png') or fname.lower().endswith('.jpg') or fname.lower().endswith('.jpeg')):
            continue
        src = os.path.join(SHP2_DIR, fname)
        dst = os.path.join(BACKUP_DIR, fname)
        if not os.path.exists(dst):
            shutil.copy2(src, dst)
            print('Backed up', fname)

    # Process images
    modified = []
    for fname in os.listdir(SHP2_DIR):
        if not (fname.lower().endswith('.png') or fname.lower().endswith('.jpg') or fname.lower().endswith('.jpeg')):
            continue
        path = os.path.join(SHP2_DIR, fname)
        print('Processing', fname)
        if process_image(path):
            modified.append(fname)
            print(' Modified:', fname)
        else:
            print(' No change:', fname)
    print('Done. Modified files:', modified)

if __name__ == '__main__':
    main()
