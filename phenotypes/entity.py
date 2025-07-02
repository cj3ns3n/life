import numpy as np
import random
import math
from cell import Cell


class Entity:
    FEMALE = 'f'
    MALE   = 'm'

    NORTH  = 'n'
    SOUTH  = 's'
    EAST   = 'e'
    WEST   = 'w'

    health_range = 5
    size_range = 1
    phenotype_range = 1
    life_expectancy = 100  # number of cycles an entity is expected to live
    initial_health_factor = 20  # less than 20 gives less than 100% birth health.
    mature_age = 25
    mature_age_range = 5
    birthing_death_rate = 0.1
    birthing_min_health = 20
    birthing_health_bonus = 0.1

    max_age = 150
    min_size = 1
    max_health = 100
    min_health = 75


    def __init__(self, cycle, parents=None):
        self.age = 0
        self.cycle = cycle
        self.sex = random.choice([Entity.MALE, Entity.FEMALE])
        self.preferred_direction = random.choice([Entity.NORTH, Entity.SOUTH, Entity.EAST, Entity.WEST])

        self.health = self.get_initial_health(parents)

        if parents is None:
            self.parents = ()
            self.grandparents = ()

            self.size = max(0.1, np.random.normal(1, Entity.size_range))
            self.mature_age = np.random.normal(Entity.mature_age, Entity.mature_age_range)
            self.phenotype = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        else:
            self.parents = parents
            self.grandparents = parents[0].parents + parents[1].parents

            avg_size = (parents[0].size + parents[1].size) / 2.0
            self.size = max(0.1, np.random.normal(avg_size, Entity.size_range))

            # avg phenotype values
            a = (parents[0].phenotype[0] + parents[1].phenotype[0]) / 2.0
            a = np.random.normal(a, Entity.phenotype_range)
            b = (parents[0].phenotype[1] + parents[1].phenotype[1]) / 2.0
            b = np.random.normal(b, Entity.phenotype_range)
            c = (parents[0].phenotype[2] + parents[1].phenotype[2]) / 2.0
            c = np.random.normal(c, Entity.phenotype_range)
            self.phenotype = (min(255, max(0, a)), min(255, max(0, b)), min(255, max(0, c)))

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

        return self.calc_health()
    # end def

    def calc_health(self, neighbor_cells=[]):
        neighbors = Cell.extract_entity_cells(neighbor_cells)
        new_health = self.health

        try:
            # y=40 log(-x+100)+20  logarithmic decline to 100
            fated_health = 40 * math.log(-self.age + self.life_expectancy, 10) + self.initial_health_factor
            live_neighbors = list(filter(lambda neighbor: neighbor is not None and neighbor.health > 0, neighbors))
            if len(live_neighbors) > 0:
                local_health = sum(neighbor.health for neighbor in live_neighbors) / len(live_neighbors)
                new_health = (self.health + fated_health + local_health) / 3
            # end if
        except ValueError:
            return 0.0

        return min(100, max(0, new_health))
    # end def

    def calc_color(self, show_age=False, show_health=False, show_sex=False):
        r = g = b = 0

        if not show_age and not show_health and not show_sex:
            r = self.phenotype[0]
            g = self.phenotype[1]
            b = self.phenotype[2]
        else:
            if show_age:
                if self.age > Entity.max_age:
                    r = 255
                else:
                    r = int(255.0 * 1.0 - (self.age / Entity.max_age))

            if show_health:
                if self.health < Entity.min_health:
                    g = 0
                else:
                    g = int(255.0 * (self.health - self.min_health) / (self.max_health - self.min_health))

            if show_sex:
                if self.sex == Entity.MALE:
                    b = 255
                else:
                    r = 255

                if self.age < self.mature_age:
                    g = 255
            # end if

            if r < 0 or r > 255 or g < 0 or g > 255 or b < 0 or b > 255:
                self.logger.error('bad color: %s: %s' % (str((r, g, b)), str(self)), True)
        # end if

        return (r, g, b)
    # end def

    def progress(self, neighbor_cells, cycle):
        self.cycle = cycle
        self.age += 1
        self.health = self.calc_health(neighbor_cells)
        if self.health > 50:
            # randomly grow or shrink
            self.size = max(0.1, np.random.normal(self.size, self.size/10.0))
        else:
            # shrink for ill health
            self.size = min(self.size, np.random.normal(self.size * 0.1, self.size/10.0))

        if self.size <= 0:
            self.health = 0
    # end def

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return '(age: %d, size: %.3f, health: %.1f)' % (self.age, self.size, self.health)
# end class