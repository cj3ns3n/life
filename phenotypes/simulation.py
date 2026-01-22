import random
import numpy

import constants
from pos import Pos
from phenotypes.entity import Entity
from phenotypes.nutrient import Nutrient
from cell import Cell

class Simulation:
    def __init__(self, land, surface, stats_container, logger):
        self.land = land
        self.surface = surface
        self.stats = stats_container
        self.logger = logger
        
        # Active entity tracking: maps entity -> position
        self.entities = {}
        
        # Initialize with existing entities in the grid
        self._initialize_entity_tracking()
    # end def
    
    def _initialize_entity_tracking(self):
        """Scan the grid once to build the initial active entity list."""
        for y in range(self.land.height):
            for x in range(self.land.width):
                pos = Pos(x, y)
                entity = self.land[pos].entity
                if entity and entity.health > 0:
                    self.entities[entity] = pos
        self.logger.info('Initialized with %d active entities' % len(self.entities))
    # end def
    
    def register_entity(self, entity, pos):
        """Add entity to active tracking."""
        self.entities[entity] = pos
    # end def
    
    def unregister_entity(self, entity):
        """Remove entity from active tracking."""
        if entity in self.entities:
            del self.entities[entity]
    # end def
    
    def move_entity(self, entity, old_pos, new_pos):
        """Update entity position in tracking."""
        if entity in self.entities:
            self.entities[entity] = new_pos
    # end def

    def tick(self):
        # Process only active entities (much more efficient than scanning entire grid)
        entities_list = list(self.entities.items())
        random.shuffle(entities_list)  # Shuffle for fairness
        
        entities_to_remove = []
        
        # Process each active entity
        for entity, pos in entities_list:
            # Verify entity still exists in tracking (might have died from maternal death, etc)
            if entity not in self.entities:
                continue
            
            # Get current cell
            cell = self.land[pos]
            # Enforce rule: entities and nutrients cannot occupy the same cell
            if cell.nutrient is not None:
                cell.nutrient = None
                self.stats.remove_nutrient_source()
            
            # Verify entity is still at this position (should always be true with our tracking)
            if cell.entity != entity:
                self.logger.info('WARNING: Entity position mismatch at %s' % repr(pos))
                entities_to_remove.append(entity)
                continue
            
            # Process entity if not already processed this cycle
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
                    # Natural death
                    self.stats.increment_natural_deaths(entity)
                    self.logger.info('natural death: %s; %d' % (repr(pos), self.stats.natural_deaths))
                    cell.entity = None
                    entities_to_remove.append(entity)
                # end if
            # end if
        # end for
        
        # Remove dead entities from tracking
        for entity in entities_to_remove:
            self.unregister_entity(entity)
        
        # Process nutrients (still need to scan grid for this)
        for y in range(self.land.height):
            for x in range(self.land.width):
                pos = Pos(x, y)
                cell = self.land[pos]
                nutrient = cell.nutrient
                
                if nutrient and nutrient.nutrient_level > 0:
                    self.post_nutrient_progress(nutrient, pos)
                    self.stats.add_nutrient_stats(nutrient)
                # end if
            # end for x
        # end for y
        
        # Final pass: update display for all cells
        for y in range(self.land.height):
            for x in range(self.land.width):
                pos = Pos(x, y)
                cell = self.land[pos]
                self.surface.set_color(pos, self.calc_cell_color(cell))
            # end for
        # end for
        
        # Verify tracking matches calculated population
        expected_pop = self.stats.births_count - self.stats.maternal_deaths - self.stats.natural_deaths - self.stats.starvation_deaths
        if len(self.entities) != expected_pop:
            self.logger.info('TRACKING MISMATCH: tracked=%d, calculated=%d' % (len(self.entities), expected_pop))
    # end def

    def calc_cell_color(self, cell):
        if cell.entity:
            if self.stats.show_aspect_1:
                # Show sex: bright blue for males, pink for females
                if cell.entity.sex == constants.MALE:
                    return (0, 0, 255)
                else:
                    return (255, 105, 180)
            return cell.entity.calc_color(show_health=True)
        elif cell.nutrient:
            if self.stats.show_land:
                green = int(255 * cell.nutrient.nutrient_level / 100.0)
                return (0, green, 0)
            return (0, 0, 0)
        else:
            return (0, 0, 0)
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

    def manage_health(self, cell, neighbor_cells):
        entity = cell.entity
        pos = cell.pos

        if entity.health < 100:
            needed_nutrients = entity.size

            # Entities must be adjacent to nutrients to avoid health loss.
            nutrient_cells = [cell for cell in neighbor_cells if cell.nutrient and cell.nutrient.nutrient_level > 0]
            if nutrient_cells:
                # Consume from the richest neighboring nutrient source
                nutrient_cell = max(nutrient_cells, key=lambda c: c.nutrient.nutrient_level)
                nutrient = nutrient_cell.nutrient
                new_level = nutrient.nutrient_level - needed_nutrients
                #self.logger.info('new nutrient level: %0.1f %s %s %s' % (new_level, repr(nutrient), repr(entity), pos))
                if new_level <= 0:
                    nutrient_cell.nutrient = None
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
                    # Remove dead entity from cell to prevent double-counting
                    cell.entity = None
                    # Unregister from tracking
                    self.unregister_entity(entity)
                    # Update display to show empty cell
                    self.surface.set_color(cell.pos, self.calc_cell_color(cell))
            # end if
        # end if
    # end def

    def find_entity_position(self, target_entity, neighbor_cells):
        """Find which neighbor cell contains the target entity."""
        for cell in neighbor_cells:
            if cell.entity is target_entity:
                return cell.pos
        return None
    # end def

    def find_closest_opposite_sex_pos(self, entity, pos):
        """Find the position of the closest entity of the opposite sex."""
        closest_pos = None
        closest_dist = None
        for other_entity, other_pos in self.entities.items():
            if other_entity is entity or other_entity.sex == entity.sex:
                continue
            dist = abs(other_pos.x - pos.x) + abs(other_pos.y - pos.y)
            if closest_dist is None or dist < closest_dist:
                closest_dist = dist
                closest_pos = other_pos
        return closest_pos
    # end def

    def attempt_breeding(self, entity, entity_pos, neighbor_cells, open_pos):
        best_mate = self.find_mate(entity, neighbor_cells)
        child = None

        if best_mate:
            child = Entity(self.stats.cycles, (entity, best_mate))
            self.land[open_pos].entity = child
            self.stats.increment_births(child)
            # Register new entity in tracking
            self.register_entity(child, open_pos)

            # adjust female parent health
            female_parent = entity if entity.sex == constants.FEMALE else best_mate
            if random.random() < Entity.birthing_death_rate or female_parent.health < Entity.birthing_min_health:
                self.stats.increment_maternal_deaths()
                female_parent.health = 0.0
                # Remove dead mother from cell to prevent double-counting
                female_parent_pos = entity_pos if entity.sex == constants.FEMALE else self.find_entity_position(best_mate, neighbor_cells)
                if female_parent_pos:
                    self.land[female_parent_pos].entity = None
                    # Unregister from tracking
                    self.unregister_entity(female_parent)
                    # Update display to show empty cell
                    self.surface.set_color(female_parent_pos, self.calc_cell_color(self.land[female_parent_pos]))
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

        self.manage_health(cell, neighbor_cells)
        
        # Check if entity died from starvation in manage_health
        if cell.entity is None or entity.health <= 0:
            return None

        neighbors = list(Cell.extract_entity_cells(neighbor_cells))
        if len(neighbors) < 4:
            child = None
            nutrient_neighbors = any(n_cell.nutrient and n_cell.nutrient.nutrient_level > 0 for n_cell in neighbor_cells)
            opposite_adjacent = any(
                n_cell.entity and n_cell.entity.sex != entity.sex for n_cell in neighbor_cells
            )
            child_adjacent = any(
                n_cell.entity and n_cell.entity.age < n_cell.entity.mature_age for n_cell in neighbor_cells
            )

            # Try to breed first if mature and near nutrients
            if nutrient_neighbors and entity.age >= entity.mature_age:
                new_pos = self.get_new_position(pos, entity.preferred_direction)
                if new_pos:
                    child = self.attempt_breeding(entity, pos, neighbor_cells, new_pos)
                    if child:
                        self.surface.set_color(new_pos, self.calc_cell_color(self.land[new_pos]))

            # Decide movement
            should_move = False
            preferred_dir = entity.preferred_direction

            if not opposite_adjacent and not child_adjacent:
                # Move toward closest opposite sex if not adjacent to opposite sex or a child
                target_pos = self.find_closest_opposite_sex_pos(entity, pos)
                if target_pos:
                    dx = target_pos.x - pos.x
                    dy = target_pos.y - pos.y
                    if abs(dx) >= abs(dy):
                        preferred_dir = constants.EAST if dx > 0 else constants.WEST
                    else:
                        preferred_dir = constants.SOUTH if dy > 0 else constants.NORTH
                    should_move = True
            else:
                # Stay unless not next to food
                if not nutrient_neighbors:
                    should_move = True

            if child is None and should_move and len(list(Cell.extract_children(neighbor_cells))) == 0:
                # Keep juveniles near parents if possible
                if entity.age < entity.mature_age:
                    parents = set(entity.parents)
                    if parents:
                        parent_adjacent = any(
                            n_cell.entity in parents for n_cell in neighbor_cells if n_cell.entity is not None
                        )
                        if parent_adjacent:
                            return None
                # end if
                new_pos = self.get_new_position(pos, preferred_dir)
                if new_pos:
                    # find new pos
                    self.land[new_pos].entity = entity
                    self.land[pos].entity = None
                    # moving onto nutrients clears them
                    if self.land[new_pos].nutrient is not None:
                        self.land[new_pos].nutrient = None
                        self.stats.remove_nutrient_source()
                    # Update tracking
                    self.move_entity(entity, pos, new_pos)

                    if new_pos.y != pos.y or new_pos.x != pos.x:
                        # Update new position with entity
                        self.surface.set_color(new_pos, entity.calc_color())
                        # Update old position to show it's empty (or show nutrients)
                        self.surface.set_color(pos, self.calc_cell_color(self.land[pos]))
            # end if
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
                # only place nutrients in empty cells
                if self.land[next_pos].entity is None:
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
