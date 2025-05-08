# content_pipeline/gif_stitcher.py
import os
from PIL import Image

def stitch_gif(image_paths, output_path, duration=500):
    frames = [Image.open(p) for p in image_paths if os.path.exists(p)]
    if not frames:
        raise ValueError("No valid images to stitch")
    frames[0].save(output_path, format='GIF', save_all=True, append_images=frames[1:], duration=duration, loop=0)
    return output_path