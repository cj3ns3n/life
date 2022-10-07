import numpy as np
import random

class Entity:
    health_range = 5
    size_range = 1
    sexes = ['m', 'f']

    def __init__(self, parents = None):
        self.age = 0
        self.sex = random.choice(Entity.sexes)

        if parents is None:
            self.health = min(100, np.random.normal(75, 50))
            self.health = max(10, self.health)

            self.size = max(0.1, np.random.normal(1, Entity.size_range))
        else:
            self.health = np.random.normal(Entity.health_range, Entity.health_range) + (parents[0].health + parents[1].health) / 2.0
            self.health = min(100, self.health)

            self.size = 0.5 * (parents[0].size + parents[1].size) / 2.0
        # end if
    #end def

    def procreate(self, neighbors):
        for neighbor in neighbors:
            if neighbor.sex != self.sex:
                return Entity((self, neighbor))

        return None
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
            # end if

            self.health = min(100, np.random.normal(local_health, Entity.health_range))
            self.health = max(0, self.health)

            self.size = max(0.1, np.random.normal(local_size, Entity.size_range))

            if 0 < len(live_neighbors) < len(neighbors):
                return self.procreate(live_neighbors)
        #end if

        return None
    #end def

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return '(age: %d, size: %.3f, health: %.1f)' % (self.age, self.size, self.health)
#end class