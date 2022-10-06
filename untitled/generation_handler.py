class GenerationHandler():
    def __init__(self, info_text):
        self.generation = 0
        self.updated_rows = []
        self.info_text = info_text
    #end def

    def set_generation(self, generation):
        self.generation = generation
        self.info_text.set_generation(generation)
    #end def

    def row_progressed(self, row_idx):
        self.updated_rows.append(row_idx)
        #print('updated row: %d' % row_idx)
    #end def

    def get_processed_rows(self):
        rows = self.updated_rows.copy()
        self.updated_rows = []
        return rows
    #end def
#end class
