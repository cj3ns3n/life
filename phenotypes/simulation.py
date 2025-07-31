import random
import numpy

import constants
from pos import Pos
from phenotypes.entity import Entity
from phenotypes.nutrient import Nutrient
from cell import Cell

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
                nutrient = cell.nutrient

                if entity is not None and entity.health > 0:
                    if entity.cycle < self.stats.cycles:
                        neighbor_cells = self.land.get_neighbors_cells(pos)
                        random.shuffle(neighbor_cells)
                        if self.stats.cycles == 0:
                            # add initial entities to births
                            self.stats.increment_births(entity)
                        # end if

                        entity.progress(neighbor_cells, self.stats.cycles)
                        if entity.health > 0.0:
                            self.stats.add_entity_stats(entity)
                            self.post_entity_progress(cell, neighbor_cells)
                        else:
                            self.stats.increment_natural_deaths(entity)
                            self.logger.info('natural death: %s; %d' % (repr(pos), self.stats.natural_deaths))
                        # end if
                    # end if

                    self.change_queue.add(cell)
                # end if

                if nutrient and nutrient.nutrient_level > 0:
                    self.post_nutrient_progress(nutrient, pos)
                    self.stats.add_nutrient_stats(nutrient)
                    self.change_queue.add(cell)
                # end if
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

    def find_mate(self, entity, neighbor_cells):
        best_mate = None

        if entity.age >= entity.mature_age:
            best_dist = 10000
            for neighbor_cell in neighbor_cells:
                neighbor_entity = neighbor_cell.entity
                if neighbor_cell.nutrient_level() > 0 and neighbor_entity and neighbor_entity.sex != entity.sex and neighbor_entity.age >= neighbor_entity.mature_age:
                    if self.incest_check(entity, neighbor_entity):
                        dist = self.entity_dist(entity, neighbor_entity)
                        if dist < best_dist:
                            best_dist = dist
                            best_mate = neighbor_entity
                    # end if
                # end if
            # end for
        # end if

        return best_mate
    # end def

    def manage_health(self, cell):
        entity = cell.entity
        nutrient = cell.nutrient
        pos = cell.pos

        if entity.health < 100:
            needed_nutrients = entity.size

            if nutrient:
                new_level = nutrient.nutrient_level - needed_nutrients
                #self.logger.info('new nutrient level: %0.1f %s %s %s' % (new_level, repr(nutrient), repr(entity), pos))
                if new_level <= 0:
                    self.land[pos].nutrient = None
                    self.stats.remove_nutrient_source()
                else:
                    nutrient.nutrient_level = new_level
            else:
                new_level = -needed_nutrients
            # end if

            if new_level < 0:
                # not enough nutrients
                entity.health = max(0, min(100, entity.health + new_level))
                #self.logger.info('insufficient food: %.1f %s %s' % (new_level, repr(entity), repr(pos)))
                if entity.health <= 0:
                    self.stats.increment_starvations(entity)
                    self.logger.info('starvation: %s; %d' % (repr(pos), self.stats.starvation_deaths))
            # end if
        # end if
    # end def

    def attempt_breeding(self, entity, neighbor_cells, open_pos):
        best_mate = self.find_mate(entity, neighbor_cells)
        child = None

        if best_mate:
            child = Entity(self.stats.cycles, (entity, best_mate))
            self.land[open_pos].entity = child
            self.stats.increment_births(child)

            # adjust female parent health
            female_parent = entity if entity.sex == constants.FEMALE else best_mate
            if random.random() < Entity.birthing_death_rate or female_parent.health < Entity.birthing_min_health:
                self.stats.increment_maternal_deaths()
                female_parent.health = 0.0
            else:
                # giving birth increases health; if it doesn't kill the entity
                female_parent.health = female_parent.health * (1 + numpy.random.normal(Entity.birthing_health_bonus, Entity.birthing_health_bonus/10))
                female_parent.health = max(0, min(100, female_parent.health))
            # end if
        # end if

        return child
    # end def

    def post_entity_progress(self, cell, neighbor_cells):
        pos = cell.pos
        entity = cell.entity
        child = None

        self.manage_health(cell)

        neighbors = list(Cell.extract_entity_cells(neighbor_cells))
        if len(neighbors) < 4 and entity.age >= entity.mature_age:
            new_pos = self.get_new_position(pos, entity.preferred_direction)
            if new_pos:
                if cell.nutrient and cell.nutrient.nutrient_level > 0:
                    child = self.attempt_breeding(entity, neighbor_cells, new_pos)
                    if child:
                        self.change_queue.add(self.land[new_pos])
                elif len(list(Cell.extract_children(neighbor_cells))) == 0:
                    # find new pos
                    self.land[new_pos].entity = entity
                    self.land[pos].entity = None

                    if new_pos.y != pos.y or new_pos.x != pos.x:
                        self.change_queue.add(self.land[new_pos])
                # end if nutrient
            # end if new_pos
        # end if

        return child
    # end def

    def get_random_neighbor(self, pos):
        x = max(0, min(self.land.width - 1, pos.x + random.randint(0, 1)))
        y = max(0, min(self.land.height - 1, pos.y + random.randint(-1, 1)))

        return Pos(x, y)
    # end def

    def spread_nutrients(self, amount, pos):
        try:
            next_pos = self.get_random_neighbor(pos)
            #self.logger.info('spreading nutrients: %f; %s' % (amount, pos))
            nutrients = self.land[next_pos].nutrient
            if nutrients:
                nutrients.nutrient_level = min(100, nutrients.nutrient_level + amount)
            else:
                self.land[next_pos].nutrient = Nutrient(init_nutrients = amount)
                self.stats.increment_nutrient_sources()
        except IndexError:
            self.logger.error('bad food index %s - %s' % (repr(pos), repr(next_pos)), True)

    # end def

    def post_nutrient_progress(self, nutrients, pos):
        nutrients.nutrient_level += nutrients.replenish_rate
        if nutrients.nutrient_level > 100:
            extra_nutrients = nutrients.nutrient_level - 100
            nutrients.nutrient_level = 100
            self.spread_nutrients(extra_nutrients, pos)
    # end def
# end class
