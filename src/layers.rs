// class BaseLayer:
//     def __init__(self):
//         pass

//     def forward(self, input):
//         return input

//     def backPropagate(self, input, gradientOutput):
//         num_units = input.shape[1]
//         d_layer_d_input = np.eye(num_units)

//         return np.dot(gradientOutput, d_layer_d_input)

use ndarray::{prelude::*, OwnedRepr};

trait BaseLayer {
    fn forward(&self, input: Array1<f64>) -> Array1<f64> {
        return input;
    }

    fn back_propogate(&self, input: Array1<f64>, gradient_output: Array1<f64>) -> Vec<f64> {
        let num_units = input[1];
        // let d_layer_d_input = ndarray::eye(num_units);
        //         d_layer_d_input = np.eye(num_units)
        //         return np.dot(gradientOutput, d_layer_d_input)
        return vec![0.0];
    }
}

// class ReLU(BaseLayer):
//     def __init__(self):
//         pass

//     def forward(self, input):
//         relu_forward = np.maximum(0, input)
//         return relu_forward

//     def backPropagate(self, input, gradientOutput):
//         relu_grad = input > 0
//         return gradientOutput*relu_grad

trait ReLU {}

impl BaseLayer for dyn ReLU {
    fn forward(&self, input: ArrayBase<OwnedRepr<f64>, Dim<[usize; 1]>>) -> Array1<f64> {
        // let relu_forward = ndarray::maximum(0, input);
        return input;
    }

    fn back_propogate(&self, input: Array1<f64>, gradient_output: Array1<f64>) -> Vec<f64> {
        let num_units = input[1];

        return vec![1.0];
    }
}

// class Dense(BaseLayer):
//     def __init__(self, input_units, output_units, learning_rate=0.1):
//         self.learning_rate = learning_rate
//         self.weights = np.random.normal(loc=0.0, scale=np.sqrt(2/(input_units+output_units)), size=(input_units,output_units))
//         self.biases = np.zeros(output_units)

//     def forward(self, input):
//         return np.dot(input, self.weights) + self.biases

//     def backPropagate(self, input, gradientOutput):
//         gradientInput = np.dot(gradientOutput, self.weights.T)
//         gradientWeights = np.dot(input.T, gradientOutput)
//         gradientBiases = gradientOutput.mean(axis=0)*input.shape[0]

//         assert gradientWeights.shape == self.weights.shape and gradientBiases.shape == self.biases.shape

//         self.weights = self.weights - self.learning_rate*gradientWeights
//         self.biases = self.biases - self.learning_rate*gradientBiases

//         return gradientInput

struct Dense {
    learning_rate: u32,
    weights: Vec<f64>,
    biases: Vec<f64>,
}

impl Dense {
    fn new(input_units: Vec<f64>, output_units: Vec<f64>, learning_rate: f64) -> Dense {
        return Dense {
            learning_rate: todo!(),
            weights: todo!(),
            biases: todo!(),
        };
    }
}

impl BaseLayer for Dense {}
