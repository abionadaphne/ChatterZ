import select, socket, sys, pdb
from pychat_util import Hall, Room, Player
import pychat_util

READ_BUFFER = 4096

hostname = socket.gethostname()
IP=socket.gethostbyname(hostname) 
port=7010
listen_sock = pychat_util.create_socket((IP, port))

hall = Hall()
connection_list = []
connection_list.append(listen_sock)

while True:
    # Player.fileno()
    read_players, write_players, error_sockets = select.select(connection_list, [], [])
    for player in read_players:
        if player is listen_sock: # new connection, player is a socket
            new_socket, add = player.accept()
            new_player = Player(new_socket)
            connection_list.append(new_player)
            hall.welcome_new(new_player)

        else: # new message
            msg = player.socket.recv(READ_BUFFER)
            if msg:
                msg = msg.decode().lower()
                hall.handle_msg(player, msg)
            else:
                player.socket.close()
                connection_list.remove(player)

    for sock in error_sockets: # close error sockets
        sock.close()
connection_list.remove(sock)
