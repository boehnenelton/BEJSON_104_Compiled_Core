#!/usr/bin/env python3
"""
Image Resizer Script
Author: Elton Boehnen (boehnenelton2024@gmail.com)
Description: Resizes images from 'images/backup/' with an additional 6% reduction
             from current size (scaling down to 384x214) while maintaining aspect ratio using Pillow.
"""
import os
import shutil
from PIL import Image

SRC_DIR = "images"
BACKUP_DIR = os.path.join(SRC_DIR, "backup")

# Current images are at 408x228.
# An additional 6% reduction means keeping 94% (100% - 6% = 94%):
# 408 * 0.94 = 383.52 -> 384x214
ADDITIONAL_REDUCTION_FACTOR = 0.94  # Reduce current size by 6% (keep 94%)

def main():
    if not os.path.exists(BACKUP_DIR):
        print(f"Error: Backup directory {BACKUP_DIR} does not exist.")
        return

    files = [f for f in sorted(os.listdir(SRC_DIR)) if os.path.isfile(os.path.join(SRC_DIR, f))]

    if not files:
        print("[INFO] No images found to process.")
        return

    print(f"[INFO] Processing {len(files)} images with additional 6% size reduction...")

    for f in files:
        src_path = os.path.join(SRC_DIR, f)
        backup_path = os.path.join(BACKUP_DIR, f)

        if not os.path.exists(backup_path):
            print(f"[WARN] Backup copy for {f} not found in {BACKUP_DIR}/. Skipping...")
            continue

        # Measure current size before resizing
        with Image.open(src_path) as current_img:
            curr_w, curr_h = current_img.size

        # Calculate new target dimensions from current size
        new_w = int(round(curr_w * ADDITIONAL_REDUCTION_FACTOR))
        new_h = int(round(curr_h * ADDITIONAL_REDUCTION_FACTOR))

        # Open original full-res image from backup to preserve quality
        with Image.open(backup_path) as orig_img:
            orig_w, orig_h = orig_img.size
            resample_filter = getattr(Image, "Resampling", Image).LANCZOS
            resized_img = orig_img.resize((new_w, new_h), resample_filter)

            # Save resized image to src_path
            resized_img.save(src_path, optimize=True)
            new_size_bytes = os.path.getsize(src_path)

            print(f"  -> {f}: {curr_w}x{curr_h} -> {new_w}x{new_h} ({new_size_bytes} bytes)")

    print("[SUCCESS] All images reduced by an additional 6%!")

if __name__ == "__main__":
    main()