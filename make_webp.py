"""
Ivolve Studios — WebP Converter (one-time repo pass)
=====================================================
Place this file in the ROOT of your ivolve-website repo folder
(same level as index.html) and run it by double-clicking
"Make WebP.bat".

What it does:
  - Walks the images/ folder (all subfolders)
  - For every .jpg / .jpeg it creates a matching .webp beside it
    (same name, same folder — e.g. hero.jpg -> hero.webp)
  - Skips files that already have an up-to-date .webp
  - Never touches or modifies your original JPEGs

Requires: Python 3 with Pillow  (pip install Pillow)
"""

import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Pillow is not installed. Run this first:  pip install Pillow")
    sys.exit(1)

WEBP_QUALITY = 80
ROOT = Path(__file__).resolve().parent / "images"

def main():
    if not ROOT.exists():
        print(f"Could not find an 'images' folder next to this script.")
        print(f"Expected: {ROOT}")
        print("Make sure this script sits in the repo root beside index.html.")
        sys.exit(1)

    jpgs = [p for p in ROOT.rglob("*") if p.suffix.lower() in (".jpg", ".jpeg")]
    print(f"Found {len(jpgs)} JPEG images under {ROOT}\n")

    made, skipped, failed = 0, 0, 0
    saved_bytes = 0

    for jpg in jpgs:
        webp = jpg.with_suffix(".webp")
        if webp.exists() and webp.stat().st_mtime >= jpg.stat().st_mtime:
            skipped += 1
            continue
        try:
            with Image.open(jpg) as im:
                if im.mode in ("P", "RGBA"):
                    im = im.convert("RGB")
                im.save(webp, "WEBP", quality=WEBP_QUALITY, method=6)
            saved = jpg.stat().st_size - webp.stat().st_size
            saved_bytes += max(saved, 0)
            made += 1
            print(f"  + {webp.relative_to(ROOT.parent)}  "
                  f"({jpg.stat().st_size//1024}KB -> {webp.stat().st_size//1024}KB)")
        except Exception as e:
            failed += 1
            print(f"  ! FAILED {jpg.name}: {e}")

    print("\n================ SUMMARY ================")
    print(f"  Created : {made} .webp files")
    print(f"  Skipped : {skipped} (already up to date)")
    print(f"  Failed  : {failed}")
    print(f"  Space saved vs JPEG: {saved_bytes/1024/1024:.1f} MB")
    print("==========================================")
    print("\nNext step: open GitHub Desktop — you'll see all the new")
    print(".webp files listed. Commit and push to deploy them.")

if __name__ == "__main__":
    main()
