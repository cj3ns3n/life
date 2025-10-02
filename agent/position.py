import direction

class Position:
  def __init__(self, x, y, max_x = 100, max_y = 100):
    self.x = x
    self.y = y
    self.max_x = max_x
    self.max_y = max_y
    if max_x > 20:
      raise ValueError('x err')
    if max_y > 20:
      raise ValueError('y err')
# end def

  def left(self):
    x = self.x - 1 if self.x - 1 >= 0 else self.x
    return Position(x, self.y, self.max_x, self.max_y)
  # end def

  def right(self):
    x = self.x + 1 if self.x + 1 < self.max_x else self.x
    return Position(x, self.y, self.max_x, self.max_y)
  # end def

  def down(self):
    y = self.y + 1 if self.y + 1 < self.max_y else self.y
    return Position(self.x, y, self.max_x, self.max_y)
  # end def

  def up(self):
    y = self.y - 1 if self.y - 1 >= 0 else self.y
    return Position(self.x, y, self.max_x, self.max_y)
  # end def

  def get(self, dir):
    if dir == direction.LEFT:
      return self.left()
    elif dir == direction.RIGHT:
      return self.right()
    elif dir == direction.UP:
      return self.up()
    elif dir == direction.DOWN:
      return self.down()
  # end def

  def __str__(self):
    return '({}, {})'.format(self.x, self.y)
# end class
