import pygame
from Config import PLAYER_INIT_Y, PLAYER_INIT_X


class Plane:
    def __init__(self, image_path: str, surface: pygame.Surface):
        self.image = pygame.image.load(image_path).convert()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.surface = surface

    def display(self):
        self.surface.blit(self.image, self.rect)


class Player(Plane):
    def __init__(self, image_path: str, speed: int, surface: pygame.Surface):
        Plane.__init__(self, image_path, surface)
        self.speed = speed
        # initialization
        self.rect.center = (PLAYER_INIT_X, PLAYER_INIT_Y)
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
        self.rect.centerx = mouse_pos[0]
        self.__adjustment()

    # keyboard controlled movement
    def keyboard_move(self, keys):
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        self.__adjustment()

    # prevent the plane move outside the screen
    def __adjustment(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.surface.get_width():
            self.rect.right = self.surface.get_width()

    def setStyle(self, mouseStyle):
        self.control_style = mouseStyle


