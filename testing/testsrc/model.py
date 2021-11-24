import numpy as np
from alive_progress import alive_bar

class model:
  def __init__(self, InShape, OutShape, Model):
    self.InShape = InShape if isinstance(InShape, tuple) else tuple([InShape])
    self.OutShape = OutShape if isinstance(OutShape, tuple) else tuple([OutShape])
    self.Model = Model
  
  def forward(self, In):
    for i in range(len(self.Model)):
      In = self.Model[i].forward(In)
    return In

  def backward(self, OutError):
    for i in reversed(range(len(self.Model))):
      OutError = self.Model[i].backward(OutError)
    return OutError

  def train(self, InTrainData, OutTrainData, NumOfGen):
    # Data Preprocessing
    NumOfData = (set(self.InShape) ^ set(InTrainData.shape)).pop()
    if InTrainData.shape.index(NumOfData) != 0:
      x = list(range(0, len(InTrainData.shape)))
      x.pop(InTrainData.shape.index(NumOfData))
      InTrainData = np.transpose(InTrainData, tuple([InTrainData.shape.index(NumOfData)]) + tuple(x))
    if OutTrainData.shape.index(NumOfData) != 0:
      x = list(range(0, len(OutTrainData.shape)))
      x.pop(OutTrainData.shape.index(NumOfData))
      OutTrainData = np.transpose(OutTrainData, tuple([OutTrainData.shape.index(NumOfData)]) + tuple(x))

    # Training
    with alive_bar(NumOfGen) as bar:
      for _ in range (NumOfGen):
        Random = np.random.randint(0, NumOfData)
        In = InTrainData[Random]
        for i in range(len(self.Model)):
          In = self.Model[i].forward(In)

        OutError = OutTrainData[Random] - In
        for i in reversed(range(len(self.Model))):
          OutError = self.Model[i].backward(OutError)

        bar()

  def test(self, InTestData, OutTestData):
    # Data Preprocessing
    NumOfData = (set(self.InShape) ^ set(InTestData.shape)).pop()
    if InTestData.shape.index(NumOfData) != 0:
      x = list(range(0, len(InTestData.shape)))
      x.pop(InTestData.shape.index(NumOfData))
      InTestData = np.transpose(InTestData, tuple([InTestData.shape.index(NumOfData)]) + tuple(x))
    if OutTestData.shape.index(NumOfData) != 0:
      x = list(range(0, len(OutTestData.shape)))
      x.pop(OutTestData.shape.index(NumOfData))
      OutTestData = np.transpose(OutTestData, tuple([OutTestData.shape.index(NumOfData)]) + tuple(x))

    # Testing
    testcorrect = 0
    with alive_bar(NumOfData) as bar:
      for Generation in range (NumOfData):
        In = InTestData[Generation]
        for i in range(len(self.Model)):
          In = self.Model[i].forward(In)

        testcorrect += 1 if np.argmax(In) == np.argmax(OutTestData[Generation]) else 0
        bar()

    return testcorrect / NumOfData