import pickle
import socket
from game import Info_send
# import time
import pygame
import Config
from BG import Background
from Plane import Player, Plane
from Shoot import Bullet_group, Oppo_bullets

pygame.init()
window = pygame.display.set_mode((Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT))
pygame.display.set_caption(Config.GAME_NAME)

# set background
background = Background(Config.BACKGROUND_PATH, Config.BACKGROUND_SPEED)

# set player
player = Player(Config.PLAYER_PATH, Config.PLAYER_SPEED, window)
# player.setStyle(False)
player_bullet = Bullet_group(window, Config.BULLET_PATH, Config.BULLET_SPEED)

# set player's bullets
# bullets =

# set enemy player
opponent = Plane(Config.OPPONENT_PATH, window)
opponent.rect.center = (Config.PLAYER_INIT_X, Config.WINDOW_HEIGHT - Config.PLAYER_INIT_Y)
opponent_bullets = Oppo_bullets(Config.OPPONENT_BULLETS_PATH, window)

# set server information
serverIP = '10.35.20.154'
serverPort = 5555

# set client socket information
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((serverIP, serverPort))
# playerId = None
playerId = int(client_socket.recv(2048).decode())
info = Info_send()

# set clock
clock = pygame.time.Clock()

# set font
font = pygame.font.Font(Config.FONT_PATH, Config.FONT_SIZE)

run = True

print('game started')
while run:
    # command = input("enter 'start' to join the game: ")
    # if command == 'start':
        # client_socket.connect((serverIP, serverPort))
        # playerId = int(client_socket.recv(2048).decode())
        # info = Info_send()
        # print('game started')
        # while True:
    # time.sleep(1/3)
    # display background
    background.display(True, window)
    clock.tick(Config.FRAMES)
    client_socket.send(pickle.dumps(info))
    info = pickle.loads(client_socket.recv(4096))
    if info.state == 'preparing':
        # print(int(info.remaining_time))
        # display the countdown for game start
        text = font.render(str(int(info.remaining_time)), True, 'white')
        window.blit(text, (0, 0))
    elif info.state == 'playing':
        # show magazine size
        text = font.render('player: ' + str(player_bullet.magazine), True, 'white')
        window.blit(text, (0, 0))
        text = font.render('opponent: ' + str(info.magazine), True, 'white')
        window.blit(text, (0, Config.FONT_SIZE + 5))
        # update player's position
        player.update()
        # update player's bullets
        player_bullet.update(player.rect.centerx, player.rect.centery)
        # update opponent's position
        opponent.rect.centerx = info.player_pos
        # update opponent's bullets
        opponent_bullets.loads(info.bullet_pos)
        # load magazine
        info.magazine = player_bullet.magazine
        # detect collision
        info.survive = opponent_bullets.collision(player.mask, player.rect)
        # load player's position
        info.player_pos = player.rect.centerx
        # load player's bullets
        info.bullet_pos = player_bullet.get_pos()

        # print('enemy information: ', info.player_pos)
        # info.player_pos = input("enter the player's position (type 'quit' to quit the game): ")
        # if info.player_pos == 'quit':
        #     run = False
    elif info.state == 'game over':
        # print(info.win)
        # print(playerId)
        if info.win == playerId:
            print('you win')
        else:
            print('you lost')
        run = False
    # display player
    player.display()
    player_bullet.display()
    opponent.display()
    opponent_bullets.display()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
client_socket.close()
        # client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)