import logging

from random import random
from entity import Entity
from neighbors import Neighbors


class World:
  def __init__(self, width = 20, height = 20):
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s - %(name)s', level=logging.INFO)
    self.logger = logging.getLogger('World')

    self.width = width
    self.height = height

    self.entity_count = 0
    self.land = self.create()

    self.logger.info('world create size {}x{}; {} entities'.format(self.width, self.height, self.entity_count))
  # end def

  def create(self):
    land = []
    for y in range(self.height):
      row = []
      for x in range(self.width):
        #cell = Cell(Pos(x, y), self.create_entity(life_likelyhood), self.create_nutrient(food_likelyhood))
        if random() < 0.05:
          row.append(Entity())
          self.entity_count += 1
        else:
          row.append(None)
      # end for
      land.append(row)
    # end for

    return land
  # end def

  def get_entity(self, pos):
    try:
      return self.land[pos.y][pos.x]
    except IndexError as ex:
      self.logger.error('Index out of range {}'.format(str(pos)))
      raise ex
  # end def

  def get_neighbors(self, pos):
    left_neighbor = None
    right_neighbor = None
    above_neighbor = None
    below_neighbor = None

    left_pos = pos.left()
    if left_pos.x != pos.x:
      left_neighbor = self.get_entity(left_pos)

    right_pos = pos.right()
    if right_pos.x != pos.x:
      right_neighbor = self.get_entity(right_pos)

    up_pos = pos.up()
    if up_pos.y != pos.y:
      above_neighbor = self.get_entity(up_pos)

    below_pos = pos.down()
    if below_pos.y != pos.y:
      below_neighbor = self.get_entity(below_pos)

    return Neighbors(left_neighbor, right_neighbor, above_neighbor, below_neighbor)
  # end def

  def move(self, src_pos, dest_pos):
    if self.get_entity(dest_pos) is None:
      raise ValueError(str(dest_pos) + ' is occupied')

    src_entity = self.get_entity(src_pos)
    self.land[dest_pos.y][dest_pos.x] = src_entity
    self.land[src_pos.y][src_pos.x] = None
  # end def
# end class