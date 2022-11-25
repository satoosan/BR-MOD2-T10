import random

from dino_runner.utils.constants import SHIELD, SHIELD_TYPE, HAMMER, HAMMER_TYPE, GODZILLA_TYPE, NUCLEAR
from dino_runner.components.power_ups.power_up import PowerUp


POWER_UP = [(SHIELD, SHIELD_TYPE), (HAMMER, HAMMER_TYPE), (NUCLEAR, GODZILLA_TYPE)]


class Skill(PowerUp):
    def __init__(self):
        self.image, self.type  = POWER_UP[random.randint(0, 2)]
        super().__init__(self.image, self.type)