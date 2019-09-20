import numpy as np
import os.path as path


class NeurlN(object):

    def __init__(self, learning_rate=0.1, start_weight=0):
        self.weights_0_1 = np.random.normal(0.0, 2 ** -0.5, (8, 7))
        self.weights_0_2 = np.random.normal(0.0, 2 ** -0.5, (4, 8))
        self.weights_1_2 = np.random.normal(0.0, 1, (1, 4))
        self.sigmoid_mapper = np.vectorize(self.sigmoid)
        self.learning_rate = learning_rate
        self.start_w = start_weight

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def predict(self, inputs):

        if not self.start_w:
            inputs_1 = np.dot(self.weights_0_1, inputs)
            outputs_1 = self.sigmoid_mapper(inputs_1)

            inputs_2 = np.dot(self.weights_0_2, outputs_1)
            outputs_2 = self.sigmoid_mapper(inputs_2)

            inputs_3 = np.dot(self.weights_1_2, outputs_2)
            outputs_3 = self.sigmoid_mapper(inputs_3)
        else:
            inputs_1 = np.dot(np.loadtxt(path.abspath("weight_0_1")), inputs)
            outputs_1 = self.sigmoid_mapper(inputs_1)

            inputs_2 = np.dot(np.loadtxt(path.abspath("weight_0_2")), outputs_1)
            outputs_2 = self.sigmoid_mapper(inputs_2)

            inputs_3 = np.dot(np.loadtxt(path.abspath("weight_1_2")), outputs_2)
            outputs_3 = self.sigmoid_mapper(inputs_3)
        return outputs_3

    def train(self, inputs, expected_predict):
        inputs_1 = np.dot(self.weights_0_1, inputs)
        outputs_1 = self.sigmoid_mapper(inputs_1)

        inputs_2 = np.dot(self.weights_0_2, outputs_1)
        outputs_2 = self.sigmoid_mapper(inputs_2)

        inputs_3 = np.dot(self.weights_1_2, outputs_2)
        outputs_3 = self.sigmoid_mapper(inputs_3)
        actual_predict = outputs_3[0]

        error_layer_1_2 = np.array([actual_predict - expected_predict])
        gradient_layer_1_2 = actual_predict * (1 - actual_predict)
        weights_delta_layer_1_2 = error_layer_1_2 * gradient_layer_1_2
        self.weights_1_2 -= (np.dot(weights_delta_layer_1_2, outputs_2.reshape(1, len(outputs_2)))) * self.learning_rate
        #print(error_layer_1_2)
        #print(gradient_layer_1_2)
        #print(weights_delta_layer_1_2)
        #print(self.weights_1_2)
        #print("----------------------------------------------------------")
        error_layer_0_1 = weights_delta_layer_1_2 * self.weights_1_2
        gradient_layer_0_1 = outputs_2 * (1 - outputs_2)
        weights_delta_layer_0_1 = error_layer_0_1 * gradient_layer_0_1
        self.weights_0_2 -= np.dot(outputs_1.reshape(len(outputs_1), 1), weights_delta_layer_0_1).T * self.learning_rate
        self.weights_0_2 = np.where(self.weights_0_2 > -0.3, self.weights_0_2, 0)
        #print(error_layer_0_1)
        #print(gradient_layer_0_1)
        #print(weights_delta_layer_0_1)
        #print(np.dot(outputs_1.reshape(len(outputs_1), 1), weights_delta_layer_0_1).T * self.learning_rate)
        #print(self.weights_0_2)
        #print("----------------------------------------------------------")
        error_layer_0_2 = weights_delta_layer_0_1.dot(self.weights_0_2)
        gradient_layer_0_2 = outputs_1 * (1 - outputs_1)
        weights_delta_layer_0_2 = error_layer_0_2 * gradient_layer_0_2
        self.weights_0_1 -= np.dot(inputs.reshape(len(inputs), 1), weights_delta_layer_0_2).T * self.learning_rate
        self.weights_0_1 = np.where(self.weights_0_1 > 0, self.weights_0_1, 0)
        #print(error_layer_0_2)
        #print(gradient_layer_0_2)
        #print(weights_delta_layer_0_2)
        #print("----")
        #print(np.dot(inputs.reshape(len(inputs), 1), weights_delta_layer_0_2).T * self.learning_rate )
        #print(self.weights_0_1)
    def save(self):
        np.savetxt("weight_0_1", self.weights_0_1, fmt='%1.8e')
        np.savetxt("weight_0_2", self.weights_0_2, fmt='%1.8e')
        np.savetxt("weight_1_2", self.weights_1_2, fmt='%1.8e')