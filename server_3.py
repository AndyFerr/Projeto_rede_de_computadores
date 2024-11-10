#!/usr/bin/env python3

import socket
import threading
import os

#######################################################################
#                     Defining functions

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def broadcast_msg(message, clientSender):
    """
        send the message received from clientSender to all the clients on the server
        except for the clientSender himself
    """
    for client in clients_sockets:
        if (client != clientSender):
            client.send(message.encode("utf-8"))


def recv_message(client):

    """
        recieve the message from anyone who is in the chat,
        verify if it's the key message to exit the chat and if not, send it to everybody
        if it is, remove the user from the chat group
    """
    global stop_threading


    while (not stop_threading):

        try:
            message = client.recv(2048).decode("utf-8")

            client_indexing = clients_sockets.index(client)
            nickname = clients_nicknames[client_indexing]

            if message == "/close":

                print(f"{clients_addresses[client_indexing]} has been disconnected\n")
                clients_addresses.remove(clients_addresses[client_indexing])
                clients_sockets.remove(client)
                clients_nicknames.remove(nickname)

                msg = (f"{nickname} disconnected!")

                broadcast_msg(msg, client)
                client.close()
                stop_threading = True

                break
            else:
                msg = f"{nickname}: {message}\n"
                broadcast_msg(msg, client)
        except:
            
            client_indexing = clients_sockets.index(client)
            nickname = clients_nicknames[client_indexing]
            
            print(f"An unexpect error has occured at the rcv msg! Closing connection at {clients_addresses[client_indexing]}")
            clients_sockets.remove(client)
            clients_nicknames.remove(nickname)
            clients_addresses.remove(clients_addresses[client_indexing])
            broadcast_msg(f"{nickname} has been disconnected")

            client.close()
            stop_threading = True
            
            
#######################################################################




"""
    define the port and gthe host ip to send it to any connection in the network
"""

port = 12345
host = "0.0.0.0"

"""
    Defnine 4 lists to be managed by the threading and a flag to stop some processes
"""
clients_sockets = []
clients_nicknames = []
clients_addresses = []
nicknames = []

stop_threading = False


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
            nickname = client.recv(1024).decode("utf-8")
            
            if (nickname in clients_nicknames):
                client.send("FALSE".encode("utf-8"))
            else:
                client.send("TRUE".encode("utf-8"))
                break
        except:
            print("An unexpect error has occured! Closing connection")
            client.close()
    if (clients_sockets):
        msg = f"{nickname} joined the chat group!\n"
        broadcast_msg(msg, client)
    client.send(f"Welcome to the group chat {nickname}!".encode("utf-8"))
    
    

    clients_nicknames.append(nickname)
    clients_addresses.append(address)
    clients_sockets.append(client)
    
    client_thread = threading.Thread(target=recv_message, args=[client])
    client_thread.start()
