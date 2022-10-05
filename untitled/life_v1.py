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

if __name__ == '__main__':
    # Initializing Pygame
    pygame.init()

    # Initializing surface
    display_size = (400, 300)
    surface = pygame.display.set_mode(display_size)

    # Initialing Color
    color = (255,0,0)

    game_running = True
    mouse_pos = (0,0)
    entities = []
    for y in range(display_size[1]):
        row = []
        for x in range(display_size[0]):
            row.append(Entity())
        entities.append(row)
    #end for

    engine = EntityEngine(entities)
    engine.daemon = True
    #engine.setDaemon(True)
    engine.start()

    infoText = InfoText()

    while game_running:
        for x in range(display_size[0]):
            for y in range(display_size[1]):
                pygame.draw.rect(surface, entity_color(entities[y][x]), pygame.Rect(x, y, 1, 1))

        text, textRect = infoText.getText()
        surface.blit(text, textRect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_running = False
                    break

        pos = pygame.mouse.get_pos()
        if (pos[0] != mouse_pos[0] or pos[1] != mouse_pos[1]):
            mouse_pos = pos
            print('mouse position',pos)
    #end while

    pygame.quit()
    exit()
#end if