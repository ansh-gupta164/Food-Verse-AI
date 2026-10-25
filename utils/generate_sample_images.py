"""
Generates clean sample images for the test presets using Pillow drawing.
Ensures the app has instant, local visual test files without external internet downloads.
"""

import os
from PIL import Image, ImageDraw, ImageFont


def create_sample_images(output_dir: str = "assets/samples"):
    os.makedirs(output_dir, exist_ok=True)

    items = [
        {
            "filename": "salmon_bowl.jpg",
            "bg": (245, 247, 250),
            "primary": (224, 86, 36),     # Salmon orange
            "secondary": (34, 139, 34),   # Greens
            "accent": (230, 190, 120),    # Quinoa
            "title": "Mediterranean Salmon & Quinoa Bowl",
            "subtitle": "Fresh Atlantic Salmon, Tri-Color Quinoa, Greens, Olive Oil",
            "tag": "PRESET: FOOD AUDIT"
        },
        {
            "filename": "apple_fresh.jpg",
            "bg": (250, 250, 250),
            "primary": (195, 30, 45),     # Crisp red
            "secondary": (46, 139, 87),   # Leaf green
            "accent": (139, 69, 19),      # Stem brown
            "title": "Fresh Red Gala Apple",
            "subtitle": "Firm intact epidermis, uniform pigmentation, zero bruising",
            "tag": "PRESET: FRESHNESS (FRESH)"
        },
        {
            "filename": "banana_spot.jpg",
            "bg": (255, 253, 240),
            "primary": (235, 190, 40),    # Golden yellow
            "secondary": (110, 75, 40),   # Sugar spots
            "accent": (160, 120, 50),
            "title": "Cavendish Banana (Ripened)",
            "subtitle": "Senescence sugar spotting, intact peel, peak natural sweetness",
            "tag": "PRESET: FRESHNESS (MODERATE)"
        },
        {
            "filename": "strawberry_decay.jpg",
            "bg": (245, 240, 240),
            "primary": (140, 25, 35),     # Darkened red
            "secondary": (180, 185, 190), # Mycelium grey
            "accent": (90, 95, 100),
            "title": "Pre-packed Strawberries (Spoilage)",
            "subtitle": "Visible Botrytis fungal mycelium, tissue softening, exudate",
            "tag": "PRESET: FRESHNESS (SPOILED)"
        },
        {
            "filename": "kitchen_prep.jpg",
            "bg": (235, 240, 245),
            "primary": (70, 90, 120),     # Stainless steel
            "secondary": (34, 197, 94),   # Sanitized board green
            "accent": (239, 68, 68),      # Raw board red
            "title": "Commercial Kitchen Preparation Line",
            "subtitle": "Stainless counters, color-coded boards, PPE inspection station",
            "tag": "PRESET: KITCHEN HYGIENE"
        }
    ]

    for item in items:
        filepath = os.path.join(output_dir, item["filename"])
        if os.path.exists(filepath):
            continue

        img = Image.new("RGB", (800, 550), color=item["bg"])
        draw = ImageDraw.Draw(img)

        # Draw decorative background elements
        draw.rectangle([20, 20, 780, 530], outline=(220, 225, 230), width=2)
        draw.rectangle([40, 40, 760, 100], fill=(255, 255, 255), outline=(210, 215, 220), width=1)

        # Draw Tag badge
        draw.rectangle([55, 55, 280, 85], fill=item["primary"])
        draw.text((65, 62), item["tag"], fill=(255, 255, 255))

        # Central illustration circle / platter
        center_x, center_y = 400, 290
        radius = 140
        draw.ellipse(
            [center_x - radius, center_y - radius, center_x + radius, center_y + radius],
            fill=(255, 255, 255),
            outline=item["primary"],
            width=6
        )

        # Draw inner decorative food shapes
        draw.ellipse([center_x - 90, center_y - 70, center_x + 90, center_y + 70], fill=item["primary"])
        draw.ellipse([center_x - 60, center_y - 50, center_x + 20, center_y + 30], fill=item["secondary"])
        draw.ellipse([center_x + 10, center_y - 40, center_x + 80, center_y + 40], fill=item["accent"])

        # Title & Subtitle banner
        draw.rectangle([40, 450, 760, 520], fill=(255, 255, 255), outline=(210, 215, 220), width=1)
        draw.text((60, 462), item["title"], fill=(15, 23, 42))
        draw.text((60, 490), item["subtitle"], fill=(100, 116, 139))

        img.save(filepath, "JPEG", quality=90)


if __name__ == "__main__":
    create_sample_images()
