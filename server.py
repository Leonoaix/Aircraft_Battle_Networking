import socket
import select
from game import Game
import pickle
import time
from Config import COUNTDOWN


serverIP = '10.35.20.154'
serverPort = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(False)
server.bind((serverIP, serverPort))
server.listen()
print('ready for connection')

# this array contains all the sockets that paid attention to
inputs = [server, ]
# record the information of the game
game_info = Game()
# bind the player with its ID
players = {}
# shows the current available ID
current_id = 0
start_time = None


while True:
    r, w, e = select.select(inputs, [], [], 0.05)
    for sock in r:
        # if there's a new client connection
        if sock == server:
            conn, addr = server.accept()
            print('Accept a player')
            players[conn] = current_id
            if current_id == 1:
                game_info.state = 'preparing'
                start_time = time.perf_counter()
                print('game started')
            conn.send(str(current_id).encode())
            inputs.append(conn)
            current_id = (current_id + 1) % 2
            print('id send')
        # if there's an update information for a client
        else:
            data = sock.recv(4096)
            # print(game_info.state)
            if data:
                data = pickle.loads(data)
                if game_info.state == 'preparing':
                    current_time = time.perf_counter()
                    elapsed_time = current_time - start_time
                    data.remaining_time = COUNTDOWN - elapsed_time + 1
                    if data.remaining_time < 1:
                        game_info.state = 'playing'
                elif game_info.state == 'playing':
                    playerId = players[sock]
                    game_info.player_pos[playerId] = data.player_pos
                    game_info.bullet_pos[playerId] = data.bullet_pos
                    game_info.magazines[playerId] = data.magazine
                    if not data.survive:
                        game_info.state = 'game over'
                        game_info.win = (playerId + 1) % 2
                        data.win = game_info.win
                    data.player_pos = game_info.player_pos[(playerId + 1) % 2]
                    data.bullet_pos = game_info.bullet_pos[(playerId + 1) % 2]
                    data.magazine = game_info.magazines[(playerId + 1) % 2]
                elif game_info.state == 'game over':
                    data.win = game_info.win
                data.state = game_info.state
                sock.send(pickle.dumps(data))
            # if a client disconnects
            else:
                if game_info.state != 'game over':
                    game_info.state = 'game over'
                    game_info.win = (players[sock]+1) % 2
                elif len(inputs) == 2:
                    # print("second player is out")
                    del game_info
                    game_info = Game()
                print('player disconnect ', players[sock])
                sock.close()
                inputs.remove(sock)
                # print(len(inputs))
                del players[sock]




