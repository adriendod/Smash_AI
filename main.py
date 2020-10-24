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

# if gpu is to be used
use_cuda = torch.cuda.is_available()
device = torch.device("cuda:0" if use_cuda else "cpu")
Tensor = torch.Tensor
LongTensor = torch.LongTensor
random_seed = 42
torch.manual_seed(random_seed)
random.seed(random_seed)


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
gamestate = console.step()
while True:
    if gamestate is None:
        continue

    # If in game:
    if gamestate.menu_state in [melee.Menu.IN_GAME, melee.Menu.SUDDEN_DEATH]:

        step += 1
        frames_total += 1

        observation_space = Observations(gamestate)
        state = observation_space.observations

        epsilon = utils.calculate_epsilon(frames_total)
        action = qnet_agent.select_action(state, epsilon)
        print(action)

        actionSpace.press_random_button(controller)

        gamestate = console.step()
        observation_space = Observations(gamestate)
        new_state = observation_space.observations
        reward = 0
        done = 0

        memory.push(state, action, new_state, reward, done)
        qnet_agent.optimize(memory)

        state = new_state






    # If in a menu:
    else:
        melee.MenuHelper.menu_helper_simple(gamestate,
                                            controller,
                                            config.port,
                                            melee.Character.FOX,
                                            melee.Stage.POKEMON_STADIUM,
                                            config.connect_code,
                                            autostart=True,
                                            swag=True)
        gamestate = console.step()

    if config.log:
        config.log.logframe(gamestate)
        config.log.writeframe()
