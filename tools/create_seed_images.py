"""
Create example seed images for testing

Generates simple product-themed placeholder images.
"""
from PIL import Image, ImageDraw, ImageFont
import os

OUTPUT_DIR = "examples/seed-images"

def create_product_image(filename, bg_color, product_name, accent_color):
    """Create a simple product placeholder image."""
    # Create 1024x1024 image
    img = Image.new('RGB', (1024, 1024), bg_color)
    draw = ImageDraw.Draw(img)

    # Try to load a nice font, fall back to default
    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 120)
        font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 60)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Draw product name
    bbox = draw.textbbox((0, 0), product_name, font=font_large)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (1024 - text_width) // 2
    y = (1024 - text_height) // 2 - 100

    # Draw shadow
    draw.text((x+5, y+5), product_name, font=font_large, fill=(0, 0, 0, 128))
    # Draw main text
    draw.text((x, y), product_name, font=font_large, fill=accent_color)

    # Draw subtitle
    subtitle = "Natural · Organic · Handcrafted"
    bbox2 = draw.textbbox((0, 0), subtitle, font=font_small)
    text_width2 = bbox2[2] - bbox2[0]
    x2 = (1024 - text_width2) // 2
    y2 = y + text_height + 40

    draw.text((x2, y2), subtitle, font=font_small, fill=accent_color)

    # Draw decorative circle
    circle_radius = 350
    circle_x = 512
    circle_y = 512
    draw.ellipse(
        [circle_x - circle_radius, circle_y - circle_radius,
         circle_x + circle_radius, circle_y + circle_radius],
        outline=accent_color,
        width=8
    )

    # Save
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, filename)
    img.save(filepath, 'PNG')
    print(f"Created: {filepath}")

def main():
    """Generate example seed images."""

    # Lavender Soap - purple tones
    create_product_image(
        "lavender-soap-1.png",
        bg_color="#E6D5F0",  # Light lavender
        product_name="Lavender Soap",
        accent_color="#6B4C8F"  # Deep purple
    )

    create_product_image(
        "lavender-soap-2.png",
        bg_color="#F0E6F5",  # Very light purple
        product_name="Lavender",
        accent_color="#8B5FA8"  # Medium purple
    )

    # Citrus Shower Gel - orange/yellow tones
    create_product_image(
        "citrus-gel-1.png",
        bg_color="#FFF4E0",  # Light cream
        product_name="Citrus Gel",
        accent_color="#FF8C00"  # Dark orange
    )

    create_product_image(
        "citrus-gel-2.png",
        bg_color="#FFF8DC",  # Cornsilk
        product_name="Fresh Citrus",
        accent_color="#FF6B35"  # Bright orange
    )

    # Rose Hand Cream - pink tones
    create_product_image(
        "rose-cream-1.png",
        bg_color="#FFE6F0",  # Light pink
        product_name="Rose Cream",
        accent_color="#D95B7F"  # Rose pink
    )

    create_product_image(
        "rose-cream-2.png",
        bg_color="#FFF0F5",  # Lavender blush
        product_name="Rose",
        accent_color="#C45577"  # Deep rose
    )

    print(f"\n✅ Created 6 seed images in {OUTPUT_DIR}/")
    print("\nYou can now:")
    print("1. Navigate to 'Upload Seeds' page in Streamlit")
    print("2. Upload these images")
    print("3. Or drag-drop them on the Generate Campaign page")

if __name__ == "__main__":
    main()
