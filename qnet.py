import torch
import torch.optim as optim
import torch.nn as nn
from dnn import NeuralNetwork
import config
from action_space import ActionSpace


# if gpu is to be used
use_cuda = torch.cuda.is_available()
device = torch.device("cuda:0" if use_cuda else "cpu")

# Instantiate action space
actionSpace = ActionSpace()

# Shortcuts
Tensor = torch.Tensor
LongTensor = torch.LongTensor


class QNetAgent(object):
    def __init__(self):
        self.nn = NeuralNetwork().to(device)

        self.loss_func = nn.MSELoss()
        # self.loss_func = nn.SmoothL1Loss()

        self.optimizer = optim.Adam(params=self.nn.parameters(), lr=config.learning_rate)
        # self.optimizer = optim.RMSprop(params=mynn.parameters(), lr=learning_rate)

    def select_action(self, state, epsilon):

        random_for_egreedy = torch.rand(1)[0]

        if random_for_egreedy > epsilon:

            with torch.no_grad():

                state = Tensor(state).to(device)
                action_from_nn = self.nn(state)
                action = torch.max(action_from_nn, 0)[1]
                action = action.item()
        else:
            action = actionSpace.get_random_action()

        return action

    def optimize(self, memory):

        if len(memory) < config.batch_size:
            return

        state, action, new_state, reward, done = memory.sample(config.batch_size)

        state = Tensor(state).to(device)
        new_state = Tensor(new_state).to(device)
        reward = Tensor(reward).to(device)
        action = LongTensor(action).to(device)
        done = Tensor(done).to(device)

        new_state_values = self.nn(new_state).detach()
        max_new_state_values = torch.max(new_state_values, 1)[0]
        target_value = reward + (1 - done) * config.gamma * max_new_state_values

        predicted_value = self.nn(state).gather(1, action.unsqueeze(1)).squeeze(1)

        loss = self.loss_func(predicted_value, target_value)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        # Q[state, action] = reward + gamma * torch.max(Q[new_state])


