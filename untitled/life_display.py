import pygame
from pos import Pos
from entity import Entity
from entities import Entities
from entity_engine import EntityEngine
from stats_container import StatsContainer
from info_text import InfoText
from terminal_display import TerminalDisplay
from terra_firma import Land
from logger import Logger


class LifeDisplay:
    image_save_frequency = 10 # 10 cycles

    def __init__(self, display_size = (600, 300)):
        pygame.init()

        self.stats = StatsContainer()
        self.infoText = InfoText()
        self.terminal = TerminalDisplay(self.stats)
        self.logger = Logger(self.terminal, __name__, 'life.log')

        self.display_size = display_size
        self.surface = pygame.display.set_mode(display_size)

        self.entities = Entities(display_size, self.logger.get_logger(Entities.__name__))
        self.land = Land(display_size, self.logger.get_logger(Land.__name__))

        self.engine = EntityEngine(self.entities, self.land, self.stats, self.logger.get_logger(EntityEngine.__name__))
        self.engine.daemon = True
        self.engine.start()

        self.max_age = 120
        self.min_size = 1
        self.max_health = 100
        self.min_health = 75

        self.show_phenotype = True
        self.show_age = True
        self.show_sparkles = True
        self.show_health = True
        self.show_sex = True
        self.show_stats_overlay = False
        self.show_land = True
    # end def

    def entity_color(self, entity):
        r = g = b = 0

        if entity is not None and entity.health > 0:
            if self.show_phenotype:
                r = entity.phenotype[0]
                g = entity.phenotype[1]
                b = entity.phenotype[2]
            else:
                if self.show_age:
                    if entity.age > self.max_age:
                        self.max_age = entity.age
                    r = int(255.0 * 1.0 - (entity.age / self.max_age))

                if self.show_health:
                    if entity.health < self.min_health:
                        self.min_health = entity.health
                    g = int(255.0 * (entity.health - self.min_health) / (self.max_health - self.min_health))

                if self.show_sex:
                    if entity.sex == Entity.MALE:
                        b = 255
                    else:
                        r = 255

                    if entity.age < entity.mature_age:
                        g = 255
                # end if
            # end if

            if r < 0 or r > 255 or g < 0 or g > 255 or b < 0 or b > 255:
                self.terminal.add_message('bad color: %s: %s' % (str((r, g, b)), str(entity)))
        # end if

        return (r, g, b)
    # end def

    def cell_color(self, entity, nutrient):
        r = g = b = 0

        if self.show_phenotype or self.show_age or self.show_health or self.show_sex:
            r, g, b = self.entity_color(entity)
            if nutrient and self.show_land:
                n = nutrient.nutrient_level / 100.0
                if r == 0 and g == 0 and b == 0:
                    r = g = b = int(255 * n)
                else:
                    r = int(r * n)
                    g = int(g * n)
                    b = int(b * n)
        elif nutrient and self.show_land:
            r = g = b = int(255 * nutrient.nutrient_level / 100.0)
        # end if

        return (r, g, b)
    # end def

    def render_row(self, row_idx):
        for x in range(0, self.display_size[0]):
            pos = Pos(x, row_idx)
            entity = self.entities[pos]
            nutrient = self.land[pos]
            entity_rect = pygame.Rect(x, row_idx, 1, 1)
            try:
                pygame.draw.rect(self.surface, self.cell_color(entity, nutrient), entity_rect)
            except ValueError:
                self.logger.error('draw.rect ValueError %s' % repr(entity), True)
            # end try

            if self.show_sparkles and entity and entity.age == 0:
                # show burst for new borns
                self.render_burst(pos)
        # end for
    # end def

    def render_rows(self, y_range):
        for y in range(y_range[0], y_range[1]):
            self.render_row(y)
    # end def

    def render_burst(self, pos):
        leftx = max(0, pos.x - 3)
        lefty = max(0, pos.y - 3)
        centerx = max(0, pos.x - 1)
        centery = max(0, pos.y - 1)

        burst_rect = pygame.Rect(leftx, pos.y, 7, 1)
        pygame.draw.rect(self.surface, (255, 255, 255, 250), burst_rect)
        burst_rect = pygame.Rect(pos.x, lefty, 1, 7)
        pygame.draw.rect(self.surface, (255, 255, 255, 250), burst_rect)
        burst_rect = pygame.Rect(centerx, centery, 3, 3)
        pygame.draw.rect(self.surface, (255, 255, 255, 250), burst_rect)

        return pygame.Rect(leftx, lefty, 7, 7)
    # end def

    def display(self):
        self.terminal.run()

        game_running = True
        last_mouse_pos = Pos(0, 0)

        self.render_rows((0, self.display_size[1]))

        self.logger.info('display started')
        first = True
        while game_running:
            if first:
                pygame.display.flip()
                first = False
            else:
                # refresh updated entities
                updated_rows = self.engine.get_processed_rows()
                for updated_row in updated_rows:
                    self.render_row(updated_row)

                    width = self.display_size[0]
                    height = 1
                    update_rect = pygame.Rect(0, updated_row, width, height)
                    pygame.display.update(update_rect)
                # end if

                if self.show_stats_overlay:
                    self.infoText.blit(self.surface, self.stats)
                    pygame.display.update(self.infoText.get_rect())
            # end if

            self.terminal.run()

            # save periodic image
            if self.stats.cycles % LifeDisplay.image_save_frequency == 0:
                filename = 'life-%07d.jpg' % self.stats.cycles
                #pygame.image.save(self.surface, filename)
            # end if

            self.stats.increment_display_iterations()
            self.logger.info('display refreshes: %d' % self.stats.display_iterations)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_running = False
                        break
                    elif event.key == pygame.K_a:
                        self.show_age = not self.show_age
                    elif event.key == pygame.K_b:
                        self.show_sparkles = not self.show_sparkles
                    elif event.key == pygame.K_h:
                        self.show_health = not self.show_health
                    elif event.key == pygame.K_l:
                        self.show_land = not self.show_land
                    elif event.key == pygame.K_o:
                        self.show_stats_overlay = not self.show_stats_overlay
                    elif event.key == pygame.K_p:
                        self.show_phenotype = not self.show_phenotype
                    elif event.key == pygame.K_s:
                        self.show_sex = not self.show_sex
                # end if
            # end for

            mouse_pos = Pos(tuple_pos=pygame.mouse.get_pos())
            if mouse_pos != last_mouse_pos:
                last_mouse_pos = mouse_pos
                #self.terminal.add_message('mouse position %s' % repr(mouse_pos))
                self.infoText.set_entity(self.entities[mouse_pos], mouse_pos)
        # end while

        self.terminal.shutdown()
        pygame.quit()
        exit()
    #end def
#end class
