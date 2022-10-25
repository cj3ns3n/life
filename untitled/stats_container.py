import statistics

from entity import Entity


class StatsContainer:
    def __init__(self):
        self.ages = []
        self.healths = []
        self.sizes = []

        self.age_avg = 0
        self.age_stdev = 0
        self.health_avg = 0
        self.health_stdev = 0
        self.size_avg = 0
        self.size_stdev = 0

        self.cycles = 0
        self.births_count = 0
        self.males_count = 0
        self.female_count = 0
        self.natural_deaths = 0
        self.maternal_deaths = 0
        self.display_iterations = 0

        self.cycle_births = 0
        self.birth_rate = 0.0
        self.cycle_deaths = 0
        self.death_rate = 0.0
    # end init

    def get_stats(self):
        stats = {}

        stats['age_avg'] = self.age_avg
        stats['age_stdev'] = self.age_stdev
        stats['health_avg'] = self.health_avg
        stats['health_stdev'] = self.health_stdev
        stats['size_avg'] = self.size_avg
        stats['size_stdev'] = self.size_stdev
        stats['births'] = self.births_count
        stats['natural_deaths'] = self.natural_deaths
        stats['maternal_deaths'] = self.maternal_deaths
        stats['males'] = self.males_count
        stats['females'] = self.female_count
        stats['cycles'] = self.cycles
        stats['display_iterations'] = self.display_iterations
        stats['death_rate'] = self.death_rate
        stats['birth_rate'] = self.birth_rate

        return stats
    # end def

    def calc_stats(self):
        if len(self.ages) > 1:
            self.age_avg = statistics.mean(self.ages)
            self.age_stdev = statistics.stdev(self.ages)
            self.health_avg = statistics.mean(self.healths)
            self.health_stdev = statistics.stdev(self.healths)
            self.size_avg = statistics.mean(self.sizes)
            self.size_stdev = statistics.stdev(self.sizes)

            # reset stats
            self.ages = []
            self.healths = []
            self.sizes = []

            self.calculating = False
        # end if
    # end def

    def add_entity_stats(self, entity):
        self.ages.append(entity.age)
        self.healths.append(entity.health)
        self.sizes.append(entity.size)
    # end def

    def increment_display_iterations(self):
        self.display_iterations += 1
    # end def

    def increment_cycles(self):
        self.cycles += 1

        population = self.births_count - self.maternal_deaths - self.natural_deaths
        self.birth_rate = float(self.cycle_births) / float(population)
        self.cycle_births = 0

        self.death_rate = float(self.cycle_deaths) / float(population)
        self.cycle_deaths = 0
    # end def

    def increment_births(self, baby):
        self.births_count += 1
        self.cycle_births += 1
        if baby.sex == Entity.MALE:
            self.males_count += 1
        else:
            self.female_count += 1
    # end def

    def increment_natural_deaths(self, entity):
        self.natural_deaths += 1
        self.cycle_deaths == 1
        if entity.sex == Entity.MALE:
            self.males_count -= 1
        else:
            self.female_count -= 1
    # end def

    def increment_maternal_deaths(self):
        self.maternal_deaths += 1
        self.female_count -= 1
        self.cycle_deaths += 1
    # end def
# end class