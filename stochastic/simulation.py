import random
from pos import Pos

import constants


class Simulation:
    def __init__(self, land, change_queue, stats_container, logger):
        self.land = land
        self.change_queue = change_queue
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

                    self.change_queue.add(cell)
                # end def
            # end for x
        # end for y
    # end def

    def get_new_position(self, pos, preferred_dir):
        vacant_positions = self.land.get_vacant_neighbor_positions(pos)

        if len(vacant_positions) == 1:
            return vacant_positions[0]
        elif len(vacant_positions) > 0:
            if preferred_dir == constants.NORTH:
                north_loc = Pos(pos.x, pos.y - 1)
                if north_loc in vacant_positions:
                    return north_loc
            elif preferred_dir == constants.SOUTH:
                south_loc = Pos(pos.x, pos.y + 1)
                if south_loc in vacant_positions:
                    return south_loc
            elif preferred_dir == constants.WEST:
                west_loc = Pos(pos.x - 1, pos.y)
                if west_loc in vacant_positions:
                    return west_loc
            elif preferred_dir == constants.EAST:
                east_loc = Pos(pos.x + 1, pos.y)
                if east_loc in vacant_positions:
                    return east_loc
            # end if

            return random.choice(vacant_positions)
        # end if

        return None
    # end def
# end class
