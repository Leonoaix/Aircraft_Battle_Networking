import math

import pygame
from Config import *
from BG import Background
from Plane import Player
from Shoot import Bullet_group

# Initialize pygame
pygame.init()

# Set window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Set icon
icon = pygame.image.load(ICON_PATH).convert()
pygame.display.set_icon(icon)

# Set game name
pygame.display.set_caption(GAME_NAME)

# Set frame control
clock = pygame.time.Clock()


class GameState:
    def __init__(self):
        self.currentState = None

    def update(self):
        if self.currentState:
            self.currentState.update()

    def trigger(self):
        if self.currentState:
            self.currentState.trigger()

    def changeState(self, newState):
        self.currentState = newState

    def display(self, surface):
        if self.currentState:
            self.currentState.display(surface)


class GameplayState:
    def __init__(self):
        self.background = Background(BACKGROUND_PATH, BACKGROUND_SPEED)
        # create player sprite group
        self.player = Player(PLAYER_PATH, PLAYER_SPEED)
        self.player_bullet = Bullet_group(window)
        self.magazine_size = MAGAZINE_SIZE

    # Location updates for objects already on the window
    def update(self):
        self.player.update()
        self.player_bullet.update()

    # updating for events that need click to trigger
    def trigger(self):
        if self.magazine_size > 0:
            self.player_bullet.add(self.player.create_bullet(BULLET_PATH, math.pi/2, BULLET_SPEED))
            self.magazine_size -= 1

    def display(self, surface):
        self.background.display(True, surface)
        self.player_bullet.display()
        self.player.display(surface)


# GameState control
game_state = GameState()
gameplay_state = GameplayState()

# change state to gameplay state
game_state.changeState(gameplay_state)


# Main loop
run = True
while run:
    clock.tick(FRAMES)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            game_state.trigger()
    game_state.update()
    game_state.display(window)
    pygame.display.update()
