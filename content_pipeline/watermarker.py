# content_pipeline/watermarker.py
from PIL import Image, ImageDraw, ImageFont

def add_watermark(image_path, text="Sample – Not Advice – tradingwhale.io/disclaimer"):
    try:
        base = Image.open(image_path).convert("RGBA")
        watermark = Image.new("RGBA", base.size, (255,255,255,0))
        draw = ImageDraw.Draw(watermark)
        font = ImageFont.load_default()
        width, height = base.size
        draw.text((10, height - 20), text, fill=(255,255,255,180), font=font)
        combined = Image.alpha_composite(base, watermark)
        out_path = image_path.replace(".png", "_watermarked.png")
        combined.save(out_path)
        return out_path
    except Exception as e:
        return f"[Error watermarking image: {str(e)}]"
