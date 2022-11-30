import sys
import os
import argparse
import json
import numpy as np
from sklearn.model_selection import train_test_split, KFold
from sklearn.preprocessing import normalize
from MLPmodel.mlp import MLP
from tqdm import trange

BEATSAMPLES = 100

def getArgParser():
    desc =  'This driver runs a genre classification Multi Level Perceptron neural netwrok\n\n'
    desc += 'A preprocessiong of mp3 files to json files is required' 
    # TODO add more

    parser = argparse.ArgumentParser(
        prog = 'genreClassificationDriver: MLP genre classification',
        description = desc,
        epilog = "" # TODO
    )
    parser.add_argument('--data', type=str, help='folder containing database of json files', required=True)
    parser.add_argument('--lr', type=float, help='learning rate', required=False, default=0.1)
    parser.add_argument('--epochs', type=int, help='maximum number of epochs', required=False, default=100)
    parser.add_argument('--hiddenLayers', type=int, help='number of hidden layers', required=False, default=100)
    parser.add_argument('--hiddenLayerNodes', type=int, help='number of nodes in each hidden layer', required=False, default=100)
    parser.add_argument('--kfolds', type=int, help='number of folds for k-fold cross validation', required=False, default=5)

    return parser

def getJsonFiles(dataFolder):
    root = os.getcwd()
    path = os.path.join(root, dataFolder)

    jsonFiles = []
    for r, d, f in os.walk(path):
        for file in f:
            if file.endswith('.json'):
                jsonFiles.append(os.path.join(r, file))

    return jsonFiles

def extractData(jsonFiles):
    X = []
    y = []
    genreMap = {}
    # xEntry = np.zeros(1 + 1 + BEATSAMPLES*12 + BEATSAMPLES + BEATSAMPLES*6 + BEATSAMPLES + BEATSAMPLES)
    for i in trange(0, len(jsonFiles), 1, desc='Extracting Data'):
        if jsonFiles[i].endswith('mp3Metadata.json'):
            continue
        # print('Extracting data for %s' % jsonFiles[i])
        f = open(jsonFiles[i])
        try:
            jsonData = json.load(f)
        except:
            f.close()
            continue
        f.close()
        xEntry = np.zeros(1 + 1 + BEATSAMPLES*12 + BEATSAMPLES + BEATSAMPLES*6 + BEATSAMPLES + BEATSAMPLES)

        beats = jsonData['beats']
        samples = beats[:BEATSAMPLES] # TODO what if BEATSAMPLES > len(beats)
        if len(samples) < BEATSAMPLES:
            # song too short, throw out
            continue
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

def main(args):
    dataFolder = args.data
    jsonFilenames = getJsonFiles(dataFolder)
    X, y, genreMap = extractData(jsonFilenames)

    print('Found %d samples' % len(y))

    X = normalize(X, axis=0)
    y = np.array(y)

    initial_X_train, X_test, initial_y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=True, random_state=1)

    kf = KFold(n_splits=args.kfolds, random_state=None, shuffle=False)
    training_acc = []
    val_acc = []
    k = 1
    bestModel = None
    for train_index, val_index in kf.split(initial_X_train, initial_y_train):
        print('k (%d/%d)' % (k, args.kfolds))
        k += 1
        X_train, X_val = initial_X_train[train_index], initial_X_train[val_index]
        y_train, y_val = initial_y_train[train_index], initial_y_train[val_index]

        model = MLP(len(X_train[0]), args.hiddenLayers, args.hiddenLayerNodes, len(genreMap), args.lr, args.epochs)
        model.train(X_train, y_train)

        training_acc.append(np.mean(model.predict(X_test)==y_test))
        val_acc.append(np.mean(model.predict(X_val)==y_val))

        print('training accuracy:   %.02f%%' % (training_acc[-1]*100))
        print('validation accuracy: %.02f%%' % (val_acc[-1]*100))
        print()

        if np.max(val_acc) == val_acc[-1]:
            bestModel = model


    test_predictions = bestModel.predict(X_test)

    test_accuracy = np.mean(test_predictions==y_test)
    print('testing accuracy:    %.02f%%' % (test_accuracy*100))


if __name__ == '__main__':
    parser = getArgParser()
    args = parser.parse_args()
    main(args)