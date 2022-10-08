import pygame
from entity import Entity
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

        self.entities = self.birth_entities(display_size)

        self.infoText = InfoText()

        self.handler = GenerationHandler(self.infoText)
        self.engine = EntityEngine(self.entities, self.handler)
        self.engine.daemon = True
        self.engine.start()

        self.max_age = 100
        self.max_size = 2
        self.min_size = 1
        self.max_health = 100
        self.min_health = 75
    #end def

    def birth_entities(self, size):
        entities = []
        for y in range(size[1]):
            row = []
            for x in range(size[0]):
                row.append(Entity())
            entities.append(row)
        #end for

        return entities
    #end def

    def entity_color(self, entity):
        entity_color = (0, 0, 0)
        if entity.health > 0:
            if entity.age > self.max_age:
                self.max_age = self.max_age * 10
            if entity.size > self.max_size:
                self.max_size = entity.size
            if entity.size < self.min_size:
                self.min_size = entity.size
            if entity.health < self.min_health:
                self.min_health = entity.health

            r = int(255.0 * entity.age / self.max_age)
            g = int(255.0 * (entity.health - self.min_health) / (self.max_health - self.min_health))
            b = int(255.0 * (entity.size - self.min_size) / (self.max_size - self.min_size))

            entity_color = (r, g, b)

            if r < 0 or r > 255 or g < 0 or g > 255 or b < 0 or b > 255:
                print('%s: %s' % (str(entity_color), str(entity)))
        # end if

        return entity_color
    #end def

    def render_rows(self, x_range, y_range):
        for x in range(x_range[0], x_range[1]):
            for y in range(y_range[0], y_range[1]):
                entity = self.entities[y][x]
                entity_rect = pygame.Rect(x, y, 1, 1)
                pygame.draw.rect(self.surface, self.entity_color(entity), entity_rect)
            #end for
        #end for
    #end def

    def display(self):
        game_running = True
        last_mouse_pos = Pos(0, 0)

        self.render_rows((0, self.display_size[0]), (0, self.display_size[1]))

        display_count = 0
        image_count = 0
        while game_running:
            display_count += 1
            self.infoText.set_display_count(display_count)

            gen_text = self.infoText.get_generation_text()
            self.surface.blit(gen_text[0], gen_text[1])
            births_text = self.infoText.get_census_text()
            self.surface.blit(births_text[0], births_text[1])
            display_text = self.infoText.get_display_text()
            self.surface.blit(display_text[0], display_text[1])
            entity_text = self.infoText.get_entity_text()
            self.surface.blit(entity_text[0], entity_text[1])

            if display_count <= 1:
                pygame.display.flip()
            else:
                # refresh updated entities
                max_row = 0
                min_row = 0
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

                # refresh info text
                gen_text_rec = gen_text[1]
                births_text_rec = births_text[1]
                display_text_rec = display_text[1]
                entity_text_rec = entity_text[1]

                #print('update: %d, (%03d, %03d)' % (len(updated_rows), min_row, max_row))
                if gen_text_rec.top > max_row or display_text_rec.bottom < min_row:
                    height = gen_text_rec.height + births_text_rec.height + display_text_rec.height + entity_text_rec.height
                    width = max([gen_text_rec.width, births_text_rec.width, display_text_rec.width, entity_text_rec.width])
                    update_rect = pygame.Rect(gen_text_rec.left, gen_text_rec.top, width, height)

                    pygame.display.update(update_rect)
                #end def
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
                # end if
            # end for

            mouse_pos = Pos(tuple=pygame.mouse.get_pos())
            if mouse_pos != last_mouse_pos:
                last_mouse_pos = mouse_pos
                #print('mouse position', pos)
                self.infoText.set_entity(self.entities[mouse_pos.y][mouse_pos.x], mouse_pos)
        # end while

        pygame.quit()
        exit()
    #end def
#end class
