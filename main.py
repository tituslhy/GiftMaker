#%%
from src.movieStitcher import stitch_movie
from src.audio_scribe import audio_scribe
from src.summarise import LLM_write

#%%
def main(root: str,
         recipient: str,
         prompt_LLM: bool = False,
         LLM_setting: str = None
         ):
    """Stitches separate video files into a single movie, scribes the movie
    and if propmt_LLM is True, prompts the LLM of choice for a reply.

    Args:
        root (str): Directory containing the videos
        recipient (str): Name of friend receiving the gift
        prompt_LLM (bool, optional): Setting to prompt LLM. Defaults to False.
        LLM_setting: Only accepts "HuggingFace" or "OpenAI"
    """
    
    stitched_movie_title = f"happybirthday_{recipient}"
    script_path = f"./{root}/{stitched_movie_title}_script"
    movie_path = stitch_movie(root, stitched_movie_title)
    txt_path = audio_scribe(movie_path, script_path)
    print("Stitching and scribing done!")
    
    if prompt_LLM:
        with open(txt_path, 'r') as f:
            text = f.read()
        return LLM_write(text, LLM_setting)

#%%
if __name__ == "__main__":
    recipient = "TeYang"
    root = f"./Videos/{recipient}"
    main(root, recipient)
# %%
