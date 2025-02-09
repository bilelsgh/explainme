"""
Utils function for streamlit app
"""
import importlib.util
import os
import re
import shutil

from config.config import manim_code_path, video_path


def clean_dir(video: bool, code: bool) -> None:
    """
    Clean video or/and code folder(s)

    :param video: (bool) If True remove every file in the video folder
    :param code: (bool) If True remove every file in the code folder
    """
    if video:
        for dir in os.listdir(video_path):
            shutil.rmtree(os.path.join(video_path, dir))

    if code:
        for code_file in os.listdir(manim_code_path):
            if not ("__" in code_file):
                os.remove(os.path.join(manim_code_path, code_file))


def generate_video(manim_code: str) -> None:
    """
    Execute manim code to generate a video

    :param manim_code: manim python code
    """

    clean_dir(True, True)
    file_path = f"{manim_code_path}/code.py"

    manim_code = re.sub(r"```python|```", "", manim_code)
    code_to_export = (
        f'from manim import *\nconfig.media_dir="{video_path}"\n{manim_code}'
    )

    with open(file_path, "w") as f:
        f.write(code_to_export)

    # Load the file as a package
    spec = importlib.util.spec_from_file_location("dynamic_scene", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Run the manim code
    scene_instance = module.DynamicScene()
    scene_instance.render()
