from melee import enums
import random

def press_random_button(controller):
    random_x = random.uniform(-1, 1)
    random_Y = random.uniform(-1, 1)
    button_list = [None, enums.Button.BUTTON_A]
    random_button = random.randint(0, len(button_list) - 1)
    controller.simple_press(random_x, random_Y, button_list[random_button])