#!/usr/bin/python3
import melee
import action_space
import random
import math
import torch
from console import *
from action_space import ActionSpace
from observation_space import Observations

# if gpu is to be used
use_cuda = torch.cuda.is_available()

device = torch.device("cuda:0" if use_cuda else "cpu")
Tensor = torch.Tensor
LongTensor = torch.LongTensor
random_seed = 42
torch.manual_seed(random_seed)
random.seed(random_seed)

###### PARAMS ######
learning_rate = 0.02
num_episodes = 500
gamma = 1

hidden_layer = 64

replay_mem_size = 50000
batch_size = 32

egreedy = 0.9
egreedy_final = 0
egreedy_decay = 500

report_interval = 10
score_to_solve = 195

####################

actionSpace = ActionSpace()
observation_space = Observations()

def calculate_epsilon(steps_done):
    epsilon = egreedy_final + (egreedy - egreedy_final) * \
              math.exp(-1. * steps_done / egreedy_decay )
    return epsilon

# Main loop
step = 0
while True:
    step += 1
    gamestate = console.step()
    if gamestate is None:
        continue

    # If in game:
    if gamestate.menu_state in [melee.Menu.IN_GAME, melee.Menu.SUDDEN_DEATH]:
        if config.framerecord:
            framedata._record_frame(gamestate)
        #if step % 2 == 0:
            #distance = gamestate.distance
            #print(distance)
            #print(gamestate.player[1].x)
        observation_space.update(gamestate)
        print(observation_space.observations)
        actionSpace.press_random_button(controller)




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

    if config.log:
        config.log.logframe(gamestate)
        config.log.writeframe()
