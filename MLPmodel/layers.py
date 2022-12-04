import numpy as np

class BaseLayer:
    def __init__(self):
        pass

    def forward(self, input):
        return input
    
    def backPropagate(self, input, gradientOutput):
        num_units = input.shape[1]
        d_layer_d_input = np.eye(num_units)

        return np.dot(gradientOutput, d_layer_d_input)

class ReLU(BaseLayer):
    def __init__(self):
        pass

    def forward(self, input):
        relu_forward = np.maximum(0, input)
        return relu_forward
    
    def backPropagate(self, input, gradientOutput):
        relu_grad = input > 0
        return gradientOutput*relu_grad

class Dense(BaseLayer):
    def __init__(self, input_units, output_units, learning_rate=0.1):
        self.learning_rate = learning_rate
        self.weights = np.random.normal(loc=0.0, scale=np.sqrt(2/(input_units+output_units)), size=(input_units,output_units))
        self.biases = np.zeros(output_units)

    def forward(self, input):
        return np.dot(input, self.weights) + self.biases
    
    def backPropagate(self, input, gradientOutput):
        gradientInput = np.dot(gradientOutput, self.weights.T)
        gradientWeights = np.dot(input.T, gradientOutput)
        gradientBiases = gradientOutput.mean(axis=0)*input.shape[0]

        assert gradientWeights.shape == self.weights.shape and gradientBiases.shape == self.biases.shape

        self.weights = self.weights - self.learning_rate*gradientWeights
        self.biases = self.biases - self.learning_rate*gradientBiases

        return gradientInput