import pygame
import random

class StarField(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.__stars = []
        for _ in range(100):
            x = random.randint(0, 1024)
            y = random.randint(0, 768)
            speed = random.randint(50, 200)
            self.__stars.append([x, y, speed])

    def update(self, dt):
        for star in self.__stars:
            star[1] += star[2] * dt  

    def draw(self, surface):
        for star in self.__stars:
            pygame.draw.circle(surface, (255, 255, 255), (int(star[0]), int(star[1])), 2)
    