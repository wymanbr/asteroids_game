import pygame


class HudElement(pygame.sprite.Sprite):
    def __init__(self, text, font, pos, color=(255,255,255)):
        super().__init__()
        self.__font = font
        self.__color = color
        self.__pos = pos
        self.__text = text
        self.image = self.__font.render(text, True, self.__color)
        self.rect = self.image.get_rect(center=pos)

    def update(self, dt):
        self.image = self.__font.render(self.__text, True, (255, 255, 255))
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def change_text(self, text):
        if not self.__text:
            return
        self.__text = text
