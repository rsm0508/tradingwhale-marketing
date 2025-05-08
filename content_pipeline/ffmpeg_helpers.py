# content_pipeline/ffmpeg_helpers.py
import subprocess

def optimize_gif(input_gif, output_gif):
    cmd = [
        "ffmpeg", "-y", "-i", input_gif,
        "-filter_complex", "[0:v] fps=10,scale=480:-1:flags=lanczos", output_gif
    ]
    try:
        subprocess.run(cmd, check=True)
        return output_gif
    except Exception as e:
        return f"[Error optimizing gif: {str(e)}]"
