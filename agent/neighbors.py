class Neighbors:
  def __init__(self, left_neighbor, right_neighbor, above_neighbor, below_neighbor):
    self.left = left_neighbor
    self.right = right_neighbor
    self.above = above_neighbor
    self.below = below_neighbor
  # end def

  def get(self, direction):
    if direction == direction.LEFT:
      return self.left
    elif direction == direction.RIGHT:
      return self.right
    elif direction == direction.UP:
      return self.up
    elif direction == direction.DOWN:
      return self.down
    else:
      return None
  # end def
# end class
