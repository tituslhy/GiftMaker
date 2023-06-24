#%%
import os
from dotenv import load_dotenv
load_dotenv()
import ffmpeg
from typing import List

def stitch_movie(files_dir: str, outfile_name: str):
    clips = []
    for file in os.listdir(files_dir):
        file_dir = os.path.join(files_dir, file)
        clips.append(ffmpeg.input(file_dir))
    try:
        (
            ffmpeg
            .concat(
                *clips
                )
            .output(f"{files_dir}/{outfile_name}.mp4")
            .run()
        )
    except Exception as e:
        print(e)
    print("Files merged")
# %%
if __name__ == "__main__":
    files_dir = "./Tests"
    stitch_movie(files_dir, "happybirthday")