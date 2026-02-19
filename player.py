
import pygame
from collideable import PowerupType, UtilityFunctions


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, manager):
        super().__init__()
        self.__assets = {}
        self.__load_assets()
        self.image = self.__assets['regular_image']
        self.rect = self.image.get_rect(center=(x, y))

        self.__manager = manager
        self.__movement_speed = 250
        self.__movement_multiplier = .125
        self.__x_velocity = 0
        self.__y_velocity = 0
        self.__health = 100
        self.__lives = 3
        self.__shield = False
        self.__invincible = False
        self.__invincible_timer = 0.0
        self.__shot_timer = 0.0

    def __load_assets(self):
        # Load images
        self.__assets['regular_image'] = pygame.image.load("./assets/ship.png").convert_alpha()
        self.__assets['shielded_image'] = pygame.image.load("./assets/shielded_ship.png").convert_alpha()
        self.__assets['invincible_image'] = pygame.image.load("./assets/ship2.png").convert_alpha()
        # Load sound effects
        self.__assets['sfx_fire'] = pygame.mixer.Sound("./assets/sfx_laser1.ogg")
        self.__assets['sfx_damage'] = pygame.mixer.Sound("./assets/sfx_twoTone.ogg")

    def update(self, dt):
        self.__shot_timer += dt
        if self.__invincible == True:
            self.__invincible_timer += dt
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if self.__x_velocity > -self.__movement_speed:
                self.__x_velocity -= self.__movement_speed * self.__movement_multiplier
        if keys[pygame.K_RIGHT]:
            if self.__x_velocity < self.__movement_speed:
                self.__x_velocity += self.__movement_speed * self.__movement_multiplier
        if keys[pygame.K_UP]:
            if self.__y_velocity > -self.__movement_speed:
                self.__y_velocity -= self.__movement_speed * self.__movement_multiplier
        if keys[pygame.K_DOWN]:
            if self.__y_velocity < self.__movement_speed:
                self.__y_velocity += self.__movement_speed * self.__movement_multiplier
        if keys[pygame.K_SPACE]:
            if self.__shot_timer > .25:
                self.__shot_timer = 0.0
                Laser = PlayerLaser(self.rect.centerx,self.rect.centery - 20)
                self.__manager.add_object(Laser)
                self.__manager.add_object(Laser, 'projectiles')
                self.__assets['sfx_fire'].play()

        self.rect.x += self.__x_velocity * dt
        self.rect.y += self.__y_velocity * dt

        # Collision with an enemy code
        hits = pygame.sprite.spritecollide(self, self.__manager.get_group('enemies'), False)
        if hits:
            if self.__shield:
                self.__shield = False
                self.image = self.__assets['regular_image']
            elif not self.__invincible:
                self.__health -= 10
                if self.__health <= 0:
                    self.__lives -= 1
                    self.__health = 100
            hits[0].kill()
            self.__assets['sfx_damage'].play()
        # PUT NEW CODE BELOW HERE

        

        if not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
            self.__x_velocity *= 0.9
            if abs(self.__x_velocity) < 1:
                self.__x_velocity = 0
        if not (keys[pygame.K_UP] or keys[pygame.K_DOWN]):
            self.__y_velocity *= 0.9
            if abs(self.__y_velocity) < 1:
                self.__y_velocity = 0

        self.rect.x += self.__x_velocity * dt
        self.rect.y += self.__y_velocity * dt

        
        if not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
            self.__x_velocity *= 0.9
            if abs(self.__x_velocity) < 1:
                self.__x_velocity = 0
        if not (keys[pygame.K_UP] or keys[pygame.K_DOWN]):
            self.__y_velocity *= 0.9
            if abs(self.__y_velocity) < 1:
                self.__y_velocity = 0

        self.rect.x = UtilityFunctions.clamp(self.rect.x, 0, 1024 - self.rect.width)
        self.rect.y = UtilityFunctions.clamp(self.rect.y, 0, 768 - self.rect.height)

        hits = pygame.sprite.spritecollide(self, self.__manager.get_group('powerups'), False)
        if hits:
            pwr_type = hits[0].get_type()
            if pwr_type == PowerupType.CLEAR:
                self.__manager.clear_enemies()
            elif pwr_type == PowerupType.HEALTH:
                self.__health += 100
            elif pwr_type == PowerupType.SHIELD:
                self.image = self.__assets['shielded_image']
                self.__shield = True
            elif pwr_type == PowerupType.INVINCIBLE:
                self.__invincible = True
                self.__invincible_timer = 0.0
                self.image = self.__assets['invincible_image']
            hits[0].kill()

        if self.__invincible_timer > 30.0:
            self.__invincible_timer -= 30.0
            self.__invincible = False
            self.image = self.__assets['regular_image']


    def get_invincible(self):
        return self.__invincible
    
    def get_health(self):
        return self.__health
    
    def get_lives(self):
        return self.__lives


class PlayerLaser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("./assets/playerLaser.png").convert_alpha()  # preserves transparency
        self.rect = self.image.get_rect(center=(x, y))
        self.__speed = 1000

    def update(self, dt):
        self.rect.y -= self.__speed * dt

        if self.rect.y < 0:
            self.kill()