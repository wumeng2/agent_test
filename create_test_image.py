#!/usr/bin/env python3
"""
Create a simple test image for ID card OCR testing.
Requires: pip install Pillow
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    import os

    # Create a blank white image (ID card-like proportions)
    width, height = 850, 540
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)

    # Try to use a Chinese font, fall back to default
    try:
        # Try common Chinese font paths
        font_paths = [
            '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
            '/usr/share/fonts/truetype/arphic/uming.ttc',
            '/System/Library/Fonts/PingFang.ttc',  # macOS
            'C:/Windows/Fonts/msyh.ttc',  # Windows
        ]
        font = None
        for font_path in font_paths:
            if os.path.exists(font_path):
                font = ImageFont.truetype(font_path, 28)
                break
        if font is None:
            font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()

    # Draw ID card content
    y_offset = 50

    # Title
    draw.text((50, y_offset), "居民身份证", fill='black', font=font)
    y_offset += 60

    # Fields
    fields = [
        ("姓名", "张三"),
        ("性别", "男"),
        ("民族", "汉"),
        ("出生", "1990年01月01日"),
        ("住址", "北京市东城区长安街1号院"),
        ("公民身份号码", "110101199001011234"),
    ]

    for label, value in fields:
        draw.text((50, y_offset), f"{label}: {value}", fill='black', font=font)
        y_offset += 50

    # Add some decorative lines to make it look more like an ID card
    draw.rectangle([(40, 40), (width-40, height-40)], outline='gray', width=3)

    # Save the test image
    output_path = "/home/py/test_claude/test_id_card_sample.jpg"
    img.save(output_path, quality=95)
    print(f"✓ Test ID card image created: {output_path}")
    print(f"  Size: {width}x{height}")
    print(f"\nYou can now use this image for testing:")
    print(f"  python id_card_ocr.py  # (update the image_path first)")
    print(f"  python test_id_card_ocr.py")

except ImportError:
    print("✗ Pillow not installed.")
    print("  Install it with: pip install Pillow")
except Exception as e:
    print(f"✗ Error creating test image: {e}")
