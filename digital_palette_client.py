#!/usr/bin/env python3
# client program
#
# Serena Geroe
#
# Prompts user for an instruction, sends instruction to the server, and receives the server's reply

import socket

HOST = "127.0.0.1"  # This is the loopback address
PORT = 65432        # The port used by the server

def client_connect_w_server(): # function that drives the client

    '''
    This function creates a socket object, connects with the server using this socket,
    opens an infinite loop to keep the connection open so the server continues to
    listen for a message from the client, and calls the talk_to_server() function.
    '''

    print("\nInitiating connection to server. IP", HOST, ", Port", PORT,"\n")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # creates the socket object for a specified address and port number
        s.connect((HOST, PORT)) # connects to the server
        print(f"Connection established\n")
        while True: # loop until the user asks to quit
            if not talk_to_server(s): # calls the function to communicate messages with the server
                break

def talk_to_server(sock):
    '''
    This function manages the interfaces between the client and the server, and the (human) user and the client.
    It specifies how to format the instruction input and formats the server's reply.
    Then, it sends the user's message to the server, listens and waits for the server's reply, receives the 
    server's reply, and communicates it with the human user.
    '''
    # welcome message
    msg = input("Welcome to the Digital Palette!\n" +
                "What two different primary colors would you like to blend, or from which two primary colors should I randomly choose?\n" +
                "Please enter your input in the following format (excluding the '<>' characters): " + 
                "<blend or choose>,<primary color 1>,<primary color 2> \n"+
                "Enter quit to exit this program.\n\n")
    if msg == 'quit': # Check whether user seeks to exit the program
        print("\nClient quitting per operator request\n") # Communicate to the user the program is ending
        return False
    print(f"\nSending message '{msg}' to server\n") # print message that is going to be sent to the server
    sock.sendall(msg.encode('utf-8')) # this line (1) encodes the message to be sent to the server to be type byte, and (2)
                                      # sends the message to the server
    print("Message sent, awaiting reply\n")
    reply = sock.recv(1024) # receives the message from the server

    if not reply: # tells the client to keep listening for a reply from the server
        return False
    else:
        print(f"Received server's reply: '{reply}'. Thank you.\n") # communicate the server's reply to the user
        return reply


# run the code! First, run client_connect_w_server(). Then, notify the user the program is ending.
if __name__ == "__main__":
    client_connect_w_server()
print("End of program. Exiting the Digital Palette\n")
