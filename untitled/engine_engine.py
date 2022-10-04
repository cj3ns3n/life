import threading
from entity_engine import EntityEngine

class EngineEngine(threading.Thread):
    def __init__(self, entities):
        threading.Thread.__init__(self)

        self.entities = entities
        self.size = (len(entities[0]), len(entities))
    #end def

    def run(self) :
        count = 0
        for i in range(self.size[1]):
            print('starting engine', count)
            count += 1
            entityEngine = EntityEngine(self.entities[i])
            entityEngine.setDaemon(True)
            entityEngine.start()
    #end def
#end class