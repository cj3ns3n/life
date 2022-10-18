class Pos:
    def __init__(self, x=-1, y=-1, pos=None, tuple_pos=None):
        if tuple_pos is not None:
            self.x = tuple_pos[0]
            self.y = tuple_pos[1]
        elif pos is not None:
            self.x = pos.x
            self.y = pos.y
        else:
            self.x = x
            self.y = y
    # end def

    def __eq__(self, other_obj):
        if isinstance(other_obj, Pos):
            return self.x == other_obj.x and self.y == other_obj.y
        else:
            raise ValueError
    # end def

    def __ne__(self, other_obj):
        return not self == other_obj
    # end def

    def __repr__(self):
        return '(%d, %d)' % (self.x, self.y)

    def __str__(self):
        return repr(self)
# end class

if __name__ == '__main__':
    p0 = Pos(0, 0)
    p00 = Pos(pos=p0)
    p1 = Pos(tuple_pos=(1, 1))

    print(p0 == p0)  # true
    print(p0 == p00) # true
    print(p0 == p1)  # false
    print(p00 == p1) # false

    print(p0 != p0)  # false
    print(p0 != p00) # false
    print(p0 != p1)  # true
# end if
