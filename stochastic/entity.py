import numpy as np
import random

import constants


class Entity:
    def __init__(self):
        self.age = 0
        self.sex = random.choice([constants.MALE, constants.FEMALE])
        self.health = np.random.normal(0.5, 0.2)
        self.size = self.health

        if self.health < 0:
            self.health = 0.1
        if self.health > 1:
            self.health = 1.0
    # end def

    def progress(self):
        if self.health > 0:
            self.health = min(1, self.health + np.random.normal(-0.05, 0.1))
            self.age += 1

        if self.health < 0:
            self.health = 0.1
        if self.health > 1:
            self.health = 1.0

        self.size = self.health
    # end def

    def calc_color(self, use_r=False, use_g=False, use_b=False):
        value = int(255.0 * self.health)
        r = g = b = 0

        if not use_r and not use_g and not use_b:
            r = g = b = value
        else:
            if use_r:
                r = value
            if use_g:
                g = value
            if use_b:
                b = value
        # end if

        if value <= 0:
            r = 200
            g = b = 0

        return (r, g, b)
    # end def

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return '(health: %.1f)' % (self.health)
# end class