#!/usr/bin/env python3

import socket
import threading
import time
import sys
import os

#######################################################################
#                     Defining functions

import os

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_nickname():
    """
        gets into a loop until it gets a valid nickname and then returns it
    """
    while True:
        nickname = input("nickname: ")
        if (3 <= len(nickname) <= 10):
            return nickname
        else:
            clear_terminal()
            print("The nickname is invalid. try again.\n")
            time.sleep(2)
            clear_terminal()


def nickname_setter():
    global stopping_thread
    global client_socket

    

    while not stopping_thread:
        nickname = print("Enter a nicknmame between 3 and 10 characters:\n")
        try:
            nickname = get_nickname()
            client_socket.send(f"{nickname}".encode("utf-8"))

            response = client_socket.recv(1024).decode("utf-8")

            if (response == "FALSE"):
                clear_terminal()
                print("This nickname already exists. Try another one!")
                time.sleep(2)
                clear_terminal()
            else:
                clear_terminal()
                break
        except:
            print("An unexpected error has occurred. Connection closed!")
            client_socket.close()
            stopping_thread = True
            break


def message_send():
    global stopping_thread
    while not (stopping_thread):
        print("\n")
        message = input()
        try:
            client_socket.send(message.encode("utf-8"))
            if (message.lower() == r"/close" or message.lower().startswith(r"/close")):
                stopping_thread = True
                break
        except:
            print("An unexpect error has occured. Closing connection!\n")
            client_socket.close()
            stopping_thread = True


def message_recv():
    global stopping_thread
    while not (stopping_thread):
        try:
            message = client_socket.recv(2048).decode("utf-8")
            
            print(f"{message}\n")
        except:
            print("An unexpect error has occured. Closing connection!\n")
            client_socket.close()
            stopping_thread = True

#######################################################################
#######################################################################






"""
    set the port number and the server address
"""
server_address = "192.168.112.1"
server_port = 12345
stopping_thread = False

"""
    Create the client socket and connects it to the server
"""
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((server_address, server_port))
    print(f"Connected to {server_address} : {server_port}\n")
except socket.error as msg:
    print(f"Connection error. {msg}\n")
    sys.exit()

nickname_setter()
msg = client_socket.recv(1024).decode("utf-8")
print(f"{msg} Type '/close' to leave the chat.\n")
rcv_thread = threading.Thread(target=message_recv)
send_thread = threading.Thread(target=message_send)

rcv_thread.start()
send_thread.start()


while True:
    if not (stopping_thread):
        pass
    else:
        client_socket.close()
        sys.exit(
            "Connection closed!\n"
        )
        
