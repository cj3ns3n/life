import threading
from pos import Pos

class EntityEngine(threading.Thread):
    def __init__(self, entities, generation_handler):
        threading.Thread.__init__(self)

        self.entities = entities
        self.generation_handler = generation_handler
    # end def

    def run(self) :
        generationCount = 0
        while True:
            #print('progressing', count)
            generationCount += 1
            self.generation_handler.set_generation(generationCount)
            for y in range(self.entities.height):
                for x in range(self.entities.width):
                    pos = Pos(x, y)
                    neighbors = self.entities.get_neighbors(pos)
                    entity = self.entities[pos]
                    if entity is not None and entity.health > 0:
                        child = entity.progress(neighbors)
                        #if x == 0 and y == 0:
                        #    print((entity.age, entity.health, entity.initial_health_factor, entity.life_expectancy))
                        if not entity.health > 0:
                            self.generation_handler.increment_deaths()
                        if child:
                            new_pos = self.entities.get_vacant_neighbor_pos(pos)
                            if new_pos:
                                #print('dead: %s' % (str(self.entities[new_pos[1]][new_pos[0]])))
                                self.entities[new_pos] = child
                                self.generation_handler.increment_births()
                            # end if
                        # end if
                    # end if
                # end for
                self.generation_handler.row_progressed(y)
        # end while
    # end def
# end class