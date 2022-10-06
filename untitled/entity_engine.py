import threading

class EntityEngine(threading.Thread):
    def __init__(self, entities, generation_handler):
        threading.Thread.__init__(self)

        self.entities = entities
        self.generation_handler = generation_handler
    #end def

    def run(self) :
        generationCount = 0
        while True:
            #print('progressing', count)
            generationCount += 1
            self.generation_handler.set_generation(generationCount)
            rowCount = 0
            for entity_row in self.entities:
                for entity in entity_row:
                    entity.progress()
                self.generation_handler.row_progressed(rowCount)
                rowCount += 1
        #end while
    #end def
#end class