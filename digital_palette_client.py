#!/usr/bin/env python3
# client
#
# DESCRIPTION

import socket

HOST = "127.0.0.1"  # This is the loopback address
PORT = 65432        # The port used by the server

def client_driver():
    print("Initiating connection to server. IP", HOST, ", Port", PORT)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"Connection established")
        while True:
            # loop until the user asks to quit
            if not talk_to_server(s):
                break

def talk_to_server(sock):
    msg = input("Welcome to the Digital Palette!\n" +
                "What primary colors would you like to blend, or from which two primary colors should I randomly choose?\nPlease enter your input in the following format (excluding the '<>' characters): <blend or choose>,<primary color 1>,<primary color 2>\n")
    if msg == 'quit':
        print("Client quitting per operator request\nExiting the Digital Palette")
        return False
    print(f"Sending message '{msg}' to server")
    sock.sendall(msg.encode('utf-8'))
    print("Message sent, awaiting reply")
    reply = sock.recv(4096)

    if not reply:
        return False
    else:
        print(f"Received server's reply: '{reply}'")
        return reply

if __name__ == "__main__":
    client_driver()
print("End of program\n" +
      "Exiting the Digital Palette")
