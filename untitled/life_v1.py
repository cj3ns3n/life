import pygame
import random
from entity import Entity
from entity_engine import EntityEngine
from info_text import InfoText

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

class GenerationHandler():
    def __init__(self, info_text):
        self.generation = 0
        self.info_text = info_text

    def set_generation(self, generation):
        self.generation = generation
        self.info_text.set_generation(generation)
#end class

if __name__ == '__main__':
    # Initializing Pygame
    pygame.init()

    # Initializing surface
    display_size = (400, 300)
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

    display_count = 0
    while game_running:
        display_count += 1
        infoText.set_display_count(display_count)

        max_x = 0
        max_y = 0
        for x in range(display_size[0]):
            for y in range(display_size[1]):
                entity = entities[y][x]
                if handler.generation <= 1 or entity.age > handler.generation - 1:
                    max_x = x
                    max_y = max(max_y, y)
                    entity_rect = pygame.Rect(x, y, 1, 1)
                    pygame.draw.rect(surface, entity_color(entity), entity_rect)
                    #if handler.generation > 1:
                    #    print('(%03d, %03d) %03d, %03d, %03d' % (max_x, max_y, display_count, entity.age, handler.generation))
                    #pygame.display.update(entity_rect)
            #end for
        #end for

        gen_text = infoText.get_generation_text()
        surface.blit(gen_text[0], gen_text[1])
        display_text = infoText.get_display_text()
        surface.blit(display_text[0], display_text[1])

        if display_count <= 1:
            pygame.display.flip()
            #print('flip')
        else:
            gen_text_rec = gen_text[1]
            display_text_rec = display_text[1]
            width = max(gen_text_rec.width, display_text_rec.width, max_x) + 1
            height = max(gen_text_rec.height + display_text_rec.height, max_y) + 1
            update_rect = pygame.Rect(0, 0, width, height)
            #print(update_rect)
            pygame.display.update(update_rect)
        #end if

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_running = False
                    break

        pos = pygame.mouse.get_pos()
        if pos[0] != mouse_pos[0] or pos[1] != mouse_pos[1]:
            mouse_pos = pos
            print('mouse position', pos)
    #end while

    pygame.quit()
    exit()
#end if