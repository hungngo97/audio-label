#Load the necessary python libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import librosa
import soundfile as sf
import os

FILE_SIZE = 1   #Length of each sample in seconds
SAMPLING_RATE = 44100
SHOTS = 5

def change_wav_file(file_path, sr=SAMPLING_RATE, n_fft=2048, hop_length=512, n_mels=128, fmin=20, fmax=8300, top_db=80):
    wav,sr = librosa.load(file_path,sr=sr)    # Librosa converts audio data to mono by default
    if wav.shape[0]<FILE_SIZE*sr:
        print('Size less than 1s, updating file...')
        wav=np.pad(wav,int(np.ceil((FILE_SIZE*sr-wav.shape[0])/2)),mode='reflect')
    else:
        wav=wav[:FILE_SIZE*sr]
    # Override existing file
    sf.write(file_path, wav, 44100)


for subdir, dirs, files in os.walk('./tasks'):
    for file in files:
        print(os.path.join(subdir, file))
        curr_file = os.path.join(subdir, file)
        change_wav_file(curr_file)


