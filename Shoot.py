import pygame
from Config import FRAMES


class Bullet:
    def __init__(self, image_path, pos_x, pos_y):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (pos_x, pos_y)


class Bullet_group:
    def __init__(self, surface: pygame.Surface, image_path, speed):
        self.bullets = []
        self.surface = surface
        self.speed = speed
        self.image_path = image_path
        self.clicked = False
        self.magazine = 10
        self.count = 0

    # if the user pressed the mouse, create a new bullet. update all bullets' positions.
    def update(self, plane_x, plane_y):
        mouse_pressed = pygame.mouse.get_pressed()
        self.count += 1
        if self.count == 4*FRAMES:
            self.count = 0
            self.magazine += 1
        if self.magazine > 0:
            if mouse_pressed[0] and not self.clicked:
                self.clicked = True
                self.create_bullet(plane_x, plane_y)
                self.magazine -= 1
            if not mouse_pressed[0] and self.clicked:
                self.clicked = False
        for bullet in self.bullets:
            bullet.rect.centery -= self.speed
            if bullet.rect.top < 0 or bullet.rect.left < 0 or \
                    bullet.rect.bottom > self.surface.get_height() or bullet.rect.right > self.surface.get_width():
                self.bullets.remove(bullet)

    def display(self):
        for bullet in self.bullets:
            self.surface.blit(bullet.image, bullet.rect)

    def create_bullet(self, x, y):
        self.bullets.append(Bullet(self.image_path, x, y))

    # return every bullets' positions in [x, y]
    def get_pos(self):
        ret = []
        for bullet in self.bullets:
            ret.append([bullet.rect.centerx, bullet.rect.centery])
        return ret


class Oppo_bullets:
    def __init__(self, image_path, surface: pygame.Surface):
        self.bullets = []
        self.image_path = image_path
        self.surface = surface

    def loads(self, bullet_pos):
        self.bullets.clear()
        for pos in bullet_pos:
            self.bullets.append(Bullet(self.image_path, pos[0], self.surface.get_height()-pos[1]))

    def display(self):
        for bullet in self.bullets:
            self.surface.blit(bullet.image, bullet.rect)

    def collision(self, player_mask: pygame.mask.Mask, player_rect: pygame.Rect):
        for bullet in self.bullets:
            offset_x = bullet.rect.x - player_rect.left
            offset_y = bullet.rect.y - player_rect.top
            if player_mask.overlap(bullet.mask, (offset_x, offset_y)):
                return False
        return True
