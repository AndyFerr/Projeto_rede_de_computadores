#!/usr/bin/env python3

import socket
import threading
import time
import sys

#######################################################################
#                     Defining functions

def get_nickname():
    """
        gets into a loop until it gets a valid nickname and then returns it
    """
    while True:
        nickname = input("nickname: ")
        if (3 <= len(nickname) <= 10):
            return nickname
        else:
            print("The nickname is invalid. try again.\n")


def nickname_setter():
    global stopping_thread
    global client_socket

    nickname = print("Enter a nicknmame between 3 and 10 characters:\n")

    while True:
        try:
            nickname = get_nickname()
            client_socket.send(f"{nickname}".encode("utf-8"))

            response = client_socket.recv(1024).decode("utf-8")

            if (response == "FALSE"):
                print("This nickname already exists. Try another one!")
            else:
                break
        except:
            print("An unexpected error has occurred. Connection closed!")
            client_socket.close()
            stopping_thread = False
            break


def message_send():
    global stopping_thread
    while True:
        message = input()
        try:
            client_socket.send(message.encode("utf-8"))
            if (message.lower() == r"\close" or message.lower().startswith(r"\close")):
                stopping_thread = False
                break
        except:
            print("An unexpect error has occured. Closing connection!\n")
            sys.exit()


def message_recv():
    while True:
        try:
            message = client_socket.recv(2048).decode("utf-8")
            print(f"{message}\n")
        except:
            print("An unexpect error has occured. Closing connection!\n")
            sys.exit()

#######################################################################
#######################################################################






"""
    set the port number and the server address
"""
server_address = "172.28.189.96"
server_port = 12345
stopping_thread = True

"""
    Create the client socket and connects it to the server
"""
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((server_address, server_port))
except socket.error as msg:
    print(f"Connection error. {msg}\n")
    sys.exit()


# while stopping_thread:

#     nickname_setter()
#     msg = client_socket.recv(1024).decode("utf-8")
#     print(f"{msg}\n")

#     rcv_thread = threading.Thread(target=message_recv)
#     send_thread = threading.Thread(target=message_send)

#     rcv_thread.start()
#     send_thread.start()


nickname_setter()
msg = client_socket.recv(1024).decode("utf-8")
print(f"{msg}\n")

rcv_thread = threading.Thread(target=message_recv)
send_thread = threading.Thread(target=message_send)

rcv_thread.start()
send_thread.start()
