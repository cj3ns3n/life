import pygame
import random
from entity import Entity
from entity_engine import EntityEngine
from info_text import InfoText
from generation_handler import GenerationHandler

def change_color(color):
    r_variance = color[0] * random.uniform(-0.1, 0.1)
    new_r = max(10, color[0] + r_variance)
    new_r = min(new_r, 255)
    new_color = (int(new_r), color[1], color[2])
    #print(new_color)
    return new_color
#end def

def entity_color(entity):
    r = int(255.0 * entity.age / 1000000.0)
    g = int(255.0 * entity.size / 100.0)
    b = int(255.0 * entity.health / 100.0)

    entity_color = (r, g, b)
    #print(str(entity))
    #print(entity_color)

    return entity_color
#end def

def render_rows(entities, x_range, y_range):
    for x in range(x_range[0], x_range[1]):
        for y in range(y_range[0], y_range[1]):
            entity = entities[y][x]
            entity_rect = pygame.Rect(x, y, 1, 1)
            pygame.draw.rect(surface, entity_color(entity), entity_rect)
        #end for
    #end for
#end def

if __name__ == '__main__':
    # Initializing Pygame
    pygame.init()

    # Initializing surface
    display_size = (600, 300)
    surface = pygame.display.set_mode(display_size)

    # Initialing Color
    color = (255, 0, 0)

    infoText = InfoText()

    game_running = True
    mouse_pos = (0,0)
    entities = []
    for y in range(display_size[1]):
        row = []
        for x in range(display_size[0]):
            row.append(Entity())
        entities.append(row)
    #end for

    handler = GenerationHandler(infoText)
    engine = EntityEngine(entities, handler)
    engine.daemon = True
    #engine.setDaemon(True)
    engine.start()

    render_rows(entities, (0, display_size[0]), (0, display_size[1]))

    display_count = 0
    while game_running:
        display_count += 1
        infoText.set_display_count(display_count)

        gen_text = infoText.get_generation_text()
        surface.blit(gen_text[0], gen_text[1])
        display_text = infoText.get_display_text()
        surface.blit(display_text[0], display_text[1])

        if display_count <= 1:
            pygame.display.flip()
            #print('flip')
        else:
            # refresh updated entities
            max_row = 0
            min_row = 0
            updated_rows = handler.get_processed_rows()
            if len(updated_rows) > 0:
                max_row = max(updated_rows)
                min_row = min(updated_rows)

                render_rows(entities, (0, display_size[0]), (min_row, max_row + 1))

                width = display_size[0]
                height = max_row - min_row + 1
                update_rect = pygame.Rect(0, min(updated_rows), width, height)
                #print('update: %d, (%03d, %03d)' % (len(updated_rows), min_row, max_row))
                #print(update_rect)
                pygame.display.update(update_rect)
            #end if

            # refresh info text
            gen_text_rec = gen_text[1]
            display_text_rec = display_text[1]

            #print('update: %d, (%03d, %03d)' % (len(updated_rows), min_row, max_row))
            if gen_text_rec.top > max_row or display_text_rec.bottom < min_row:
                height = gen_text_rec.height + display_text_rec.height
                width = max([gen_text_rec.width, display_text_rec.width])
                update_rect = pygame.Rect(gen_text_rec.left, gen_text_rec.top, width, height)
                pygame.display.update(update_rect)
            #end def
        #end if

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_running = False
                    break
        #end for

        pos = pygame.mouse.get_pos()
        if pos[0] != mouse_pos[0] or pos[1] != mouse_pos[1]:
            mouse_pos = pos
            print('mouse position', pos)
    #end while

    pygame.quit()
    exit()
#end if