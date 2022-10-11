import threading
import statistics
from pos import Pos

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

    def run(self) :
        self.cycles = 0
        while True:
            #print('progressing', count)
            ages = []
            healths = []
            sizes = []
            stats_thread = None

            for y in range(self.entities.height):
                for x in range(self.entities.width):
                    pos = Pos(x, y)
                    neighbors = self.entities.get_neighbors(pos)
                    entity = self.entities[pos]
                    if entity is not None and entity.health > 0:
                        child = entity.progress(neighbors)
                        #if x == 0 and y == 0:
                        #    print((entity.age, entity.health, entity.initial_health_factor, entity.life_expectancy))
                        if not entity.health > 0:
                            self.deaths += 1
                        else:
                            ages.append(entity.age)
                            healths.append(entity.health)
                            sizes.append(entity.size)
                        # end def

                        if child:
                            new_pos = self.entities.get_vacant_neighbor_pos(pos)
                            if new_pos:
                                self.births += 1
                                #print('dead: %s' % (str(self.entities[new_pos[1]][new_pos[0]])))
                                self.entities[new_pos] = child
                            # end if
                        # end if
                    # end if
                # end for x
                self.processed_rows.append(y)
            # end for y

            self.cycles += 1

            if stats_thread is None or not stats_thread.is_alive():
                print('stats thread')
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