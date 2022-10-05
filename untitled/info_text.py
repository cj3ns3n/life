import pygame

class InfoText():
    def __init__(self):
        green = (0, 255, 0)
        blue = (0, 0, 128)

        font = pygame.font.Font(None, 18)
        self.text = font.render('Generation', True, green, blue)
        self.textRect = self.text.get_rect()
        self.textRect.center = (35, 10)
    #end def

    def getText(self):
        return (self.text, self.textRect)