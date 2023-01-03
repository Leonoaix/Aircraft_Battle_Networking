import pygame
import Config
from Shoot import Bullet


class Plane:
    def __init__(self, image_path: str):
        self.image = pygame.image.load(image_path).convert()
        self.rect = self.image.get_rect()

    def display(self, surface):
        surface.blit(self.image, self.rect)


class Player(Plane):
    def __init__(self, image_path: str, speed: int):
        Plane.__init__(self, image_path)
        self.speed = speed
        # initialization
        self.rect.center = (Config.PLAYER_INIT_X, Config.PLAYER_INIT_Y)
        # Set controlling style, mouse_control: True, keyboard_control: False
        self.control_style = True

    # update position
    def update(self):
        if self.control_style:
            self.mouse_move(pygame.mouse.get_pos())
        else:
            self.keyboard_move(pygame.key.get_pressed())

    # mouse controlled movement
    def mouse_move(self, mouse_pos):
        self.rect.center = mouse_pos
        self.__adjustment()

    # keyboard controlled movement
    def keyboard_move(self, keys):
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        self.__adjustment()

    # prevent the plane move outside the screen
    def __adjustment(self):
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > Config.WINDOW_HEIGHT:
            self.rect.bottom = Config.WINDOW_HEIGHT
        if self.rect.right > Config.WINDOW_WIDTH:
            self.rect.right = Config.WINDOW_WIDTH

    def changeStyle(self, mouseStyle):
        self.control_style = mouseStyle

    def create_bullet(self, image_path, angle, speed):
        return Bullet(image_path, self.rect.centerx, self.rect.centery, angle, speed)