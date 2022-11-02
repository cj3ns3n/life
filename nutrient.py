class Nutrient:
    def __init__(self, init_nutrients = 100.0, replenish_rate = 0.1):
        self.nutrient_level = init_nutrients
        self.replenish_rate = replenish_rate
    # end def

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return '(level: %d, rate: %.1f)' % (self.nutrient_level, self.replenish_rate)
# end class
