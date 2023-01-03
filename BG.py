import pygame
import Config


class Background:
    def __init__(self, image_path: str, speed: float):
        self.image1 = pygame.image.load(image_path).convert()
        self.image2 = pygame.image.load(image_path).convert()
        # speed defines how many pixels does the background move every frame
        self.speed = speed
        # pos[0] is x, pos[1] is y
        self.pos1 = [0, 0]
        self.pos2 = [0, -Config.WINDOW_HEIGHT]

    # scrolling indicate whether the background is scrolled
    def display(self, scrolling: bool, window: pygame.Surface):
        if scrolling:
            self.pos1[1] += self.speed
            self.pos2[1] += self.speed
            if self.pos1[1] == Config.WINDOW_HEIGHT:
                self.pos1[1] = -Config.WINDOW_HEIGHT
            if self.pos2[1] == Config.WINDOW_HEIGHT:
                self.pos2[1] = -Config.WINDOW_HEIGHT
            window.blit(self.image1, (self.pos1[0], self.pos1[1]))
            window.blit(self.image2, (self.pos2[0], self.pos2[1]))
        else:
            window.blit(self.image1, (0, 0))
