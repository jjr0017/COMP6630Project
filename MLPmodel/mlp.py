import random
import numpy as np
from tqdm import trange
from MLPmodel.layers import *

np.random.seed(1)

class MLP:
    def __init__(self, inputNodes, hiddenLayers, hiddenLayerNodes, outputNodes, learningRate, epochs):
        self.inputNodes = inputNodes
        self.hiddenLayers = hiddenLayers
        self.hiddenLayerNodes = hiddenLayerNodes
        self.outputNodes = outputNodes
        self.learningRate = learningRate
        self.epochs = epochs
    
        self.network = []
        self.train_log = []
        self.val_log = []

        self.setUpNetwork()

    def setUpNetwork(self):
        self.network.append(Dense(self.inputNodes, self.hiddenLayerNodes, self.learningRate))
        for _ in range(self.hiddenLayers-1):
            self.network.append(ReLU())
            self.network.append(Dense(self.hiddenLayerNodes, self.hiddenLayerNodes, self.learningRate))
        self.network.append(ReLU())
        self.network.append(Dense(self.hiddenLayerNodes, self.outputNodes, self.learningRate))

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
        return activations

    def backward(self, layer_inputs, inital_loss_grad):
        loss_grad = inital_loss_grad
        for layer_index in range(len(self.network))[::-1]:
            layer = self.network[layer_index]
            loss_grad = layer.backward(layer_inputs[layer_index], loss_grad)

    def iterate_minibatches(self, inputs, targets, batchsize):
        assert len(inputs) == len(targets)
        if len(inputs) < batchsize:
            batchsize = len(inputs)
        for start_idx in range(0, len(inputs) - batchsize + 1, batchsize):
            excerpt = slice(start_idx, start_idx + batchsize)
            yield inputs[excerpt], targets[excerpt]

    def predict(self, X):
        logits = self.forward(X)[-1]
        return logits.argmax(axis=-1)
        
    def train(self, X, y):
        X = np.array(X)
        y = np.array(y)
        for epoch in trange(0, self.epochs, 1, desc='Training'):
            for x_batch, y_batch in self.iterate_minibatches(X, y, 25):
                layer_activations = self.forward(x_batch)

                layer_inputs = [x_batch]+layer_activations
                logits = layer_activations[-1]

                # loss = self.softmax_crossentropy_with_logits(logits, y_batch)
                loss_grad = self.grad_softmax_crossentropy_with_logits(logits, y_batch)
                self.backward(layer_inputs, loss_grad)          
            
            self.train_log.append(np.mean(self.predict(X)==y))

            # print('epoch: %d/%d' % (epoch+1, self.epochs))
            # print('\ttrain accuracy =      %.02f%%' % (self.train_log[-1]*100))
            if (self.train_log[-1] == 1):
                print('100%% training accuracy reached')
                return