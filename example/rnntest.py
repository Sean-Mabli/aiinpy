import numpy as np

class tanh:
  def forward(self, input):
    return np.tanh(input)

  def backward(self, input):
    return 1 - np.square(input)

class stablesoftmax:
  def forward(self, input):
    return np.exp(input - np.max(input)) / np.sum(np.exp(input - np.max(input)))

  def backward(self, input):
    out = np.zeros((len(input), len(input)))
    for i in range(len(input)):
      for j in range(len(input)):
        out[i, j] = input[i] * (1 if i == j else 0 - input[j])
    return out

class rnn:
  def __init__(self, outshape, type, outactivation=stablesoftmax(), hidshape=64, learningrate=0.05, inshape=None):
    self.learningrate, self.type, self.outactivation = learningrate, type, outactivation
    self.inshape, self.hidshape, self.outshape = inshape, hidshape, outshape
    
    if inshape is not None:
      self.weightsinToHid = np.random.uniform(-0.005, 0.005, (np.prod(hidshape), np.prod(inshape)))

    self.weightsHidToHid = np.random.uniform(-0.005, 0.005, (np.prod(hidshape), np.prod(hidshape)))
    self.Hidbiases = np.zeros(hidshape)

    self.weightsHidToout = np.random.uniform(-0.005, 0.005, (np.prod(outshape), np.prod(hidshape)))
    self.outbiases = np.zeros(outshape)

  def __copy__(self):
    return type(self)(self.outshape, self.type, self.outactivation, self.hidshape, self.learningrate, self.inshape)

  def modelinit(self, inshape):
    self.inshape = inshape
    self.weightsinToHid = np.random.uniform(-0.005, 0.005, (np.prod(self.hidshape), np.prod(inshape)))
    return self.outshape

  def forward(self, input):
    self.input = input
    self.Hid = np.zeros((len(self.input) + 1, self.hidshape))
    
    if self.type == 'ManyToOne':
      for i in range(len(input)):
        self.Hid[i + 1, :] = tanh().forward(self.weightsinToHid @ input[i].flatten() + self.weightsHidToHid @ self.Hid[i, :] + self.Hidbiases)

      self.out = self.outactivation.forward(self.weightsHidToout @ self.Hid[len(input), :] + self.outbiases)
    
    elif self.type == 'ManyToMany':
      self.out = np.zeros((len(self.input), self.outshape))

      for i in range(len(input)):
        self.Hid[i + 1, :] = tanh().forward(self.weightsinToHid @ input[i].flatten() + self.weightsHidToHid @ self.Hid[i, :] + self.Hidbiases)
        self.out[i, :] = self.outactivation.forward(self.weightsHidToout @ self.Hid[i + 1, :] + self.outbiases)

    return self.out

  def backward(self, outError):
    weightsinToHidΔ = np.zeros(self.weightsinToHid.shape)
    weightsHidToHidΔ = np.zeros(self.weightsHidToHid.shape)
    HidbiasesΔ = np.zeros(self.Hidbiases.shape)

    if self.type == 'ManyToOne':
      derivative = self.outactivation.backward(self.out)
      outGradient = derivative * outError if np.ndim(derivative) == 1 else derivative @ outError
      weightsHidTooutΔ = np.outer(outGradient, self.Hid[len(self.input)].T)
      outbiasesΔ = outGradient

      HidError = self.weightsHidToout.T @ outError

      for i in reversed(range(len(self.input))):
        HidGradient = np.multiply(tanh().backward(self.Hid[i + 1]), HidError)

        HidbiasesΔ += HidGradient
        weightsHidToHidΔ += np.outer(HidGradient, self.Hid[i].T)
        weightsinToHidΔ += np.outer(HidGradient, self.input[i].T)

        HidError = self.weightsHidToHid.T @ HidGradient

    elif self.type == 'ManyToMany':
      weightsHidTooutΔ = np.zeros(self.weightsHidToout.shape)
      outbiasesΔ = np.zeros(self.outbiases.shape)

      HidError = self.weightsHidToout.T @ outError[len(self.input) - 1]

      for i in reversed(range(len(self.input))):
        HidGradient = np.multiply(tanh().backward(self.Hid[i + 1]), HidError)
        outGradient = np.multiply(self.outactivation.backward(self.out[i]), outError[i])

        weightsinToHidΔ += np.outer(HidGradient, self.input[i].T)
        weightsHidToHidΔ += np.outer(HidGradient, self.Hid[i].T)
        HidbiasesΔ += HidGradient

        weightsHidTooutΔ += np.outer(outGradient, self.Hid[i].T)
        outbiasesΔ += outGradient

        HidError = self.weightsHidToHid.T @ HidGradient + self.weightsHidToout.T @ outError[i]

    self.weightsinToHid += self.learningrate * np.clip(weightsinToHidΔ, -1, 1)
    self.weightsHidToHid += self.learningrate * np.clip(weightsHidToHidΔ, -1, 1)
    self.Hidbiases += self.learningrate * np.clip(HidbiasesΔ, -1, 1)

    self.weightsHidToout += self.learningrate * np.clip(weightsHidTooutΔ, -1, 1)
    self.outbiases += self.learningrate * np.clip(outbiasesΔ, -1, 1)