#%%
import os
import ffmpeg

def get_video_and_audio(filename: str):
    input = ffmpeg.input(filename)
    return input.video, input.audio

#%%
def stitch_movie(files_dir: str, outfile_name: str):
    clips = [os.path.join(files_dir, file) for file in os.listdir(files_dir)]
    
    to_merge = []
    for clip in clips:
        v, a = get_video_and_audio(clip)
        to_merge.append(v)
        to_merge.append(a)
    joined = ffmpeg.concat(*to_merge,
                            v = 1,
                            a = 1).node
    out_path = f"{files_dir}/{outfile_name}.mp4"
    ffmpeg.output(joined[0], 
                  joined[1], 
                  out_path).run()

    print("Files merged")
#     return out_path

# %%
if __name__ == "__main__":
    files_dir = "../Videos/TeYang"
    stitch_movie(files_dir, "happybirthday")
# %%
