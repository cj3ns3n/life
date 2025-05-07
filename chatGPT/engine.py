import logging

from position import Position
import operations


class Engine:
  def __init__(self, world):
    self.world = world

    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s - %(name)s', level=logging.INFO)
    self.logger = logging.getLogger('Engine')
  # end def

  def run(self):
    try:
      while True:
        for x in range(self.world.width):
          for y in range(self.world.height):
            entity_pos = Position(x, y, self.world.width, self.world.height)
            entity = self.world.get_entity(entity_pos)
            if entity:
              neighbors = self.world.get_neighbors(entity_pos)
              operation = entity.progress(neighbors)

              if type(operation) is operations.Talk:
                neighbor = neighbors.get(operation.dir)
                self.conversation(entity, neighbor)

              elif type(operation) is operations.Move:
                new_pos = entity_pos.get(operation.dir)
                try:
                  self.world.move(entity_pos, new_pos)
                  self.logger.info('legal move {} to {}'.format(entity.name, new_pos))
                except ValueError:
                  self.logger.info('\tillegal move {} to {}'.format(entity.name, new_pos))
                  entity.illegal_move()

              elif type(operation) is operations.Attack:
                neighbor = neighbors.get(operation.dir)
                self.attack(entity, neighbor)

              elif type(operation) is operations.GiveFood:
                self.give_food(entity, operation.dir, neighbors)
              # end if
            # end if
          # end for
        # end for
      # end while
    except KeyboardInterrupt:
      print("Simulation stopped.")
  # end def

  def conversation(self, entity, neighbor):
    done = False
    neighborMessage = entity.getMessage()
    while not done:
      if type(neighborMessage) == operations.EndConversation:
        neighbor.end_conversation()
        done = True
      else:
        response = neighbor.getResponse(neighborMessage)
        if type(response) == operations.EndConversation:
          entity.end_conversation()
          done = True
        else:
          neighborMessage = entity.getResponse(response)
      # end if
    # end while
  # end def

  def attack(self, attacker, neighbor):
    attacker_coef = attack.health + attacker.strength + max(1000 - attacker.age)
    neighbor_coef = neighbor.health + neighbor.strength + max(1000 - neighbor.age)
    if attacker_coef >= neighbor_coef:
      attacker.attack_success()
      neighbor.attacked()
    else:
      attacker.attack_failed()
      neighbor.attack_defended()
    # end if
  # end def
# end class
