import math
from statistics import mean
#import random
from numpy import random

class Entity:
    health_range = 5
    size_range = 1

    def __init__(self):
        self.age = 0
        self.size = 1
        self.health = 100
    #end def

    def progress(self, neighbors = []):
        self.age += 1

        if self.health > 0:
            live_neighbors = list(filter(lambda entity: entity.health > 0, neighbors))
            if len(live_neighbors) > 0:
                local_health = (sum(neighbor.health for neighbor in live_neighbors) + self.health) / (len(live_neighbors) + 1)
                local_size = (sum(neighbor.size for neighbor in live_neighbors) + self.size) / (len(live_neighbors) + 1)
            else:
                local_health = self.health
                local_size = self.size
            #end if

            # health detrimentally determined by size and age and randomness
            self.health = min(100, random.normal(local_health, Entity.health_range))
            self.health = max(0, self.health)

            self.size = max(0.1, random.normal(local_size, Entity.size_range))
            #end if
    #end def

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return '(age: %d, size: %.3f, health: %.1f)' % (self.age, self.size, self.health)
#end class