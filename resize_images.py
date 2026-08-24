#!/usr/bin/env python3
"""
Image Resizer Script
Author: Elton Boehnen (boehnenelton2024@gmail.com)
Description: Backs up original images to 'images/backup/' and resizes images in 'images/'
             by reducing dimensions by 62% (scaling down to 38% of original width/height)
             while maintaining aspect ratio using Pillow.
"""
import os
import shutil
from PIL import Image

SRC_DIR = "images"
BACKUP_DIR = os.path.join(SRC_DIR, "backup")
SCALE_FACTOR = 0.38  # 62% reduction = 38% remaining size

def main():
    if not os.path.exists(SRC_DIR):
        print(f"Error: {SRC_DIR} directory does not exist.")
        return

    os.makedirs(BACKUP_DIR, exist_ok=True)
    print(f"[INFO] Created backup directory: {BACKUP_DIR}")

    files = [f for f in sorted(os.listdir(SRC_DIR)) if os.path.isfile(os.path.join(SRC_DIR, f))]

    if not files:
        print("[INFO] No images found to process.")
        return

    print(f"[INFO] Backing up and resizing {len(files)} images...")

    for f in files:
        src_path = os.path.join(SRC_DIR, f)
        backup_path = os.path.join(BACKUP_DIR, f)

        # Step 1: Backup original image
        shutil.copy2(src_path, backup_path)
        print(f"  -> Backed up: {f} -> {BACKUP_DIR}/")

        # Step 2: Open and resize image
        with Image.open(src_path) as img:
            orig_w, orig_h = img.size
            new_w = int(round(orig_w * SCALE_FACTOR))
            new_h = int(round(orig_h * SCALE_FACTOR))

            # Resample using high-quality LANCZOS / Resampling.LANCZOS filter
            resample_filter = getattr(Image, "Resampling", Image).LANCZOS
            resized_img = img.resize((new_w, new_h), resample_filter)

            # Save resized image back over src_path
            resized_img.save(src_path, optimize=True)
            new_size_bytes = os.path.getsize(src_path)

            print(f"     Resized: {orig_w}x{orig_h} -> {new_w}x{new_h} ({new_size_bytes} bytes)")

    print("[SUCCESS] All images resized and original copies secured in images/backup/.")

if __name__ == "__main__":
    main()