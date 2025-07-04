import pygame

from pos import Pos
from phenotypes.entity import Entity
from info_text import InfoText


class LifeDisplay:
    image_save_frequency = 10  # 10 cycles

    def __init__(self, land, change_queue, display_size, stats, logger):
        pygame.init()

        self.stats = stats
        self.infoText = InfoText()
        self.logger = logger

        self.display_size = display_size
        self.surface = pygame.display.set_mode(display_size)

        self.land = land
        self.change_queue = change_queue

        self.show_entity = True
        self.show_aspect_1 = False
        self.show_aspect_2 = False
        self.show_aspect_3 = False
        self.show_sparkles = True
        self.show_stats_overlay = False
        self.show_land = True

        self.changed_cells = []
    # end def

    def entity_color(self, entity):
        r = g = b = 0

        if entity is not None and entity.health > 0:
            if self.show_entity:
                r = entity.phenotype[0]
                g = entity.phenotype[1]
                b = entity.phenotype[2]
            else:
                if self.show_aspect_1:
                    if entity.age > self.max_age:
                        self.max_age = entity.age
                    r = int(255.0 * 1.0 - (entity.age / self.max_age))

                if self.show_aspect_2:
                    if entity.health < self.min_health:
                        self.min_health = entity.health
                    g = int(255.0 * (entity.health - self.min_health) / (self.max_health - self.min_health))

                if self.show_aspect_3:
                    if entity.sex == Entity.MALE:
                        b = 255
                    else:
                        r = 255

                    if entity.age < entity.mature_age:
                        g = 255
                # end if
            # end if

            if r < 0 or r > 255 or g < 0 or g > 255 or b < 0 or b > 255:
                self.logger.error('bad color: %s: %s' % (str((r, g, b)), str(entity)), True)
        # end if

        return (r, g, b)
    # end def

    def cell_color(self, cell):
        r = g = b = 0
        nutrient = cell.nutrient
        entity = cell.entity

        if entity:
            try:
                if self.show_entity or self.show_aspect_1 or self.show_aspect_2 or self.show_aspect_3:
                    r, g, b = entity.calc_color(self.show_aspect_1, self.show_aspect_2, self.show_aspect_3)
            except Exception as ex:
                self.logger.error('cell color error: %s - %s' % (entity, nutrient))
                self.logger.error(str(ex))
        # end if

        return (r, g, b)
    # end def

    def render_cells(self, cells):
        minx = self.display_size[0]
        miny = self.display_size[1]
        maxx = 0
        maxy = 0

        for cell in cells:
            minx = min(minx, cell.pos.x)
            miny = min(miny, cell.pos.y)
            maxx = max(maxx, cell.pos.x)
            maxy = max(maxy, cell.pos.y)

            try:
                cell_rect = pygame.Rect(cell.pos.x, cell.pos.y, 1, 1)
                pygame.draw.rect(self.surface, self.cell_color(cell), cell_rect)
            except ValueError:
                self.logger.error('draw.rect ValueError %s' % repr(cell.pos), True)
            # end try
        # end for
    # end def

    def render_cell(self, cell):
        try:
            cell_rect = pygame.Rect(cell.pos.x, cell.pos.y, 1, 1)
            pygame.draw.rect(self.surface, self.cell_color(cell), cell_rect)
        except ValueError:
            self.logger.error('draw.rect ValueError %s' % repr(pos), True)
        # end try

        if self.show_sparkles and cell.entity and cell.entity.age == 0:
            # show burst for newborns
            self.render_burst(cell.pos)
    # end def

    def render_row(self, row_idx):
        for x in range(0, self.display_size[0]):
            pos = Pos(x, row_idx)
            cell = self.land[pos]
            cell_rect = pygame.Rect(x, row_idx, 1, 1)
            try:
                pygame.draw.rect(self.surface, self.cell_color(cell), cell_rect)
            except ValueError:
                self.logger.error('draw.rect ValueError %s' % repr(pos), True)
            # end try

            if self.show_sparkles and cell.entity and cell.entity.age == 0:
                # show burst for newborns
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
                changed_cell = self.change_queue.get()
                self.changed_cells.append(changed_cell)
                if len(self.changed_cells) > 100:
                    self.render_cells(self.changed_cells)
                    self.changed_cells = []

                if self.show_stats_overlay:
                    self.infoText.blit(self.surface, self.stats)
                    pygame.display.update(self.infoText.get_rect())
            # end if

            self.logger.refresh_terminal()

            # save periodic image
            if self.stats.cycles % LifeDisplay.image_save_frequency == 0:
                filename = 'life-%07d.jpg' % self.stats.cycles
                #pygame.image.save(self.surface, filename)
            # end if

            self.stats.increment_display_iterations()
            #self.logger.info('display refreshes: %d' % self.stats.display_iterations)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_running = False
                        break
                    elif event.key == pygame.K_e:
                        self.show_entity = not self.show_entity
                    elif event.key == pygame.K_1:
                        self.show_aspect_1 = not self.show_aspect_1
                    elif event.key == pygame.K_2:
                        self.show_aspect_2 = not self.show_aspect_2
                    elif event.key == pygame.K_3:
                        self.show_aspect_3 = not self.show_aspect_3
                    elif event.key == pygame.K_b:
                        self.show_sparkles = not self.show_sparkles
                    elif event.key == pygame.K_n:
                        self.show_land = not self.show_land
                    elif event.key == pygame.K_o:
                        self.show_stats_overlay = not self.show_stats_overlay
                # end if
            # end for

            mouse_pos = Pos(tuple_pos=pygame.mouse.get_pos())
            if mouse_pos != last_mouse_pos:
                last_mouse_pos = mouse_pos
                #self.terminal.add_message('mouse position %s' % repr(mouse_pos))
                self.infoText.set_entity(self.land.get_entity(mouse_pos), mouse_pos)
        # end while

        self.logger.shutdown()
        pygame.quit()
        exit()
    #end def
#end class
