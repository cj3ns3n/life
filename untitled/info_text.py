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

    def blit(self, surface, stats_container):
        y_loc = InfoText.initial_y_loc
        stats = stats_container.get_stats()

        gen_text = self.font.render('Cycles %d' % stats['cycles'], True, InfoText.green, InfoText.blue)
        gen_text_rec = gen_text.get_rect()
        gen_text_rec.topleft = (10, y_loc)
        surface.blit(gen_text, gen_text_rec)
        y_loc += gen_text_rec.height

        pop_text = self.font.render('Population %d' % (stats['births'] - stats['maternal_deaths'] - stats['natural_deaths']), True, InfoText.green, InfoText.blue)
        pop_text_rec = pop_text.get_rect()
        pop_text_rec.topleft = (10, y_loc)
        surface.blit(pop_text, pop_text_rec)
        y_loc += pop_text_rec.height

        births = stats['births']
        m_deaths = stats['maternal_deaths']
        n_deaths = stats['natural_deaths']
        m_deathrate = 100.0 * float(m_deaths) / float(births) if births > 0 else 0.0
        n_deathrate = 100.0 * float(n_deaths) / float(births) if births > 0 else 0.0  # skewed because initial spawned entities are not in the birth count
        births_text_str = 'Births: %02d; Maternal Deaths: %02d (rate: %0.1f%%); Natural Deaths: %02d (rate: %0.1f%%)' % (births, m_deaths, m_deathrate, n_deaths, n_deathrate)
        births_text = self.font.render(births_text_str, True, InfoText.green, InfoText.blue)
        births_text_rec = births_text.get_rect()
        births_text_rec.topleft = (10, y_loc)
        surface.blit(births_text, births_text_rec)
        y_loc += births_text_rec.height

        age_text = self.font.render('Avg Age: %.1f, Stdv Age: %.1f' % (stats['age_avg'], stats['age_stdev']), True, InfoText.green, InfoText.blue)
        age_text_rec = age_text.get_rect()
        age_text_rec.topleft = (10, y_loc)
        surface.blit(age_text, age_text_rec)
        y_loc += age_text_rec.height

        health_text = self.font.render('Avg Health: %.1f, Stdv Health: %.1f' % (stats['health_avg'], stats['health_stdev']), True, InfoText.green, InfoText.blue)
        health_text_rec = health_text.get_rect()
        health_text_rec.topleft = (10, y_loc)
        surface.blit(health_text, health_text_rec)
        y_loc += health_text_rec.height

        size_text = self.font.render('Avg Size: %.1f, Stdv Size: %.1f' % (stats['size_avg'], stats['size_stdev']), True, InfoText.green, InfoText.blue)
        size_text_rec = size_text.get_rect()
        size_text_rec.topleft = (10, y_loc)
        surface.blit(size_text, size_text_rec)
        y_loc += size_text_rec.height

        display_text = self.font.render('Refreshes %d' % stats['display_iterations'], True, InfoText.green, InfoText.blue)
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

    def set_entity(self, entity, entity_pos):
        self.entity = entity
        self.entity_pos = entity_pos

    def get_entity_text(self):
        entity_text = 'Entity: None'
        if self.entity:
            entity_text = 'Entity: %s %s' % (str(self.entity_pos), str(self.entity))

        text = self.font.render(entity_text, True, InfoText.green, InfoText.blue)
        return text
    # end def
# end def
