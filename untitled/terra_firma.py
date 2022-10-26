import random
from food import Food

class Land:
    def __init__(self, size, terminal, food_likelyhood=0.01):
        self.size = size
        self.width = size[0]
        self.height = size[1]
        self.terminal = terminal

        self.land = self.terraformation(food_likelyhood)
    # end def

    def terraformation(self, food_likelyhood):
        land = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                if random.random() < food_likelyhood:
                    row.append(Food())
                else:
                    row.append(None)
            # end for
            land.append(row)
        # end for

        return land
    # end def

    def __setitem__(self, pos, food):
        self.land[pos.y][pos.x] = food
    # end def

    def __getitem__(self, pos):
        try:
            return self.land[pos.y][pos.x]
        except IndexError:
            print('IndexError: %s' % repr(pos))
    # end def
# end class
