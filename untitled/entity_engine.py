import threading

class EntityEngine(threading.Thread):
    def __init__(self, entities):
        threading.Thread.__init__(self)

        self.entities = entities
        self.size = (len(entities[0]), len(entities))
    #end def

    def run(self) :
        count = 0
        while True:
            print('progressing', count)
            count += 1
            for x in range(self.size[0]):
                for y in range(self.size[1]):
                    self.entities[y][x].progress()
    #end def
#end class