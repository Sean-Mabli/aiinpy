import numpy as np
from emnist import extract_training_samples, extract_test_samples
import src as ai

# Create Dataset
inTrainData, outTrainData = extract_training_samples('digits')
inTestData, outTestData = extract_test_samples('digits')
inTrainData, inTestData = (inTrainData[0 : 5000] / 255) - 0.5, (inTestData[0 : 1000] / 255) - 0.5

outTrainDataReal = np.zeros((5000, 10))
for i in range(5000):
  outTrainDataReal[i, outTrainData[i]] = 1
outTestDataReal = np.zeros((1000, 10))
for i in range(1000):
  outTestDataReal[i, outTestData[i]] = 1

# CNN model
modela = ai.model((28, 28), 10, [
  ai.convmatrix(inshape=(28, 28), filtershape=(4, 3, 3), learningrate=0.01, activation=ai.relu()),
  ai.pool(stride=(2, 2), filtershape=(2, 2), opperation='Max'),
  ai.nn(outshape=10, activation=ai.stablesoftmax(), learningrate=0.1, weightsinit=(0, 0))
])

modelb = ai.model((28, 28), 10, [
  ai.conv(inshape=(28, 28), filtershape=(4, 3, 3), learningrate=0.01, activation=ai.relu()),
  ai.pool(stride=(2, 2), filtershape=(2, 2), opperation='Max'),
  ai.nn(outshape=10, activation=ai.stablesoftmax(), learningrate=0.1, weightsinit=(0, 0))
])

modelb.layers[0].filter = modela.layers[0].filter
modelb.layers[2].weights = modela.layers[2].weights
modelb.layers[2].biases = modela.layers[2].biases

a = modela.train((inTrainData, outTrainDataReal), 10)
b = modelb.train((inTrainData, outTrainDataReal), 10)

print('\n')

x = np.zeros((10, 3))
u = np.empty((10, 3), dtype=tuple)
for j in range(len(a)):
  x[j // 3, j % 3] = abs(np.round(np.sum(abs(a[j]) - abs(b[j])), 3))
  u[j // 3, j % 3] = a[j].shape

print(x)
print(u)