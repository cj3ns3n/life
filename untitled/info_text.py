import pygame

class InfoText():
    green = (0, 255, 0)
    blue = (0, 0, 128)
    initial_y_loc = 10

    def __init__(self):
        self.font = pygame.font.Font(None, 18)

        self.display_count = 0
        self.entity = None
        self.rect = pygame.Rect(0, 0, 0, 0)
    # end def

    def blit(self, surface, engine):
        y_loc = InfoText.initial_y_loc

        gen_text = self.get_cycles_text(engine)
        gen_text_rec = gen_text.get_rect()
        gen_text_rec.topleft = (10, y_loc)
        surface.blit(gen_text, gen_text_rec)
        y_loc += gen_text_rec.height

        births_text = self.get_births_stats(engine)
        births_text_rec = births_text.get_rect()
        births_text_rec.topleft = (10, y_loc)
        surface.blit(births_text, births_text_rec)
        y_loc += births_text_rec.height

        age_text = self.get_age_stats(engine)
        age_text_rec = age_text.get_rect()
        age_text_rec.topleft = (10, y_loc)
        surface.blit(age_text, age_text_rec)
        y_loc += age_text_rec.height

        health_text = self.get_health_stats(engine)
        health_text_rec = health_text.get_rect()
        health_text_rec.topleft = (10, y_loc)
        surface.blit(health_text, health_text_rec)
        y_loc += health_text_rec.height

        size_text = self.get_size(engine)
        size_text_rec = size_text.get_rect()
        size_text_rec.topleft = (10, y_loc)
        surface.blit(size_text, size_text_rec)
        y_loc += size_text_rec.height

        display_text = self.get_display_text()
        display_text_rec = display_text.get_rect()
        display_text_rec.topleft = (10, y_loc)
        surface.blit(display_text, display_text_rec)
        y_loc += display_text_rec.height

        entity_text = self.get_entity_text()
        entity_text_rec = entity_text.get_rect()
        entity_text_rec.topleft = (10, y_loc)
        surface.blit(entity_text, entity_text_rec)
        y_loc += entity_text_rec.height

        height = y_loc - InfoText.initial_y_loc
        width = max([gen_text_rec.width, births_text_rec.width, age_text_rec.width, health_text_rec.width, size_text_rec.width, display_text_rec.width, entity_text_rec.width])
        self.rect = pygame.Rect(gen_text_rec.left, gen_text_rec.top, width, height)
    # end def

    def get_rect(self):
        return self.rect
    # end def

    def get_cycles_text(self, engine):
        text = self.font.render('Cycles %d' % engine.cycles, True, InfoText.green, InfoText.blue)
        return text
    # end def

    def get_births_stats(self, engine):
        text = self.font.render('Births: %02d; Deaths: %02d' % (engine.births, engine.deaths), True, InfoText.green, InfoText.blue)
        return text
    # end def

    def get_age_stats(self, engine):
        text = self.font.render('Avg Age: %.1f, Stdv Age: %.1f' % (engine.age_avg, engine.age_stdv), True, InfoText.green, InfoText.blue)
        return text
    # end def

    def get_health_stats(self, engine):
        text = self.font.render('Avg Health: %.1f, Stdv Health: %.1f' % (engine.health_avg, engine.health_stdv), True, InfoText.green, InfoText.blue)
        return text
    # end def

    def get_size(self, engine):
        text = self.font.render('Avg Size: %.1f, Stdv Size: %.1f' % (engine.size_avg, engine.size_stdv), True, InfoText.green, InfoText.blue)
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
