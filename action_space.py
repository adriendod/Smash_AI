from melee import enums
import numpy as np
import random


def combine_actions(button, x, y):
    action = [button, x, y]
    return action


class ActionSpace:

    def __init__(self):
        self.no_button = None
        self.normal = enums.Button.BUTTON_A
        self.special = enums.Button.BUTTON_B
        self.shield = enums.Button.BUTTON_L
        self.jump = enums.Button.BUTTON_X
        self.grab = enums.Button.BUTTON_Z
        self.stick_positions = np.arange(-1, 2, 1)
        self.button_list = [self.no_button, self.normal, self.special, self.shield, self.jump, self.grab]
        self.actions = []

        # Create action list
        for button in self.button_list:
            for x in self.stick_positions:
                for y in self.stick_positions:
                    self.actions.append(combine_actions(button, x, y))

    def press_button(self, controller, action_index):
        action = self.actions[action_index]
        controller.simple_press(action[1], action[2], action[0])

    def press_random_button(self, controller):
        random_button = random.randint(0, len(self.actions) - 1)
        self.press_button(controller, self.actions[random_button])

    def get_random_action(self):
        rand_int = random.randint(0, len(self.actions) - 1)
        return rand_int
