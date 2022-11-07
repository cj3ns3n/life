import random

from cell import Cell
from entity import Entity
from nutrient import Nutrient
from pos import Pos

class Land:
    def __init__(self, size, logger, life_likelyhood=0.05, nutrient_likelyhood=0.01):
        self.size = size
        self.width = size[0]
        self.height = size[1]
        self.logger = logger

        self.land = self.terraformation(life_likelyhood, nutrient_likelyhood)
    # end def

    def create_nutrient(self, nutrient_likelyhood):
        if random.random() < nutrient_likelyhood:
            return Nutrient()
        else:
            return None
    # end def

    def create_entity(self, life_likelyhood):
        if random.random() < life_likelyhood:
            return Entity(-1)
        else:
            return None
    # end def

    def terraformation(self, life_likelyhood, food_likelyhood):
        land = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                cell = Cell(self.create_entity(life_likelyhood), self.create_nutrient(food_likelyhood))
                row.append(cell)
            # end for
            land.append(row)
        # end for

        return land
    # end def

    def get_neighbors(self, pos):
        neighbors = []
        if pos.x > 0:  # left neighbor
            neighbors.append(self[Pos(pos.x-1, pos.y)].entity)
        if pos.x < self.width - 1:  # right neighbor
            neighbors.append(self[Pos(pos.x+1, pos.y)].entity)
        if pos.y > 0:  # top neighbor
            neighbors.append(self[Pos(pos.x, pos.y-1)].entity)
        if pos.y < self.height - 1:  # bottom neighbor
            neighbors.append(self[Pos(pos.x, pos.y+1)].entity)

        if len(neighbors) > 4:
            self.logger.warn('lots o neighbors: %d', len(neighbors), True)

        return list(filter(lambda n: n is not None and n.health > 0.0, neighbors))
    # end def

    def get_vacant_neighbor_positions(self, pos):
        positions = []

        if pos.x > 0: # left neighbor
            left_neighbor = self.get_entity(Pos(pos.x-1, pos.y))
            if left_neighbor is None or not left_neighbor.health > 0:
                positions.append(Pos(pos.x-1, pos.y))

        if pos.x < self.size[0] - 1: # right neighbor
            right_neighbor =  self.get_entity(Pos(pos.x+1, pos.y))
            if right_neighbor is None or not right_neighbor.health > 0:
                positions.append(Pos(pos.x+1, pos.y))

        if pos.y > 0: # top neighbor
            top_neighbor = self.get_entity(Pos(pos.x, pos.y-1))
            if top_neighbor is None or not top_neighbor.health > 0:
                positions.append(Pos(pos.x, pos.y-1))

        if pos.y < self.size[1] - 1: # bottom neighbor
            bottom_neighbor =  self.get_entity(Pos(pos.x, pos.y+1))
            if bottom_neighbor is None or not bottom_neighbor.health > 0:
                positions.append(Pos(pos.x, pos.y+1))

        return positions
    # end def

    def get_nutrient(self, pos):
        return self[pos][Cell.NUTRIENT_KEY]

    def add_nutrient(self, pos, nutrient):
        self.land[pos.y][pos.x][Cell.NUTRIENT_KEY] = nutrient

    def get_entity(self, pos):
        return self[pos][Cell.ENTITY_KEY]

    def add_entity(self, pos, entity):
        self.land[pos.y][pos.x][Cell.ENTITY_KEY] = entity

    def __setitem__(self, pos, value):
        if type(value) is Cell:
            self.land[pos.y][pos.x] = value
        if type(value) is Entity:
            self.land[pos.y][pos.x][Cell.ENTITY_KEY] = value
        elif type(value) is Nutrient:
            self.land[pos.y][pos.x][Cell.NUTRIENT_KEY] = value
        else:
            raise TypeError
    # end def

    def __getitem__(self, pos):
        try:
            return self.land[pos.y][pos.x]
        except IndexError:
            print('IndexError: %s' % repr(pos))
    # end def
# end class
