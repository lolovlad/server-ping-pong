import Traning
import numpy as np
import sys


def MSE(y, Y):
    return np.mean((y - Y) ** 2)

train = [([33.7, 1, 2, 1, 0.02, 0.7, 0.6], 0.6),
        ([56.8, 1, 1, 3, 0.1, 0.4, 0.75], 0.3),
        ([13.2, 0, 2, 3, -0.02, 0.8, 0.5], 0.73),
        ([45.1, 0, 3, 1, -0.3, 0.6, 0.64], 0.82),
        ([206.5, 1, 3, 3, 0.01, 0.56, 0.72], 0.66),
        ([10.7, 1, 2, 2, 0.07, 0.69, 0.40], 0.43),
        ([140.3, 0, 4, 1, -0.2, 0.56, 0.7], 0.91),
        ([0.9, 1, 2, 4, -0.9, 0.01, 0.01], 0.01),
        ([156.0, 1, 4, 4, -0.1, 0.74, 0.89], 0.92),
        ([56.5, 0, 1, 1, 0.2, 0.57, 0.57], 0.64),
        ([170.7, 1, 2, 2, 0.3, 0.84, 0.73], 0.78)
         ]

epochs = 50000
learning_rate = 0.01

network = Traning.NeurlN(learning_rate=learning_rate, start_weight=0)

#network.train(np.array(train[0][0]), np.array(train[0][1]))

for e in range(epochs):
    inputs_ = []
    correct_predictions = []
    for input_stat, correct_prediction in train:
        network.train(np.array(input_stat), correct_prediction)
        inputs_.append(np.array(input_stat))
        correct_predictions.append(np.array(correct_prediction))
    train_loss = MSE(network.predict(np.array(inputs_).T), np.array(correct_predictions))
    sys.stdout.write("\rProgress: {}, Training loss: {}".format(str(100 * e/float(epochs))[:4], str(train_loss)[:5]))
print(network.predict(np.array([170.7, 0, 4, 2, 0.3, 0.84, 0.73])))
network.save()