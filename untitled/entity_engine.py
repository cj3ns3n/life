import threading
import random
import numpy
from pos import Pos
from entity import Entity

class EntityEngine(threading.Thread):
    def __init__(self, entities, stats_container, terminal):
        threading.Thread.__init__(self)

        self.entities = entities
        self.processed_rows = set()
        self.stats = stats_container
        self.terminal = terminal
    # end def

    def get_processed_rows(self):
        rows = self.processed_rows.copy()
        self.processed_rows = set()
        return rows
    # end def

    def get_vacant_position(self, pos, preferred_dir):
        vacant_positions = self.entities.get_vacant_neighbor_positions(pos)
        if len(vacant_positions) == 1:
            return vacant_positions[0]
        elif len(vacant_positions) > 0:
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
            # end if

            return random.choice(vacant_positions)
        # end if

        return None
    # end def

    def entity_dist(self, entity1, entity2):
        square_sums = (entity1.phenotype[0] - entity2.phenotype[0])**2
        square_sums += (entity1.phenotype[1] - entity2.phenotype[1])**2
        square_sums += (entity1.phenotype[2] - entity2.phenotype[2])**2
        square_sums += (entity1.age - entity2.age)**2

        return square_sums**0.5
    # end def

    def incest_check(self, entity1, entity2):
        ancestry = entity1.parents + entity1.grandparents + entity2.parents + entity2.grandparents
        if entity1 in ancestry or entity2 in ancestry:
            # shared parents or grandparents
            return False
        if any(x in entity1.parents + entity1.grandparents for x in entity2.parents + entity2.grandparents):
            # siblings or aunt/uncle
            return False

        return True
    # end def

    def find_mate(self, entity, neighbors):
        best_mate = None

        if entity.age >= entity.mature_age:
            best_dist = 10000
            for neighbor in neighbors:
                if neighbor.sex != entity.sex and neighbor.age >= neighbor.mature_age:
                    if self.incest_check(entity, neighbor):
                        dist = self.entity_dist(entity, neighbor)
                        if dist < best_dist:
                            best_dist = dist
                            best_mate = neighbor
                    # end if
                # end if
            # end for
        # end if

        return best_mate
    # end def

    def child_exists(self, neighbors):
        return len(list(filter(lambda entity: entity.age < entity.mature_age, neighbors))) > 0
    # end def

    def post_entity_progress(self, pos, entity, neighbors):
        if len(neighbors) < 4 and entity.age >= entity.mature_age:
            new_pos = self.get_vacant_position(pos, entity.preferred_direction)
            if new_pos:
                best_mate = self.find_mate(entity, neighbors)
                if len(neighbors) > 4:
                    self.terminal.add_message('pos: %s, entity: %s, mate: %s, %d' % (repr(pos), repr(entity), repr(best_mate), len(neighbors)))

                if best_mate:
                    child = Entity(self.stats.cycles, (entity, best_mate))
                    self.entities[new_pos] = child
                    self.stats.increment_births(child)
                    #self.terminal.add_message('birth %s; %d; %d' % (repr(pos), child.mature_age, self.stats.births_count))

                    # adjust female parent health
                    female_parent = entity if entity.sex == Entity.FEMALE else best_mate
                    if random.random() < Entity.birthing_death_rate or female_parent.health < Entity.birthing_min_health:
                        self.stats.increment_maternal_deaths()
                        female_parent.health = 0.0
                    else:
                        # giving birth increases health; if it doesn't kill the entity
                        female_parent.health = female_parent.health * (1 + numpy.random.normal(Entity.birthing_health_bonus, Entity.birthing_health_bonus/10))
                        female_parent.health = max(0, min(100, female_parent.health))
                    # end if

                    return child
                elif not self.child_exists(neighbors):
                    # find new pos
                    self.entities[new_pos] = entity
                    self.entities[pos] = None

                    if new_pos.y != pos.y:
                        self.processed_rows.add(new_pos.y)
                # end if
            # end if
        # end if
    # end def

    def run(self):
        while True:
            stats_thread = None

            # shuffle the processing of rows and columns to avoid bias artifacts
            y_positions = list(range(self.entities.height))
            random.shuffle(y_positions)
            for y in y_positions:
                x_positions = list(range(self.entities.width))
                random.shuffle(x_positions)
                for x in x_positions:
                    pos = Pos(x, y)
                    entity = self.entities[pos]
                    if entity is not None and entity.health > 0:
                        if entity.cycle < self.stats.cycles:
                            neighbors = self.entities.get_neighbors(pos)
                            random.shuffle(neighbors)
                            if self.stats.cycles == 0:
                                # add initial entities to births
                                self.stats.increment_births(entity)
                                #self.terminal.add_message('birth: %s; %d' % (repr(pos), self.stats.births_count))
                            # end if

                            entity.progress(neighbors, self.stats.cycles)
                            if entity.health > 0.0:
                                self.stats.add_entity_stats(entity)
                                self.post_entity_progress(pos, entity, neighbors)
                            else:
                                self.stats.increment_natural_deaths(entity)
                                #self.terminal.add_message('natural death: %s; %d' % (repr(pos), self.stats.natural_deaths))
                            # end if
                        # end if
                    # end if
                # end for x

                self.processed_rows.add(y)
            # end for y

            self.stats.increment_cycles()

            if stats_thread is None or not stats_thread.is_alive():
                stats_thread = threading.Thread(target=self.stats.calc_stats)
                stats_thread.start()
                stats_thread.join()  # forced to join until locking to implemented
        # end while
    # end def
# end class