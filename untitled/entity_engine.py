import threading

class EntityEngine(threading.Thread):
    def __init__(self, entities, generation_handler):
        threading.Thread.__init__(self)

        self.entities = entities
        self.generation_handler = generation_handler
        self.size = (len(entities[0]), len(entities))
    #end def

    def get_neighbors(self, pos):
        neighbors = []
        if pos[0] > 0: # left neighbor
            neighbors.append(self.entities[pos[1]][pos[0]-1])
        if pos[0] < self.size[0] - 1: # right neighbor
            neighbors.append(self.entities[pos[1]][pos[0]+1])
        if pos[1] > 0: # top neighbor
            neighbors.append(self.entities[pos[1]-1][pos[0]])
        if pos[1] < self.size[1] - 1: # bottom neighbor
            neighbors.append(self.entities[pos[1]+1][pos[0]])

        return neighbors
    #end def

    def run(self) :
        generationCount = 0
        while True:
            #print('progressing', count)
            generationCount += 1
            self.generation_handler.set_generation(generationCount)
            for y in range(self.size[1]):
                for x in range(self.size[0]):
                    self.entities[y][x].progress(self.get_neighbors((x, y)))
                self.generation_handler.row_progressed(y)
        #end while
    #end def
#end class