import random
import logging
import uuid

import operations
import direction

class Entity:
  FEMALE = 'female'
  MALE = 'male'

  def __init__(self):
    self.age = 0
    self.name = str(uuid.uuid4()).split('-')[1]
    self.sex = random.choice([Entity.MALE, Entity.FEMALE])
    self.health = 100
    self.strength = 1
    self.size = 1
    #self.strength = min(0.1, np.random.normal(1, Entity.strength_range))
    #self.size = min(0.1, np.random.normal(1, Entity.size_range))

    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s - %(name)s', level=logging.INFO)
    self.logger = logging.getLogger('Entity')

    #self.setup_AI()
  # end def

  def progress(self, neighborhood):
    return self.get_operation(neighborhood)
  # end def

  def get_operation(self, neighborhood):
    return operations.Move(direction.RIGHT)
  # end def

  def illegal_move(self):
    pass
  # end def
# end class
