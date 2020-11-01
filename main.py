#!/usr/bin/python3
import melee
import random
import time
import torch
import utils
from console import *
from action_space import ActionSpace
from observation_space import Observations
from experience_replay import ExperienceReplay
from qnet import QNetAgent
from torch.utils.tensorboard import SummaryWriter

# if gpu is to be used
use_cuda = torch.cuda.is_available()
device = torch.device("cuda:0" if use_cuda else "cpu")
Tensor = torch.Tensor
LongTensor = torch.LongTensor
random_seed = 42
torch.manual_seed(random_seed)
random.seed(random_seed)

writer = SummaryWriter()

actionSpace = ActionSpace()
memory = ExperienceReplay(config.replay_mem_size)
qnet_agent = QNetAgent()

steps_total = []

frames_total = 0
solved_after = 0
solved = False

start_time = time.time()

# Main loop
step = 0
total_reward = 0
done = False
gamestate = console.step()

while True:
    if gamestate is None:
        continue
    # If in game:
    if gamestate.menu_state in [melee.Menu.IN_GAME, melee.Menu.SUDDEN_DEATH]:

        step += 1
        reward = 0

        observation_space = Observations(gamestate)
        state = observation_space.observations

        # Get action
        epsilon = utils.calculate_epsilon(frames_total)
        action = qnet_agent.select_action(state, epsilon)

        # Press button
        actionSpace.press_button(controller, action)

        for _ in range(2):
            frames_total += 1
            gamestate = console.step()
            new_observation_space = Observations(gamestate)
            new_state = new_observation_space.observations
            temp_reward = new_observation_space.reward(observation_space)
            reward += temp_reward

        memory.push(state, action, new_state, reward, done)
        loss = qnet_agent.optimize(memory)

        total_reward += reward
        state = new_state

        if done:
            done = False
        if step == 250:
            step = 0
            done = True
            writer.add_scalar('Rewards', total_reward, step)
            print("Reward: " + str(total_reward))
            writer.add_scalar('Epsilon', epsilon, step)
            if loss is not None:
                writer.add_scalar('Loss', loss, step)
                print("Loss: " + str(loss))
            total_reward = 0

    # If in a menu:
    else:
        melee.MenuHelper.menu_helper_simple(gamestate,
                                            controller,
                                            melee.Character.FOX,
                                            melee.Stage.POKEMON_STADIUM,
                                            connect_code=False,
                                            autostart=True,
                                            swag=True)

        gamestate = console.step()

    if config.log:
        config.log.logframe(gamestate)
        config.log.writeframe()
