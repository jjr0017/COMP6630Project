import sys
import os
import argparse
import json
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import normalize
from MLPmodel.mlp import MLP
import pickle

BEATSAMPLES = 100

def getArgParser():
    desc =  'This program runs a genre classification Multi Level Perceptron neural network\n\n'
    desc += 'An input MP3 file and a genre is classified based on that data' 

    parser = argparse.ArgumentParser(
        prog = 'genreClassificationDriver: MLP genre classification',
        description = desc,
        epilog = "" # TODO
    )
    parser.add_argument('--song', type=str, help='MP3 file of song to decide genre', required=True)

    return parser

def extractData(jsonFile):
    X = []
    y = []
    genreMap = {}
    f = open(jsonFile)
    jsonData = json.load(f)
    f.close()
    xEntry = np.zeros(1 + 1 + BEATSAMPLES*12 + BEATSAMPLES + BEATSAMPLES*6 + BEATSAMPLES + BEATSAMPLES)

    beats = jsonData['beats']
    samples = beats[:BEATSAMPLES] # TODO what if BEATSAMPLES > len(beats)
    if len(samples) < BEATSAMPLES:
        print('song too short to classify')
        return
    idx = 0
    # tempo
    xEntry[idx] = jsonData['tempo']
    idx += 1
    # tuning
    xEntry[idx] = jsonData['tuning']
    idx += 1
    # chromagram samples 12 bands
    # numSamples = len(jsonData['chromagram'][0])
    for i in range(12):
        for counter in range(len(samples)):
            jsonIdx = samples[counter]
            xEntry[idx] = jsonData['chromagram'][i][jsonIdx]
            idx += 1

    # spec_bw samples 
    # numSamples = len(jsonData['spec_bw'][0])
    # maxSample = np.max(jsonData['spec_bw'])
    for counter in range(len(samples)):
        jsonIdx = samples[counter]
        xEntry[idx] = jsonData['spec_bw'][0][jsonIdx]
        idx += 1
    # constrast samples 6 bands
    # numSamples = len(jsonData['contrast'][0])
    # maxSample = np.max(jsonData['contrast'])
    for i in range(6):
        for counter in range(len(samples)):
            jsonIdx = samples[counter]
            xEntry[idx] = jsonData['contrast'][i][jsonIdx]
            idx += 1

    # maxRolloff samples
    # numSamples = len(jsonData['maxRolloff'][0])
    # maxSample = np.max(jsonData['maxRolloff'])
    for counter in range(len(samples)):
        jsonIdx = samples[counter]
        xEntry[idx] = jsonData['maxRolloff'][0][jsonIdx]
        idx += 1
    # minRolloff samples
    # numSamples = len(jsonData['minRolloff'][0])
    # maxSample = np.max(jsonData['minRolloff'])
    for counter in range(len(samples)):
        jsonIdx = samples[counter]
        xEntry[idx] = jsonData['minRolloff'][0][jsonIdx]
        idx += 1
    assert idx == len(xEntry)
    X.append(xEntry)
    if jsonData['genre'] not in genreMap:
        genreMap[jsonData['genre']] = len(genreMap)
    y.append(genreMap[jsonData['genre']])

    return X, y, genreMap

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

def main(args):
    songPath = args.song
    jsonFilename = songPath.replace('.mp3', '.json')
    createJsonFile(songPath)
    X, y, genreMap = extractData(jsonFilename)
    
    with open('data/learnedModel.mlp', 'rb') as modelFile:
        model = pickle.load(modelFile)

    with open('data/genreMap.map', 'rb') as genreFile:
        genreMap = pickle.load(genreFile)

    prediction = model.predict(X)[0]

    print("The model predicts this song to be a " + list(genreMap.keys())[list(genreMap.values()).index(prediction)] + " song")

if __name__ == '__main__':
    parser = getArgParser()
    args = parser.parse_args()
    main(args)
