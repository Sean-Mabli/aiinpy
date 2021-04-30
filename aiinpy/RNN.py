class RNN:
  def __init__(self, InputSize, OutputSize, Type, HiddenSize, LearningRate=0.05):
    self.LearningRate = LearningRate
    self.Type = Type

    self.WeightsHidToHid = np.random.randn(HiddenSize, HiddenSize) / 1000
    self.WeightsInputToHid = np.random.randn(HiddenSize, InputSize) / 1000
    self.WeightsHidToOut = np.random.randn(OutputSize, HiddenSize) / 1000

    self.HiddenBiases = np.zeros(HiddenSize)
    self.OutputBiases = np.zeros(OutputSize)

  def ForwardProp(self, InputLayer):
    self.InputLayer = InputLayer
    self.Hidden = np.zeros((len(self.InputLayer) + 1, self.WeightsHidToHid.shape[0]))

    for i in range(len(InputLayer)):
      self.Hidden[i + 1, :] = Tanh(self.WeightsInputToHid @ InputLayer[i] + self.WeightsHidToHid @ self.Hidden[i, :] + self.HiddenBiases)

    self.Output = StableSoftMax(self.WeightsHidToOut @ self.Hidden[len(InputLayer), :] + self.OutputBiases)
    return self.Output

  def BackProp(self, OutputError):
    OutputGradient = np.multiply(DerivativeOfStableSoftMax(self.Output), OutputError)
    self.WeightsHidToOut += np.outer(np.transpose(self.Hidden[len(InputLayer), :]), OutputGradient) * self.LearningRate

    self.HiddenError = np.zeros((self.Hidden.shape))
    self.HiddenError[len(InputLayer)] = self.WeightsHidToHid @ OutputError

    for i in reversed(range(len(InputLayer))):
      self.HiddenGradient = np.multiply(DerivativeOfTanh(self.Output), FollowingLayerError)