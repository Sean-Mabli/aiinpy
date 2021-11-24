import testsrc as ai
from alive_progress import alive_bar
import numpy as np

rnn_model = ai.rnn(InSize=1, OutSize=1, Type='ManyToMany', OutActivation=ai.identity(), LearningRate=0.01)

Data = np.genfromtxt('testing\data\Timeseries\Airpassenger.csv', dtype=int)
Data = (Data - min(Data)) / (max(Data) - min(Data)).astype(float)

TrainingData = Data[0 : 100, np.newaxis]
TestData = Data[100 :, np.newaxis]

NumOfTrainGen = 15000
NumOfTestGen = len(TestData) - 5

with alive_bar(NumOfTrainGen + NumOfTestGen) as bar:
  for Generation in range(NumOfTrainGen):
    Random = np.random.randint(0, len(TrainingData) - 5)

    In = TrainingData[Random : Random + 5]
    Out = rnn_model.forward(In)

    OutError = TrainingData[Random + 1 : Random + 6] - Out
    InError = rnn_model.backward(OutError)

    bar()

  for Generation in range(NumOfTestGen):
    In = TestData[Generation : Generation + 5]
    Out = rnn_model.forward(In)

    OutError = TestData[Generation + 1 : Generation + 6] - Out
    InError = rnn_model.backward(OutError)

    bar()