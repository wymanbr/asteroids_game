from player import Player
from collideable import ObjectSpawner
from hud_elements import HudElement
import pygame
from starfield import StarField

class GameManager:
    def __init__(self, engine):
        self.__engine = engine
        self.player = Player(512, 384, self)
        self.__groups = {}
        self.__object_spawner = ObjectSpawner(self)
        self.__score = 0
        self.__time = 0.0
        self.__elapsed_time = 0.0
        self.speed_multiplier = 1.0
        self.__hud_font = pygame.font.Font(None, 36)

        self.__setup_groups()
        self.__setup_hud()

    def __setup_groups(self):
        
        self.add_group('all')
        self.add_group('enemies')
        self.add_group('projectiles')
        self.add_group('powerups')
        self.__groups['starfield'] = StarField()
        
        self.add_object(self.player)
        self.add_object(self.__object_spawner)

    def __setup_hud(self):
        self.__score_hud = HudElement("Score: 0", self.__hud_font, (100, 20))
        self.__time_hud = HudElement("Time: 0", self.__hud_font, (400, 20))
        self.__health_hud = HudElement("Health: 100", self.__hud_font, (700, 20))
        self.__lives_hud = HudElement("Lives: 3", self.__hud_font, (900, 20))
        self.add_object(self.__score_hud)
        self.add_object(self.__time_hud)
        self.add_object(self.__health_hud)
        self.add_object(self.__lives_hud)

    def get_score(self):
        return self.__score
    
    def add_to_score(self, points):
        if isinstance(points, int) and points > 0:
            self.__score += points
            

    def get_speed_multiplier(self):
        return self.speed_multiplier
    
    def get_time(self):
        return self.__time
    
    def add_group(self, group):
        self.__groups[group] = pygame.sprite.Group()
    
    def get_group(self, group):
        return self.__groups.get(group, pygame.sprite.Group())
    
    def add_object(self, obj, group='all'):
        if group not in self.__groups:
            self.add_group(group)
        self.__groups[group].add(obj)
    
    def clear_enemies(self):
        for i in self.__groups.get('enemies', []):
            i.kill()

    def update(self, dt):
        self.__time += dt
        self.__time_hud.change_text(f"Time: {self.__time:.2f}")
        self.__health_hud.change_text(f"Health: {self.player.get_health()}")
        self.__lives_hud.change_text(f"Lives: {self.player.get_lives()}")
        self.__score_hud.change_text(f"Score: {self.__score}")

        self.__elapsed_time += dt
        if self.__elapsed_time >= 10.0:
            self.__elapsed_time -= 10.0
            self.speed_multiplier += 0.1
        if self.player.get_lives() < 0:
            self.__engine.running = False