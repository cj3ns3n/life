import pygame
from entities import Entities
from entity_engine import EntityEngine
from info_text import InfoText
from generation_handler import GenerationHandler
from pos import Pos

class LifeDisplay:
    image_save_frequency = 1 * 60 * 1000 # 1 minute

    def __init__(self, display_size = (600, 300)):
        pygame.init()
        self.display_size = display_size
        self.surface = pygame.display.set_mode(display_size)

        self.entities = Entities(display_size)

        self.infoText = InfoText()

        self.handler = GenerationHandler(self.infoText)
        self.engine = EntityEngine(self.entities, self.handler)
        self.engine.daemon = True
        self.engine.start()

        self.max_age = 120
        self.max_size = 2
        self.min_size = 1
        self.max_health = 100
        self.min_health = 75

        self.show_age = True
        self.show_health = True
        self.show_size = True
    #end def

    def entity_color(self, entity):
        r = g = b = 0

        if entity is not None and entity.health > 0:
            if self.show_age:
                if entity.age > self.max_age:
                    self.max_age = entity.age
                r = int(255.0 * entity.age / self.max_age)
            # end if

            if self.show_health:
                if entity.health < self.min_health:
                    self.min_health = entity.health
                g = int(255.0 * (entity.health - self.min_health) / (self.max_health - self.min_health))
            # end if

            if self.show_size:
                if entity.size > self.max_size:
                    self.max_size = entity.size
                if entity.size < self.min_size:
                    self.min_size = entity.size

                b = int(255.0 * (entity.size - self.min_size) / (self.max_size - self.min_size))
            # end if

            if r < 0 or r > 255 or g < 0 or g > 255 or b < 0 or b > 255:
                print('%s: %s' % (str((r, g, b)), str(entity)))
        # end if

        return (r, g, b)
    # end def

    def render_rows(self, x_range, y_range):
        for x in range(x_range[0], x_range[1]):
            for y in range(y_range[0], y_range[1]):
                entity = self.entities[Pos(x, y)]
                entity_rect = pygame.Rect(x, y, 1, 1)
                pygame.draw.rect(self.surface, self.entity_color(entity), entity_rect)
            # end for
        # end for
    # end def

    def display(self):
        game_running = True
        last_mouse_pos = Pos(0, 0)

        self.render_rows((0, self.display_size[0]), (0, self.display_size[1]))

        display_count = 0
        image_count = 0
        while game_running:
            display_count += 1
            self.infoText.set_display_count(display_count)
            self.infoText.blit(self.surface, self.engine)

            if display_count <= 1:
                pygame.display.flip()
            else:
                # refresh updated entities
                updated_rows = self.handler.get_processed_rows()
                if len(updated_rows) > 0:
                    max_row = max(updated_rows)
                    min_row = min(updated_rows)

                    self.render_rows((0, self.display_size[0]), (min_row, max_row + 1))

                    width = self.display_size[0]
                    height = max_row - min_row + 1
                    update_rect = pygame.Rect(0, min(updated_rows), width, height)
                    #print('update: %d, (%03d, %03d)' % (len(updated_rows), min_row, max_row))
                    #print(update_rect)
                    pygame.display.update(update_rect)
                #end if

                pygame.display.update(self.infoText.get_rect())
            #end if

            # save periodic image
            if pygame.time.get_ticks() > LifeDisplay.image_save_frequency * image_count:
                filename = 'life-%04d.jpg' % image_count
                pygame.image.save(self.surface, filename)
                print('saved %s' % filename)
                image_count += 1
            # end if

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
                    elif event.key == pygame.K_h:
                        self.show_health = not self.show_health
                    elif event.key == pygame.K_s:
                        self.show_size = not self.show_size
                # end if
            # end for

            mouse_pos = Pos(tuple=pygame.mouse.get_pos())
            if mouse_pos != last_mouse_pos:
                last_mouse_pos = mouse_pos
                #print('mouse position', pos)
                self.infoText.set_entity(self.entities[mouse_pos], mouse_pos)
        # end while

        pygame.quit()
        exit()
    #end def
#end class
