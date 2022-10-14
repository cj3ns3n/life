import threading
import statistics
import random
from pos import Pos
from entity import Entity


class EntityEngine(threading.Thread):
    def __init__(self, entities):
        threading.Thread.__init__(self)

        self.entities = entities

        self.processed_rows = []

        # stats
        self.cycles = 0
        self.births = 0
        self.deaths = 0
        self.age_avg = 0
        self.age_stdv = 0
        self.health_avg = 0
        self.health_stdv = 0
        self.size_avg = 0
        self.size_stdv = 0
    # end def

    def get_processed_rows(self):
        rows = self.processed_rows.copy()
        self.processed_rows = []
        return rows
    # end def

    def get_vacant_position(self, pos, preferred_dir):
        vacant_positions = self.entities.get_vacant_neighbor_positions(pos)
        if len(vacant_positions) > 0:
            if preferred_dir == Entity.NORTH:
                north_loc = Pos(pos.x, pos.y - 1)
                if north_loc in vacant_positions:
                    return north_loc
            elif preferred_dir == Entity.SOUTH:
                south_loc = Pos(pos.x, pos.y + 1)
                if south_loc in vacant_positions:
                    return south_loc
            elif preferred_dir == Entity.WEST:
                west_loc = Pos(pos.x - 1, pos.y)
                if west_loc in vacant_positions:
                    return west_loc
            elif preferred_dir == Entity.EAST:
                east_loc = Pos(pos.x + 1, pos.y)
                if east_loc in vacant_positions:
                    return east_loc
            else:
                return random.choice(vacant_positions)
        else:
            return None
    # end def

    def run(self):
        self.cycles = 0
        while True:
            #print('progressing', count)
            ages = []
            healths = []
            sizes = []
            stats_thread = None

            # shuffle the processing of rows and columns to avoid bias artifacts
            y_positions = list(range(self.entities.height))
            random.shuffle(y_positions)
            for y in y_positions:
                x_positions = list(range(self.entities.width))
                random.shuffle(x_positions)
                for x in x_positions:
                    pos = Pos(x, y)
                    neighbors = self.entities.get_neighbors(pos)
                    random.shuffle(neighbors)
                    entity = self.entities[pos]
                    if entity is not None and entity.health > 0:
                        child = entity.progress(neighbors)
                        #if x == 0 and y == 0:
                        #    print((entity.age, entity.health, entity.initial_health_factor, entity.life_expectancy))
                        if entity.health > 0:
                            ages.append(entity.age)
                            healths.append(entity.health)
                            sizes.append(entity.size)
                        else:
                            self.deaths += 1
                        # end def

                        # check if any neighbors died
                        if len(list(filter(lambda neighbor: not neighbor.health > 0, neighbors))):
                            #print('neighbor died')
                            self.deaths += 1

                        if child:
                            new_pos = self.get_vacant_position(pos, entity.preferred_direction)
                            if new_pos:
                                self.births += 1
                                self.entities[new_pos] = child
                        elif entity.age > entity.mature_age and entity.health > 50:
                            new_pos = self.get_vacant_position(pos, entity.preferred_direction)
                            if new_pos:
                                self.entities[new_pos] = entity
                                self.entities[pos] = None
                        # end if
                    # end if
                # end for x
                self.processed_rows.append(y)
            # end for y

            self.cycles += 1

            if stats_thread is None or not stats_thread.is_alive():
                stats_thread = threading.Thread(target=self.calc_stats, args=(ages, healths, sizes))
                stats_thread.start ()
                stats_thread.join ()
        # end while
    # end def

    def calc_stats(self, ages, healths, sizes):
        self.age_avg = statistics.mean(ages)
        self.age_stdv = statistics.stdev(ages)
        self.health_avg = statistics.mean(healths)
        self.health_stdv = statistics.stdev(healths)
        self.size_avg = statistics.mean(sizes)
        self.size_stdv = statistics.stdev(sizes)
    # end def

# end class