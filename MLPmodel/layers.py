import numpy as np

class BaseLayer:
    def __init__(self):
        pass

    def forward(self, input):
        return input
    
    def backward(self, input, grad_output):
        num_units = input.shape[1]
        d_layer_d_input = np.eye(num_units)

        return np.dot(grad_output, d_layer_d_input)

class ReLU(BaseLayer):
    def __init__(self):
        pass

    def forward(self, input):
        relu_forward = np.maximum(0, input)
        return relu_forward
    
    def backward(self, input, grad_output):
        relu_grad = input > 0
        return grad_output*relu_grad

class Dense(BaseLayer):
    def __init__(self, input_units, output_units, learning_rate=0.1):
        self.learning_rate = learning_rate
        self.weights = np.random.normal(loc=0.0, scale=np.sqrt(2/(input_units+output_units)), size=(input_units,output_units))
        self.biases = np.zeros(output_units)

    def forward(self, input):
        return np.dot(input, self.weights) + self.biases
    
    def backward(self, input, grad_output):
        grad_input = np.dot(grad_output, self.weights.T)
        grad_weights = np.dot(input.T, grad_output)
        grad_biases = grad_output.mean(axis=0)*input.shape[0]

        assert grad_weights.shape == self.weights.shape and grad_biases.shape == self.biases.shape

        self.weights = self.weights - self.learning_rate*grad_weights
        self.biases = self.biases - self.learning_rate*grad_biases

        return grad_input