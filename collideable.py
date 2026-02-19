from enum import Enum
import random
import math
import pygame


class UtilityFunctions:
    @staticmethod
    def move_straight(enemy, dt):
        enemy.rect.y += enemy.get_speed() * dt

    @staticmethod
    def move_sine(enemy, dt):
        enemy.rect.y += enemy.get_speed() * dt
        enemy.rect.x += math.sin(pygame.time.get_ticks() * 0.005)

    @staticmethod
    def move_zigzag(enemy, dt):
        enemy.rect.y += enemy.get_speed() * dt

        # this checks if there is a 'start_x' attribute and 
        # since theres not it will set the stating point
        if not hasattr(enemy, 'start_x'):
            enemy.start_x = enemy.rect.x
        if not hasattr(enemy, 'zigzag_dir'):
            enemy.zigzag_dir = 1

        enemy.rect.x += 100 * dt * enemy.zigzag_dir

        if enemy.rect.x < enemy.start_x - 100:
            enemy.zigzag_dir = 1
        elif enemy.rect.x > enemy.start_x + 100:
            enemy.zigzag_dir = -1

        

    @staticmethod
    def clamp(value, min_value, max_value):
        """Clamp a value.  Give a number, a minimum and a
        maximum, return either the minimum (if the value is too low),
        the maximum (if the value is too high), or the value (if it is
        within the bounds of min-max).

        @param value - the value we wish to check
        @param min_value - the minimum number we expect back
        @param max_value - the maximum number we expect back

        @return the clamped value
        """
        if value < min_value:
            return min_value
        elif value > max_value:
            return max_value
        else:
            return value


class ObjectSpawner(pygame.sprite.Sprite):
    def __init__(self, manager):
        super().__init__()
        self.__manager = manager
        self.image = pygame.Surface((1, 1), pygame.SRCALPHA)  # invisible
        self.rect = pygame.Rect(0, 0, 0, 0)  # only rect, no image
        self.__enemy_images = ["enemyBlack1.png", 
                        "enemyBlue4.png",  
                        "enemyGreen3.png", 
                        "enemyRed1.png"]
        self.__asteroid_images = ["meteorGrey_big1.png", 
                        "meteorGrey_big2.png", 
                        "meteorGrey_big3.png", 
                        "meteorGrey_big4.png",
                        "meteorGrey_med1.png", 
                        "meteorGrey_med2.png",
                        "meteorGrey_small1.png",
                        "meteorGrey_small2.png",
                        "meteorGrey_tiny1.png",
                        "meteorGrey_tiny2.png"]
        self.__powerup_images = ["powerupYellow_bolt.png", 
                        "powerupYellow_shield.png",
                        "powerupYellow_star.png",
                        "powerupYellow.png"]
        self.__movement_functions = [UtilityFunctions.move_straight, UtilityFunctions.move_sine, UtilityFunctions.move_zigzag]
        self.__enemy_time = 0
        self.__powerup_time = 0
    
    def update(self, dt):
        self.__enemy_time += dt
        self.__powerup_time += dt
        if self.__enemy_time > 1.0:
            self.__enemy_time -= 1.0
            choose_ship = random.choice([True, False])
            if choose_ship:
                new_ship = EnemyShip((random.randint(0, 1024),0), './assets/' + random.choice(self.__enemy_images), random.choice(self.__movement_functions), self.__manager)
                self.__manager.add_object(new_ship)
                self.__manager.add_object(new_ship, 'enemies')
            else:
                new_meteor = Asteroid((random.randint(0, 1024), 0), './assets/' + random.choice(self.__asteroid_images), self.__manager)
                self.__manager.add_object(new_meteor)
                self.__manager.add_object(new_meteor, 'enemies')
        if self.__powerup_time > 30.0:
            self.__powerup_time -= 30.0
            powerupType = random.choice(list(PowerupType)) 
            powerup = Powerup((random.randint(0, 1024), 0), './assets/' + self.__powerup_images[powerupType.value], powerupType)
            self.__manager.add_object(powerup)
            self.__manager.add_object(powerup, 'powerups')
        

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, pos, image, manager):
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.__manager = manager
        self.__speed = random.randint(100, 1000)

    def get_speed(self):
        return self.__speed

    def update(self, dt):
        self.rect.y += self.__speed * dt
        if self.rect.y > 768:
            self.kill()
        hits = pygame.sprite.spritecollide(self, self.__manager.get_group('projectiles'), False)
        if hits:
            hits[0].kill()


class EnemyShip(pygame.sprite.Sprite):
    def __init__(self, pos, image, movement_function, manager):
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.__manager = manager
        self.__movement_function = movement_function
        self.__speed = random.randint(100, 500)
        self.__explosion_sfx = pygame.mixer.Sound("./assets/explosion.wav")

    def get_speed(self):
        return self.__speed
    
    def update(self, dt):
        self.__movement_function(self, dt)
        if self.rect.y > 768:
            self.kill()
        hits = pygame.sprite.spritecollide(self, self.__manager.get_group('projectiles'), False)
        if hits:
            for proj in hits:
                proj.kill()                      
            self.__manager.add_to_score(100)     
            self.kill()                         
            sfx = getattr(self, '_EnemyShip__explosion_sfx', None)
            if sfx:
                sfx.play()

class PowerupType(Enum):
    CLEAR = 0
    SHIELD = 1
    INVINCIBLE = 2
    HEALTH = 3


class Powerup(pygame.sprite.Sprite):
    def __init__(self, pos, image, type):
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.__type = type
        self.__speed = 100

    def update(self, dt):
        self.rect.y += self.__speed * dt
        if self.rect.y > 768:
            self.kill()

    def get_speed(self):
        return self.__speed
    
    def get_type(self):
        return self.__type
