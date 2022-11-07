from os import linesep

class Cell:
    ENTITY_KEY = 'entity'
    NUTRIENT_KEY = 'nutrient'

    def __init__(self, entity = None, nutrient = None):
        self.entity = entity
        self.nutrient = nutrient
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
# end class