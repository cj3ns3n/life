import pygame

class InfoText():
    green = (0, 255, 0)
    blue = (0, 0, 128)

    def __init__(self):
        self.font = pygame.font.Font(None, 18)

        self.generation = 0
        self.display_count = 0
        self.entity = None
    #end def

    def set_generation(self, generation):
        self.generation = generation

    def get_generation_text(self):
        text = self.font.render('Generation %d' % self.generation, True, InfoText.green, InfoText.blue)
        textRect = text.get_rect()
        textRect.topleft = (10, 10)

        return (text, textRect)
    #end def

    def set_display_count(self, display_count):
        self.display_count = display_count

    def get_display_text(self):
        text = self.font.render('Refreshes %d' % self.display_count, True, InfoText.green, InfoText.blue)
        textRect = text.get_rect()
        textRect.topleft = (10, 20)

        return (text, textRect)
    #end def

    def set_entity(self, entity, entity_pos):
        self.entity = entity
        self.entity_pos = entity_pos

    def get_entity_text(self):
        entity_text = 'Entity: None'
        if self.entity:
            entity_text = 'Entity: (%03d, %03d) %s' % (self.entity_pos[0], self.entity_pos[1], str(self.entity))

        text = self.font.render(entity_text, True, InfoText.green, InfoText.blue)
        textRect = text.get_rect()
        textRect.topleft = (10, 30)

        return (text, textRect)

#end def
