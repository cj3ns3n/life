import numpy as np


class Nutrient:
    def __init__(self):
        self.nutrient_level = np.random.normal(0, 1)
    # end def

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return '(level: %d)' % (self.nutrient_level)
# end class
