from os import linesep

class Cell:
    ENTITY_KEY = 'entity'
    NUTRIENT_KEY = 'nutrient'

    def __init__(self, pos, entity = None, nutrient = None):
        self.pos = pos
        self.entity = entity
        self.nutrient = nutrient
    # end def

    def nutrient_level(self):
        return 0 if self.nutrient is None else self.nutrient.nutrient_level
    # end def

    def __eq__(self, other):
        return repr(self.pos) == repr(other.pos)
    # end def

    def __hash__(self):
        return hash(repr(self.pos))
    # end def

    @staticmethod
    def extract_entity_cells(cells):
        entity_cells = filter(lambda cell: cell.entity, cells)
        return map(lambda cell: cell.entity, entity_cells)
    # end def

    @staticmethod
    def extract_children(cells):
        return filter(lambda cell: cell.entity and cell.entity.age < cell.entity.mature_age, cells)
    # end def

    def __setitem__(self, key, value):
        if key == Cell.NUTRIENT_KEY:
            self.nutrient = value
        elif key == Cell.ENTITY_KEY:
            self.entity = value
        else:
            raise ValueError
    # end def

    def __getitem__(self, key):
        if key == Cell.NUTRIENT_KEY:
            return self.nutrient
        elif key == Cell.ENTITY_KEY:
            return self.entity
        else:
            raise ValueError
    # end def

    def __str__(self):
        return repr(self)
    # end def

    def __repr__(self):
        return '%s%s%s' % (repr(self.entity), linesep, repr(self.nutrient))
    # end def
# end class