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


actionSpace = ActionSpace()

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
        observation_space = Observations(gamestate)
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
