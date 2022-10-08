import pygame

class InfoText():
    green = (0, 255, 0)
    blue = (0, 0, 128)

    def __init__(self):
        self.font = pygame.font.Font(None, 18)

        self.generation = 0
        self.display_count = 0
        self.births = 0
        self.deaths = 0
        self.entity = None
        self.rect = pygame.Rect(0, 0, 0, 0)
    # end def

    def blit(self, surface):
        gen_text = self.get_generation_text()
        gen_text_rec = gen_text.get_rect()
        gen_text_rec.topleft = (10, 10)
        surface.blit(gen_text, gen_text_rec)

        births_text = self.get_census_text()
        births_text_rec = births_text.get_rect()
        births_text_rec.topleft = (10, 20)
        surface.blit(births_text, births_text_rec)

        display_text = self.get_display_text()
        display_text_rec = display_text.get_rect()
        display_text_rec.topleft = (10, 30)
        surface.blit(display_text, display_text_rec)

        entity_text = self.get_entity_text()
        entity_text_rec = entity_text.get_rect()
        entity_text_rec.topleft = (10, 40)
        surface.blit(entity_text, entity_text_rec)

        height = gen_text_rec.height + births_text_rec.height + display_text_rec.height + entity_text_rec.height
        width = max([gen_text_rec.width, births_text_rec.width, display_text_rec.width, entity_text_rec.width])
        self.rect = pygame.Rect(gen_text_rec.left, gen_text_rec.top, width, height)
    # end def

    def get_rect(self):
        return self.rect
    # end def

    def set_generation(self, generation):
        self.generation = generation

    def get_generation_text(self):
        text = self.font.render('Generation %d' % self.generation, True, InfoText.green, InfoText.blue)
        textRect = text.get_rect()
        textRect.topleft = (10, 10)

        return text
    # end def

    def set_deaths(self, death_count):
        self.deaths = death_count

    def set_births(self, birth_count):
        self.births = birth_count

    def get_census_text(self):
        text = self.font.render('Births: %02d; Deaths: %02d' % (self.births, self.deaths), True, InfoText.green, InfoText.blue)
        textRect = text.get_rect()
        textRect.topleft = (10, 20)

        return text
    # end def

    def set_display_count(self, display_count):
        self.display_count = display_count

    def get_display_text(self):
        text = self.font.render('Refreshes %d' % self.display_count, True, InfoText.green, InfoText.blue)
        textRect = text.get_rect()
        textRect.topleft = (10, 30)

        return text
    # end def

    def set_entity(self, entity, entity_pos):
        self.entity = entity
        self.entity_pos = entity_pos

    def get_entity_text(self):
        entity_text = 'Entity: None'
        if self.entity:
            entity_text = 'Entity: %s %s' % (str(self.entity_pos), str(self.entity))

        text = self.font.render(entity_text, True, InfoText.green, InfoText.blue)
        textRect = text.get_rect()
        textRect.topleft = (10, 40)

        return text
    # end def
# end def
