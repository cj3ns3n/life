import threading

class EntityEngine(threading.Thread):
    def __init__(self, entities):
        threading.Thread.__init__(self)

        self.entities = entities
    #end def

    def run(self) :
        count = 0
        while True:
            #print('progressing', count)
            count += 1
            for entity in self.entities:
                entity.progress()
        #end while
    #end def
#end class