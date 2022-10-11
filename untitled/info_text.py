import pygame

class InfoText():
    green = (0, 255, 0)
    blue = (0, 0, 128)

    def __init__(self):
        self.font = pygame.font.Font(None, 18)

        self.display_count = 0
        self.entity = None
        self.rect = pygame.Rect(0, 0, 0, 0)
    # end def

    def blit(self, surface, engine):
        gen_text = self.get_cycles_text(engine)
        gen_text_rec = gen_text.get_rect()
        gen_text_rec.topleft = (10, 10)
        surface.blit(gen_text, gen_text_rec)

        births_text = self.get_census_text(engine)
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

    def get_cycles_text(self, engine):
        text = self.font.render('Cycles %d' % engine.cycles, True, InfoText.green, InfoText.blue)
        textRect = text.get_rect()
        textRect.topleft = (10, 10)

        return text
    # end def

    def get_census_text(self, engine):
        text = self.font.render('Births: %02d; Deaths: %02d; Avg Age: %.1f, Stdv Age: %.1f, Avg Health: %.1f, Stdv Health: %.1f, Avg Size: %.1f, Stdv Size: %.1f'
                                % (engine.births, engine.deaths, engine.age_avg, engine.age_stdv, engine.health_avg, engine.health_stdv, engine.size_avg, engine.size_stdv), True, InfoText.green, InfoText.blue)
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
