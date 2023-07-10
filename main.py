#%%
import argparse
import os
from src.movieStitcher import stitch_movie
from src.audio_scribe import audio_scribe
from src.summarise import LLM_write

#%%
parser = argparse.ArgumentParser()
parser.add_argument('--root',
                    type = str,
                    required = True,
                    help = 'Path to directory containing video files')
parser.add_argument('--star',
                    type = str,
                    required = True,
                    help = 'Recipient of the gift')
parser.add_argument('--LLM',
                    type = str,
                    required = False,
                    help = 'Whether to use LLM in code. Accepts only "OpenAI" or "HuggingFace". Defaults to None')
args = parser.parse_args()

root = args.root
recipient = args.star
if args.LLM:
    LLM_setting = args.LLM
else:
    LLM_setting = None

#%%
def main(root: str,
         recipient: str,
         LLM_setting: str = 'HugChat'
         ):
    """Stitches separate video files into a single movie, scribes the movie
    and if propmt_LLM is True, prompts the LLM of choice for a reply.

    Args:
        root (str): Directory containing the videos
        recipient (str): Name of friend receiving the gift
        LLM_setting: Only accepts "HuggingFace" or "OpenAI"
    """
    assert os.path.exists(root)
    stitched_movie_title = f"happybirthday_{recipient}"
    script_path = f"./{root}/{stitched_movie_title}_script"
    movie_path = stitch_movie(root, stitched_movie_title)
    txt_path = audio_scribe(movie_path, script_path)
    print("Stitching and scribing done!")
    
    if LLM_setting:
        with open(txt_path, 'r') as f:
            text = f.read()
        return LLM_write(text, LLM_setting)

#%%
if __name__ == "__main__":
    recipient = "Bob"
    root = f"./Videos/{recipient}"
    main(root, recipient)
# %%
