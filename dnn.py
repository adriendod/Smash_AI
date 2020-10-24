import torch
import torch.nn as nn
import config

class NeuralNetwork(nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        self.linear1 = nn.Linear(config.number_of_inputs, config.hidden_layer)
        self.linear2 = nn.Linear(config.hidden_layer, config.number_of_outputs)

        self.activation = nn.Tanh()
        # self.activation = nn.ReLU()

    def forward(self, x):
        output1 = self.linear1(x)
        output1 = self.activation(output1)
        output2 = self.linear2(output1)

        return output2