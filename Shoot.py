import pygame
import math
from Config import WINDOW_HEIGHT, WINDOW_WIDTH


class Bullet:
    def __init__(self, image_path, pos_x, pos_y, angle, speed):
        self.speed = speed
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.mask = self.image.get_masks()
        self.rect.center = (pos_x, pos_y)
        self.angle = angle
        self.image = pygame.transform.rotate(self.image, self.angle)

    # move bullet to the angle direction
    def update(self):
        self.rect.centerx += math.cos(self.angle) * self.speed
        self.rect.centery -= math.sin(self.angle) * self.speed
        
        
class Bullet_group:
    def __init__(self, surface):
        self.bullets = []
        self.surface = surface
    
    def add(self, bullet):
        self.bullets.append(bullet)
    
    def update(self):
        for bullet in self.bullets:
            bullet.update()
            if bullet.rect.top < 0 or bullet.rect.left < 0 or bullet.rect.bottom > WINDOW_HEIGHT or bullet.rect.right > WINDOW_WIDTH:
                self.bullets.remove(bullet)

    def display(self):
        for bullet in self.bullets:
            self.surface.blit(bullet.image, bullet.rect)
