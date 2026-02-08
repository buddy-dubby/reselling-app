#!/usr/bin/env python3
"""
Background Remover Module
By: Buddy Dubby (Dub) 🫠

Uses rembg to remove backgrounds from product photos.
Makes listings look professional!
"""

import io
import os
from pathlib import Path
from PIL import Image

# Lazy load rembg to avoid slow startup
_rembg_session = None

def get_rembg_session():
    """Lazy load rembg session (first call downloads model ~170MB)"""
    global _rembg_session
    if _rembg_session is None:
        from rembg import new_session
        _rembg_session = new_session("u2net")
    return _rembg_session

def remove_background(input_path: str, output_path: str = None) -> str:
    """
    Remove background from an image.
    
    Args:
        input_path: Path to input image
        output_path: Path for output (optional, defaults to input_nobg.png)
    
    Returns:
        Path to the output image with transparent background
    """
    from rembg import remove
    
    # Generate output path if not provided
    if output_path is None:
        input_p = Path(input_path)
        output_path = str(input_p.parent / f"{input_p.stem}_nobg.png")
    
    # Load and process image
    with open(input_path, 'rb') as f:
        input_data = f.read()
    
    # Remove background
    output_data = remove(
        input_data,
        session=get_rembg_session(),
        alpha_matting=True,  # Better edge detection
        alpha_matting_foreground_threshold=240,
        alpha_matting_background_threshold=10,
    )
    
    # Save result
    with open(output_path, 'wb') as f:
        f.write(output_data)
    
    return output_path

def remove_background_bytes(image_bytes: bytes) -> bytes:
    """
    Remove background from image bytes.
    Returns PNG bytes with transparent background.
    """
    from rembg import remove
    
    output_data = remove(
        image_bytes,
        session=get_rembg_session(),
        alpha_matting=True,
        alpha_matting_foreground_threshold=240,
        alpha_matting_background_threshold=10,
    )
    
    return output_data

def remove_background_pil(image: Image.Image) -> Image.Image:
    """
    Remove background from PIL Image.
    Returns PIL Image with transparent background.
    """
    from rembg import remove
    
    # Convert to bytes
    buf = io.BytesIO()
    image.save(buf, format='PNG')
    input_bytes = buf.getvalue()
    
    # Process
    output_bytes = remove(
        input_bytes,
        session=get_rembg_session(),
        alpha_matting=True,
        alpha_matting_foreground_threshold=240,
        alpha_matting_background_threshold=10,
    )
    
    # Convert back to PIL
    return Image.open(io.BytesIO(output_bytes))

def add_white_background(image: Image.Image) -> Image.Image:
    """
    Add white background to transparent image.
    Good for platforms that don't support transparency.
    """
    # Create white background
    if image.mode == 'RGBA':
        background = Image.new('RGB', image.size, (255, 255, 255))
        background.paste(image, mask=image.split()[3])  # Use alpha channel as mask
        return background
    return image

def process_product_photo(input_path: str, output_dir: str = None) -> dict:
    """
    Process a product photo: remove background and create variants.
    
    Returns dict with paths to:
    - transparent: PNG with transparent background
    - white_bg: JPG with white background (good for eBay, Poshmark)
    """
    input_p = Path(input_path)
    if output_dir is None:
        output_dir = input_p.parent
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)
    
    # Load original
    with open(input_path, 'rb') as f:
        input_bytes = f.read()
    
    # Remove background
    output_bytes = remove_background_bytes(input_bytes)
    
    # Save transparent version
    transparent_path = output_dir / f"{input_p.stem}_transparent.png"
    with open(transparent_path, 'wb') as f:
        f.write(output_bytes)
    
    # Create white background version
    transparent_img = Image.open(io.BytesIO(output_bytes))
    white_bg_img = add_white_background(transparent_img)
    
    white_bg_path = output_dir / f"{input_p.stem}_white.jpg"
    white_bg_img.save(white_bg_path, 'JPEG', quality=95)
    
    return {
        "original": str(input_path),
        "transparent": str(transparent_path),
        "white_bg": str(white_bg_path)
    }

# CLI for testing
if __name__ == "__main__":
    import sys
    
    print("🫠 Dub's Background Remover")
    print("=" * 40)
    
    if len(sys.argv) < 2:
        print("Usage: python background_remover.py <image_path>")
        print("\nThis will create:")
        print("  - <name>_transparent.png (transparent background)")
        print("  - <name>_white.jpg (white background)")
        sys.exit(1)
    
    input_path = sys.argv[1]
    print(f"\nProcessing: {input_path}")
    print("(First run downloads ~170MB model, please wait...)")
    
    result = process_product_photo(input_path)
    
    print(f"\n✅ Done!")
    print(f"   Transparent: {result['transparent']}")
    print(f"   White BG:    {result['white_bg']}")
