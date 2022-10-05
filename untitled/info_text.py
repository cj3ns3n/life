import pygame

class InfoText():
    def __init__(self):
        self.font = pygame.font.Font(None, 18)

        self.generation = 0
        self.display_count = 0
    #end def

    def set_generation(self, generation):
        self.generation = generation

    def get_generation_text(self):
        green = (0, 255, 0)
        blue = (0, 0, 128)

        text = self.font.render('Generation %d' % self.generation, True, green, blue)
        textRect = text.get_rect()
        textRect.topleft = (10, 10)

        return (text, textRect)

    def set_display_count(self, display_count):
        self.display_count = display_count

    def get_display_text(self):
        green = (0, 255, 0)
        blue = (0, 0, 128)

        text = self.font.render('Refreshes %d' % self.display_count, True, green, blue)
        textRect = text.get_rect()
        textRect.topleft = (10, 20)

        return (text, textRect)
