import math
from statistics import mean
import random

class Entity:
    def __init__(self):
        self.age = 0
        self.size = 1
        self.health = 100
    #end def

    def progress(self):
        self.age += 1

        # health detrimentally determined by size and age and randomness
        variance = self.health * random.uniform(-0.01, 0.1)
        age_factor = math.log(self.age)
        size_factor = math.log(int(self.size)+1)
        health_factor = math.log(max(int(mean([age_factor, size_factor])), 1))
        #print('health info: (%s, %s, %s, %s)' % (variance, age_factor, size_factor, health_factor))
        self.health = min(self.health + variance - health_factor, 100)
        self.health = max(10, self.health)

        # size determined by health and age
        variance = self.health * random.uniform(-0.001, 0.001)
        self.size = math.log(self.age) + variance
        self.size = min(100, self.size)
    #end def

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return 'entity: (%s, %s, %s)' % (self.age, self.size, self.health)
#end class