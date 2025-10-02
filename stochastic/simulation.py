import random
from pos import Pos


class Simulation:
    def __init__(self, land, surface, stats_container, logger):
        self.land = land
        self.surface = surface
        self.stats = stats_container
        self.logger = logger
    # end def

    def tick(self):
        # shuffle the processing of rows and columns to avoid bias artifacts
        y_positions = list(range(self.land.height))
        random.shuffle(y_positions)
        for y in y_positions:
            x_positions = list(range(self.land.width))
            random.shuffle(x_positions)
            for x in x_positions:
                pos = Pos(x, y)
                cell = self.land[pos]
                entity = cell.entity
                if entity:
                    entity.progress()
                    if entity.health > 0.0:
                        self.stats.add_entity_stats(entity)
                    else:
                        self.stats.increment_natural_deaths(entity)
                        self.logger.info('natural death: %s; %d' % (repr(pos), self.stats.natural_deaths))
                    # end if

                    new_pos = self.get_new_position(pos)
                    if new_pos:
                        new_cell = self.land[new_pos]
                        new_cell.entity = entity
                        cell.entity = None
                        self.surface[new_pos.x, new_pos.y, :] = entity.calc_color()
                # end def
            # end for x
        # end for y
    # end def

    def get_new_position(self, pos):
        vacant_positions = self.land.get_vacant_neighbor_positions(pos)

        self.logger.info('num vacancies: %d' % len(vacant_positions))
        if len(vacant_positions) == 4:
            return random.choice(vacant_positions)
        elif len(vacant_positions) == 3:
            if random.random() > 0.25:
                return random.choice(vacant_positions)
        elif len(vacant_positions) == 2:
            if random.random() > 0.5:
                return random.choice(vacant_positions)
        elif len(vacant_positions) == 1:
            if random.random() > 0.75:
                return random.choice(vacant_positions)
        # end if

        return None
    # end def
# end class
