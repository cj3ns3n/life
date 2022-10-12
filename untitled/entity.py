import numpy as np
import random
import math

import numpy.random


class Entity:
    FEMALE = 'f'
    MALE = 'm'
    sexes = ['f', 'm']
    health_range = 5
    size_range = 1
    life_expectancy = 100  # number of cycles an entity is expected to live
    initial_health_factor = 20  # less than 20 gives less than 100% birth health.
    mature_age = 25
    mature_age_range = 5
    birthing_death_rate = 0.1
    birthing_min_health = 20
    birthing_health_bonus = 0.1

    def __init__(self, parents=None):
        self.age = 0
        self.sex = random.choice(Entity.sexes)

        self.health = self.get_initial_health(parents)

        if parents is None:
            self.size = max(0.1, np.random.normal(1, Entity.size_range))
            self.mature_age = np.random.normal(Entity.mature_age, Entity.mature_age_range)
        else:
            avg_size = (parents[0].size + parents[1].size) / 2.0
            self.size = np.random.normal(avg_size, Entity.size_range)

            avg_mature_age = (parents[0].mature_age + parents[1].mature_age) / 2.0
            self.mature_age = np.random.normal(avg_mature_age, Entity.mature_age_range)
        # end if
    # end def

    def get_initial_health(self, parents):
        self.health = 100
        if parents is None:
            self.life_expectancy = np.random.normal(Entity.life_expectancy, Entity.health_range)
            self.initial_health_factor = np.random.normal(Entity.initial_health_factor, Entity.health_range-3)
        else:
            avg_expectancy = (parents[0].life_expectancy + parents[1].life_expectancy) / 2.0
            avg_factor = (parents[0].initial_health_factor + parents[1].initial_health_factor) / 2.0
            self.life_expectancy = np.random.normal(avg_expectancy, 0.5)
            self.initial_health_factor = np.random.normal(avg_factor, 0.5)
        # end if

        # end if
        return self.calc_health()
    # end def

    def calc_health(self, neighbors=[]):
        new_health = self.health
        try:
            # y=40 log(-x+100)+20  logarithmic decline to 100
            fated_health = 40 * math.log(-self.age + self.life_expectancy, 10) + self.initial_health_factor
            live_neighbors = list(filter(lambda entity: entity is not None and entity.health > 0, neighbors))
            if len(live_neighbors) > 0:
                local_health = sum(neighbor.health for neighbor in live_neighbors) / len(live_neighbors)
                new_health = (self.health + fated_health + local_health) / 3
            # end if
        except ValueError:
            return 0.0

        return min(100, max(0, new_health))
    # end def

    def calc_eternal_health(self, neighbors):
        if self.health > 0:
            live_neighbors = list(filter(lambda entity: entity.health > 0, neighbors))
            if len(live_neighbors) > 0:
                local_health = (sum(neighbor.health for neighbor in live_neighbors) + self.health) / (len(live_neighbors) + 1)
                local_size = (sum(neighbor.size for neighbor in live_neighbors) + self.size) / (len(live_neighbors) + 1)
            else:
                local_health = self.health
                local_size = self.size
            # end if

            self.health = self.calc_health()
            self.size = max(0.1, np.random.normal(local_size, Entity.size_range))

            if 0 < len(live_neighbors) < len(neighbors):
                return self.procreate(live_neighbors)
        # end if
    # end def

    def procreate(self, neighbors):
        if self.age >= self.mature_age:
            for neighbor in neighbors:
                if neighbor.sex != self.sex and neighbor.age >= neighbor.mature_age:
                    child = Entity((self, neighbor))

                    # adjust femail parent health
                    female_parent = self if self.sex == Entity.FEMALE else neighbor
                    if random.random() < Entity.birthing_death_rate or female_parent.health < Entity.birthing_min_health:
                        female_parent.health = 0.0
                    else:
                        # giving birth increases health; if it doesn't kill the entity
                        female_parent.health = female_parent.health * (1 + numpy.random.normal(Entity.birthing_health_bonus, Entity.birthing_health_bonus/10))
                        female_parent.health = max(0, min(100, female_parent.health))
                    # end if

                    return child
                #end if
            # end for
        # end if

        return None
    # end def

    def progress(self, neighbors=[]):
        self.age += 1
        self.health = self.calc_health(neighbors)

        if self.health > 0:
            if len(neighbors) > 0:
                local_size = (sum(neighbor.size for neighbor in neighbors) + self.size) / (len(neighbors) + 1)
            else:
                local_size = self.size
            # end if
            self.size = max(0.1, np.random.normal(local_size, Entity.size_range))

            if len(neighbors) < 4: # if there is an empty space for a child
                return self.procreate(neighbors)
        # end if

        return None
    # end def

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return '(age: %d, size: %.3f, health: %.1f)' % (self.age, self.size, self.health)
# end class