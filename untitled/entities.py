from pos import Pos
from entity import Entity
import random

class Entities:
    def __init__(self, size, logger, life_likelyhood=0.05):
        self.size = size
        self.width = size[0]
        self.height = size[1]
        self.logger = logger
        #self.entities = self.adam_eve(size, Pos(200, 150))
        self.entities = self.birth_entities(size, life_likelyhood)
    # end def

    def adam_eve(self, size, genesis_pos):
        entities = []
        for y in range(size[1]):
            row = []
            for x in range(size[0]):
                if x == genesis_pos.x and y == genesis_pos.y:
                    adam = Entity(-1)
                    adam.sex = 'm'
                    adam.mature_age = 10
                    adam.preferred_direction = 'e'
                    row.append(adam)
                elif x == genesis_pos.x + 1 and y == genesis_pos.y:
                    eve = Entity(-1)
                    eve.sex = 'f'
                    eve.mature_age = 9
                    eve.preferred_direction = 'e'
                    row.append(eve)
                else:
                    row.append(None)
                # end if
            # end for

            entities.append(row)
        # end for

        return entities
    # end def

    def birth_entities(self, size, life_likelyhood):
        entities = []
        for y in range(size[1]):
            row = []
            for x in range(size[0]):
                if random.random() < life_likelyhood:
                    row.append(Entity(-1))
                else:
                    row.append(None)
            # end for
            entities.append(row)
        # end for

        return entities
    # end def

    def __setitem__(self, pos, value):
        self.entities[pos.y][pos.x] = value
    # end def

    def __getitem__(self, pos):
        try:
            return self.entities[pos.y][pos.x]
        except IndexError:
            print('IndexError: %s' % repr(pos))
    # end def

    def get_neighbors(self, pos):
        neighbors = []
        if pos.x > 0:  # left neighbor
            neighbors.append(self[Pos(pos.x-1, pos.y)])
        if pos.x < self.width - 1:  # right neighbor
            neighbors.append(self[Pos(pos.x+1, pos.y)])
        if pos.y > 0:  # top neighbor
            neighbors.append(self[Pos(pos.x, pos.y-1)])
        if pos.y < self.height - 1:  # bottom neighbor
            neighbors.append(self[Pos(pos.x, pos.y+1)])

        if len(neighbors) > 4:
            self.logger.warn('lots o neighbors: %d', len(neighbors), True)
        return list(filter(lambda n: n is not None and n.health > 0.0, neighbors))
    # end def

    def get_vacant_neighbor_positions(self, pos):
        positions = []

        if pos.x > 0: # left neighbor
            left_neighbor = self[Pos(pos.x-1, pos.y)]
            if left_neighbor is None or not left_neighbor.health > 0:
                positions.append(Pos(pos.x-1, pos.y))

        if pos.x < self.size[0] - 1: # right neighbor
            right_neighbor =  self[Pos(pos.x+1, pos.y)]
            if right_neighbor is None or not right_neighbor.health > 0:
                positions.append(Pos(pos.x+1, pos.y))

        if pos.y > 0: # top neighbor
            top_neighbor = self[Pos(pos.x, pos.y-1)]
            if top_neighbor is None or not top_neighbor.health > 0:
                positions.append(Pos(pos.x, pos.y-1))

        if pos.y < self.size[1] - 1: # bottom neighbor
            bottom_neighbor =  self[Pos(pos.x, pos.y+1)]
            if bottom_neighbor is None or not bottom_neighbor.health > 0:
                positions.append(Pos(pos.x, pos.y+1))

        return positions
    # end def
# end class
