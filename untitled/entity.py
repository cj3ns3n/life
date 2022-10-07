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
            #if len(live_neighbors) > 0:
            if False:
                avg_size = (sum(neighbor.size for neighbor in live_neighbors) + self.size) / (len(live_neighbors) + 1)
                avg_health = (sum(neighbor.health for neighbor in live_neighbors) + self.health) / (len(live_neighbors) + 1)

                self.size = avg_size
                self.health = avg_health

                if self.health > 100:
                    print('too healthy: %s, %f, %f %d' % (str(self), avg_size, avg_health, len(live_neighbors)))
                    for neighbor in live_neighbors:
                        print('\t%s' % str(neighbor))
            else:
                # health detrimentally determined by size and age and randomness
                self.health = min(100, random.normal(self.health, Entity.health_range))
                self.health = max(0, self.health)

                self.size = max(0.1, random.normal(self.size, Entity.size_range))
            #end if
    #end def

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return '(age: %d, size: %.3f, health: %.1f)' % (self.age, self.size, self.health)
#end class