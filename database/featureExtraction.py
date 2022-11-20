import sys
import os
import librosa
import numpy as np
import json
from multiprocessing import Pool
from createMetadata import GENRES
import tqdm
import warnings
warnings.filterwarnings('ignore') # setting ignore as a parameter

class mp3Features:
    def __init__(self, genre, tempo, tuning, beats, chromagram, spec_bw, contrast, maxRolloff, minRolloff):
        self.genre = genre
        self.tempo = tempo
        self.tuning = tuning
        self.beats = beats
        self.chromagram = chromagram
        self.spec_bw = spec_bw
        self.contrast = contrast
        self.maxRolloff = maxRolloff
        self.minRolloff = minRolloff

def getMp3Files(folder):
    mp3Filenames = []

    root = os.getcwd()
    path = os.path.join(root, folder)

    for r, d, f in os.walk(path):
        for file in f:
            if file.endswith('.mp3'):
                mp3Filenames.append(os.path.join(r, file))

    return mp3Filenames

def getJsonFeatures(mp3File, genre):
    # print(mp3File)
    try:
        y, sr = librosa.load(mp3File)

        tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
        tuning = librosa.estimate_tuning(y=y, sr=sr)
        chromagram = librosa.feature.chroma_stft(y=y, sr=sr)
        spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
        S = np.abs(librosa.stft(y))
        contrast = librosa.feature.spectral_contrast(S=S, sr=sr)
        maxRolloff = librosa.feature.spectral_rolloff(y=y, sr=sr, roll_percent=0.99)
        minRolloff = librosa.feature.spectral_rolloff(y=y, sr=sr, roll_percent=0.01)

        featureData = mp3Features(genre, tempo, tuning, beats.tolist(), chromagram.tolist(), spec_bw.tolist(), contrast.tolist(), maxRolloff.tolist(), minRolloff.tolist())
    
        return json.dumps(featureData.__dict__)
    except:

        return ''

def createJsonFile(mp3File):
    jsonFilename = mp3File.replace('.mp3', '.json')
    if os.path.isfile(jsonFilename):
        return
    genre = ''
    for g in GENRES:
         if g in mp3File:
            genre = g
            break
    if genre == '':
        print('could not find genre')
        exit(1)
    jsonData = getJsonFeatures(mp3File, genre)

    if jsonData != '':
        f = open(jsonFilename, 'w')
        f.write(jsonData)
        f.close()

def createPool(folder, threads):
    mp3Files = getMp3Files(folder)

    pool = Pool(threads)
    for _ in tqdm.tqdm(pool.imap_unordered(createJsonFile, mp3Files), total=len(mp3Files)):
        pass

def featureExtraction(folder):
    threads = 2
    createPool(folder, threads)

def main():
    folder = os.path.join(os.getcwd(), 'data')
    if len(sys.argv) == 2:
        folder = sys.argv[1]
    elif len(sys.argv) > 2:
        print('too many args. please provide just folder to look for mp3 files')
        exit(1)

    featureExtraction(folder)

    return

if __name__ == '__main__':
    main()