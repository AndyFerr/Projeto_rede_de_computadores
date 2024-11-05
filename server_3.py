import socket
import threading
import time
import sys

#######################################################################
#                     Defining functions

def broadcast_msg(message, clientSender):
    for client in clients_sockets:
        if (client != clientSender):
            client.send(message.encode("utf-8"))


def recv_message(client):

    """
        recieve the message from anyone who is in the chat,
        verify if it's the key message to exit the chat and if not, send it to everybody
        if it is, remove the user from the chat group
    """

    client_indexing = clients_sockets.index(client)
    nickname = clients_nicknames[client_indexing]

    while True:
        try:
            message = client.recv(2048).decode("utf-8")
            
            if message == r"\close":
                clients_sockets.remove(client)
                clients_addresses.remove(client_indexing)
                clients_nicknames.remove(nickname)

                msg = (f"{nickname} disconnected!")

                broadcast_msg(msg, client)

                break
            else:
                msg = f"{nickname}: {message}\n"
                broadcast_msg(msg, client)
        except:
            print("An unexpect error has occured at the rcv msg!")
            sys.exit()
            
#######################################################################




"""
    define the port and gets the host ip
"""

port = 12345
host = "0.0.0.0"

"""
    Defnine 4 lists to be managed by the threading
"""
clients_sockets = []
clients_nicknames = []
clients_addresses = []
nicknames = []
threads_list = []


"""
    creates the server socket and binds it to the host and the port previously defined
"""
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen()
print(f"server listening at port: {port}...")


while True:
    client, address = server_socket.accept()
    print(f"A connection has been established with {str(address)}\n\n")


    while True:
        try:
            client_nickname = client.recv(1024).decode("utf-8")
            
            if (client_nickname in nicknames):
                client.send("FALSE".encode("utf-8"))
            else:
                client.send("TRUE".encode("utf-8"))
                break
        except:
            print("An unexpect error has occured! Closing connection")
            client.close()
    
    client.send(f"Welcome to the server {client_nickname}!\n".encode("utf-8"))
    
    clients_nicknames.append(client_nickname)
    clients_sockets.append(client)
    clients_addresses.append(address)

    recv_send_messages_clients = threading.Thread(target=recv_message, args=[client])
    recv_send_messages_clients.start()
    # threads_list.append(recv_send_messages_clients)
    
