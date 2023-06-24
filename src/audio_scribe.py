#%%
import os
import torch
import whisper
from utils import get_device

def audio_scribe(audio_filepath: str, outfile_path: str):
    device = get_device()
    try:
        model = whisper.load_model('base.en', device = device)
    except:
        model = whisper.load_model('base.en', device = 'cpu')
    
    result = model.transcribe(audio_filepath, fp16 = False)
    with open(f'{outfile_path}.txt', 'w') as file:
        file.write(result['text'])
    print("Audio file scribed")
#%%
if __name__ == '__main__':
    audio_scribe(audio_filepath = '../Tests/happybirthday.mp4',
                 outfile_path = '../Tests/happybirthdayscript')
# %%
