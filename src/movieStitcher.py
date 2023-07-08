#%%
import glob
import subprocess

def stitch_movie(files_dir: str, outfile_name: str):
    call = ["ffmpeg"]
    end = [
        '-map', '[v]',
        '-map', '[a]',
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-movflags','+faststart',
        f'{files_dir}/{outfile_name}.mp4' 
    ]
    aspect = "1280:720"
    clips = glob.glob(f"{files_dir}/*.mp4")
    for clip in clips:
        call.append("-i")
        call.append(clip)
    filter_string, last_line = "",""
    for i in range(len(clips)):
        filter_string += f"[{i}:v]scale={aspect}:force_original_aspect_ratio=decrease,pad={aspect}:-1:-1,setsar=1,fps=30,format=yuv420p[v{i}];"
        last_line += f"[v{i}][{i}:a]"
        if i == len(clips) - 1:
            last_line += f"concat=n={i+1}:v=1:a=1[v][a]"
    filter_string += last_line
    call.append('-filter_complex')
    call.append(filter_string)
    call.extend(end)
    subprocess.call(call)
    return f"{files_dir}/{outfile_name}.mp4"

# %%
if __name__ == "__main__":
    files_dir = "../Videos/TeYang"
    stitch_movie(files_dir, "happybirthday")
# %%
