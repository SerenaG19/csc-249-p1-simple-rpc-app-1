#!/usr/bin/env python3
# server program
#
# Serena Geroe
#
# Listens for and receives a message from the client. Returns a response to the client's instruction/inquiry.

import socket
import random

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

def digital_palette(instruction):
    '''
    A function that can either 'blend' or 'choose,' given two primary colors, and includes error handling for 
    invalid inouts.

    :param param: (String): The string-version of the message sent by the
         client and received by the server.
    :return server_reply: (String) The server's reply, to be sent to the client.
   
    '''
    primary_colors = ["red","yellow","blue"] # define a list of primary colors; these are the only possible valid inputs for nouns one and two
    instruction_list = instruction.split(",") #parse the client's instructions based on a comma delimeter
    print("instruction list:" ,  instruction_list, ", length: ", len(instruction_list), "\n") # verify in terminal client instruction
    
    if len(instruction_list) == 3: # first, set these values to assist with error handling -- but only if there are three arguments in
                                    # the client's instruction
        verb = instruction_list[0] # identify the verb of the instruction
        noun_one = instruction_list[1] # identify the first color from the instruction
        noun_two = instruction_list[2] # identify the second color from the instruction

        print("verb is", verb, ", color 1 is", noun_one, ", color 2 is" , noun_two, "\n") # verify in terminal client instruction

        # invalid verb
        if (verb != "blend") and (verb != "choose"):
            server_reply = "Invalid input: unrecognized operation. Verb is neither 'blend' nor 'choose.'"
            return server_reply
        # invalid nouns
        if (noun_one not in primary_colors) or (noun_two not in primary_colors):
            server_reply = "Invalid input: unrecognized colors. You did not enter both colors to be primary colors (red, yellow, or blue)."
            return server_reply
        # two colors are the same
        if (noun_one == noun_two):
            server_reply = "Invalid input: redundant colors. Please enter two different primary colors."
            return server_reply
            
        # digital palette computations to generate server output
        if verb == "blend":
            if (noun_one == "red" or noun_one == "yellow") and (noun_two == "red" or noun_two == "yellow"):
                server_reply = "orange"
            elif (noun_one == "yellow" or noun_one == "blue") and(noun_two == "yellow" or noun_two == "blue"):
                server_reply = "green"
            else: server_reply = "violet"
        else: # choose, by process of elimination (sinse the verb is either blend or choose, and it is not blend)
            rand_num_decider = random.randint(1,10) * random.randint(2,11)
            # print("Random number decider:" , str(rand_num_decider))
            if (rand_num_decider % 2) == 0:
                server_reply = noun_one
            else: server_reply = noun_two

        return server_reply

    # too few arguments, likely due to incorrect delimeter
    elif len(instruction_list) < 3: 
        server_reply = "Invalid input: too few arguments. Ensure use of comma delimeter. Please enter three arguments separated by commas (1 verb and two colors)."
        return server_reply
    # too many arguments
    else:
        server_reply = "Invalid input: too many arguments. Please enter three arguments separated by commas (1 verb and two colors)."
        return server_reply
    

# run the code!
if __name__ == "__main__":
    print("\nInitiating connection to client - listening for connections at IP", HOST, "and port", PORT, " \n")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: #creates socket object with address family AF_INET and socket type SOCK_STREAM
        s.bind((HOST, PORT)) # associates the socket with the particular desired network interface and port number
        s.listen() # enables the server to accept connections; also accounts for the server's backlogged connections (ones that haven't yet been accepted)
        conn, addr = s.accept() # accept() blocks execution and waits for an incoming connection
        with conn: # once a connection is made with the client, a new socket object is returned from accept() (different socket from the listening socket)
            print(f"Established connection, {addr}\n")
            while True: # infinite while loop to loop over blocking calls to conn.recv()
                data = conn.recv(1024)
                data_string = data.decode('utf-8')
                # print(data_string)
                if not data:
                    break # if conn.recv() returns an empty bytes object, the server knows the client closed the connection
                print(f"Received client message: '{data!r}' [{len(data)} bytes] \n") # print client message
                reply = digital_palette(data_string) # set the server's reply equal to the output of the digital_palette function
                print("Digital Palette program output:" , reply, "\n")
                reply_byte = reply.encode('utf-8') # encode the digital_palette's reply to be type byte instead of a string
                print("Sending output '", reply, "' back to client \n")
                conn.sendall(reply_byte) # send server response to the client
            
    print("Server job complete!\n")