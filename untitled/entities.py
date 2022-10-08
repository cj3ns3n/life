from pos import Pos
from entity import Entity

class Entities:
    def __init__(self, size):
        self.size = size
        self.width = size[0]
        self.height = size[1]
        self.entities = self.birth_entities(size)
    # end def

    def birth_entities(self, size):
        entities = []
        for y in range(size[1]):
            row = []
            for x in range(size[0]):
                row.append(Entity())
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

        return neighbors
    # end def

    def get_dead_neighbor_pos(self, pos):
        if pos.x > 0 and not self[Pos(pos.x-1, pos.y)].health > 0: # left neighbor
            return Pos(pos.x-1, pos.y)
        if pos.x < self.size[0] - 1 and not self[Pos(pos.x+1, pos.y)].health > 0: # right neighbor
            return Pos(pos.x+1, pos.y)
        if pos.y > 0 and not self[Pos(pos.x, pos.y-1)].health > 0: # top neighbor
            return Pos(pos.x, pos.y-1)
        if pos.y < self.size[1] - 1 and not self[Pos(pos.x, pos.y+1)].health > 0: # bottom neighbor
            return Pos(pos.x, pos.y+1)

        return None
    # end def
# end class
