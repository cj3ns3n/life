import pygame

class InfoText():
    def __init__(self):
        self.font = pygame.font.Font(None, 18)

        self.generation = 0
        self.updated = True
    #end def

    def set_generation(self, generation):
        self.generation = generation

    def getText(self):
        green = (0, 255, 0)
        blue = (0, 0, 128)

        text = self.font.render('Generation %d' % self.generation, True, green, blue)
        textRect = text.get_rect()
        textRect.topleft = (10, 10)
#        textRect.center = (35, 10)

        self.updated = False
        return (text, textRect)
