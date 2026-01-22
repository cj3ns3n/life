import random

from cell import Cell
from phenotypes.entity import Entity
from phenotypes.nutrient import Nutrient
from pos import Pos

class Land:
    def __init__(self, size, logger, life_likelyhood=0.1, nutrient_likelyhood=0.1):
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
                entity = self.create_entity(life_likelyhood)
                nutrient = None if entity else self.create_nutrient(food_likelyhood)
                cell = Cell(Pos(x, y), entity, nutrient)
                row.append(cell)
            # end for
            land.append(row)
        # end for

        return land
    # end def

    def get_neighbors_cells(self, pos):
        neighbors = []
        if pos.x > 0:  # left neighbor
            neighbors.append(self[Pos(pos.x-1, pos.y)])
        if pos.x < self.width - 1:  # right neighbor
            neighbors.append(self[Pos(pos.x+1, pos.y)])
        if pos.y > 0:  # top neighbor
            neighbors.append(self[Pos(pos.x, pos.y-1)])
        if pos.y < self.height - 1:  # bottom neighbor
            neighbors.append(self[Pos(pos.x, pos.y+1)])

        return neighbors
    # end def

    def get_vacant_neighbor_positions(self, pos):
        positions = []

        if pos.x > 0: # left neighbor
            left_pos = Pos(pos.x-1, pos.y)
            left_neighbor = self.get_entity(left_pos)
            if (left_neighbor is None or not left_neighbor.health > 0):
                positions.append(Pos(pos.x-1, pos.y))

        if pos.x < self.size[0] - 1: # right neighbor
            right_pos = Pos(pos.x+1, pos.y)
            right_neighbor =  self.get_entity(right_pos)
            if (right_neighbor is None or not right_neighbor.health > 0):
                positions.append(Pos(pos.x+1, pos.y))

        if pos.y > 0: # top neighbor
            top_pos = Pos(pos.x, pos.y-1)
            top_neighbor = self.get_entity(top_pos)
            if (top_neighbor is None or not top_neighbor.health > 0):
                positions.append(Pos(pos.x, pos.y-1))

        if pos.y < self.size[1] - 1: # bottom neighbor
            bottom_pos = Pos(pos.x, pos.y+1)
            bottom_neighbor =  self.get_entity(bottom_pos)
            if (bottom_neighbor is None or not bottom_neighbor.health > 0):
                positions.append(Pos(pos.x, pos.y+1))

        return positions
    # end def

    def get_nutrient(self, pos):
        return self[pos][Cell.NUTRIENT_KEY]

    def add_nutrient(self, pos, nutrient):
        # do not place nutrients where an entity exists
        if self.land[pos.y][pos.x][Cell.ENTITY_KEY] is None:
            self.land[pos.y][pos.x][Cell.NUTRIENT_KEY] = nutrient

    def get_entity(self, pos):
        return self[pos][Cell.ENTITY_KEY]

    def add_entity(self, pos, entity):
        self.land[pos.y][pos.x][Cell.ENTITY_KEY] = entity
        # entities and nutrients cannot occupy the same cell
        self.land[pos.y][pos.x][Cell.NUTRIENT_KEY] = None

    def __setitem__(self, pos, value):
        if type(value) is Cell:
            self.land[pos.y][pos.x] = value
        if type(value) is Entity:
            self.land[pos.y][pos.x][Cell.ENTITY_KEY] = value
            # entities and nutrients cannot occupy the same cell
            self.land[pos.y][pos.x][Cell.NUTRIENT_KEY] = None
        elif type(value) is Nutrient:
            if self.land[pos.y][pos.x][Cell.ENTITY_KEY] is None:
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
