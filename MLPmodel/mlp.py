import random
import numpy as np
from tqdm import trange
from sklearn.model_selection import StratifiedKFold
from MLPmodel.layers import *

class MLP:
    def __init__(self, inputNodes, hiddenLayers, hiddenLayerNodes, outputNodes, learningRate, epochs, Kfolds):
        self.inputNodes = inputNodes
        self.hiddenLayers = hiddenLayers
        self.hiddenLayerNodes = hiddenLayerNodes
        self.outputNodes = outputNodes
        self.learningRate = learningRate
        self.epochs = epochs
        self.Kfolds = Kfolds
    
        self.network = []
        self.train_log = []
        self.val_log = []

        self.setUpNetwork()

    def setUpNetwork(self):
        self.network.append(Dense(self.inputNodes, self.hiddenLayerNodes))
        for _ in range(self.hiddenLayers-1):
            self.network.append(ReLU())
            self.network.append(Dense(self.hiddenLayerNodes, self.hiddenLayerNodes))
        self.network.append(ReLU())
        self.network.append(Dense(self.hiddenLayerNodes, self.outputNodes))

    def softmax_crossentropy_with_logits(self, logits, reference_answers):
        logits_for_answers = logits[np.arange(len(logits)), reference_answers]

        xentropy = - logits_for_answers + np.log(np.sum(np.exp(logits),axis=1))
        return xentropy

    def grad_softmax_crossentropy_with_logits(self, logits, reference_answers):
        ones_for_answers = np.zeros_like(logits)
        ones_for_answers[np.arange(len(logits)),reference_answers] = 1

        softmax = np.exp(logits) / np.exp(logits).sum(axis=-1,keepdims=True)
        return (- ones_for_answers+softmax) / logits.shape[0]

    def forward(self, X):
        activations = []
        layerInput = X

        for l in self.network:
            activations.append(l.forward(layerInput))
            layerInput = activations[-1]

        assert len(activations) == len(self.network)
        # print(activations)
        return activations

    def iterate_minibatches(self, inputs, targets, batchsize, shuffle=False):
        assert len(inputs) == len(targets)
        if shuffle:
            indices = np.random.permutation(len(inputs))
        for start_idx in range(0, len(inputs) - batchsize + 1, batchsize):
            if shuffle:
                excerpt = indices[start_idx:start_idx + batchsize]
            else:
                excerpt = slice(start_idx, start_idx + batchsize)
            yield inputs[excerpt], targets[excerpt]

    def predict(self, X):
        logits = self.forward(X)[-1]
        print(logits.argmax(axis=-1))
        return logits.argmax(axis=-1)
        
    def train(self, X, y):
        X = np.array(X)
        y = np.array(y)
        kf = StratifiedKFold(n_splits=self.Kfolds)
        for epoch in trange(0, self.epochs, 1):
            for x_batch, y_batch in self.iterate_minibatches(X, y, 20, False):
                layer_activations = self.forward(x_batch)
                layer_inputs = [x_batch]+layer_activations
                logits = layer_activations[-1]

                # loss = self.softmax_crossentropy_with_logits(logits, y_batch)
                loss_grad = self.grad_softmax_crossentropy_with_logits(logits, y_batch)
                
                for layer_index in range(len(self.network))[::-1]:
                    layer = self.network[layer_index]
                    loss_grad = layer.backward(layer_inputs[layer_index], loss_grad)
            
            self.train_log.append(np.mean(self.predict(X)==y))
            print(y)

            print('epoch: %d/%d' % (epoch+1, self.epochs))
            print('\ttrain accuracy =      %.03f%%' % self.train_log[-1])