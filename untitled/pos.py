class Pos:
    def __init__(self, x=-1, y=-1, pos=None, tuple=None):
        if tuple is not None:
            self.x = tuple[0]
            self.y = tuple[1]
        elif pos is not None:
            self.x = pos.x
            self.y = pos.y
        else:
            self.x = x
            self.y = y
    # end def

    def __eq__(self, otherObj):
        if isinstance(otherObj, Pos):
            return self.x == otherObj.x and self.y == otherObj.y
        else:
            raise ValueError
    # end def

    def __ne__(self, otherObj):
        return not self == otherObj
    # end def

    def __repr__(self):
        return '(%d, %d)' % (self.x, self.y)

    def __str__(self):
        return repr(self)
# end class

if __name__ == '__main__':
    p0 = Pos(0, 0)
    p00 = Pos(pos=p0)
    p1 = Pos(tuple=(1, 1))

    print(p0 == p0)  # true
    print(p0 == p00) # true
    print(p0 == p1)  # false
    print(p00 == p1) # false

    print(p0 != p0)  # false
    print(p0 != p00) # false
    print(p0 != p1)  # true
# end if
