#!/usr/bin/env python3
# server
#
# DESCRIPTION

import socket
import random

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

server_reply = b""
server_reply_string = ""
rand_num_decider = 0
verb = ""
noun_one = ""
noun_two = ""

def digital_palette(param):
    server_reply_string = ""
    param_string = str(param)
    #print(param_string)
    #print(type(param_string), "sdfghjkjhgfdfghjmk,lkjhgtfdrrftghjmk")
    param_string_list = param_string.split(",")
    #print("PARAM LIST:" +  param_string_list, len(param_string_list))
    verb = param_string_list[0]
    noun_one = param_string_list[1]
    noun_one = param_string_list[2]

    if "blend" in param_string:
        if "red" in param_string and "yellow" in param_string:
            server_reply_string = "orange"
        elif "yellow" in param_string and "blue" in param_string:
            server_reply_string = "green"
        elif "blue" in param_string and "red" in param_string:
            server_reply_string = "violet"
        else: server_reply_string = "Please only enter primary colors to blend. These are: red, yellow, and blue.\n"
    elif "choose" in param_string:
        rand_num_decider = random.random() *123456
        print("rand_num_decider" + str(rand_num_decider))
        if (rand_num_decider % 2) == 0:
            server_reply_string = noun_one
        else: server_reply_string = noun_two
        print(server_reply_string)
    else:
        server_reply_string = "Please let me know if you want to 'blend' or 'choose', and let me know which two primary colors you have selected.\n"

    #print("digital_palatte function. server reply is " + server_reply_string)
    server_reply = bytes(server_reply_string, 'utf-8')


print("Initiating connection to client - listening for connections at IP", HOST, "and port", PORT)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Established connection, {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(f"Received client message: '{data!r}' [{len(data)} bytes]")
            digital_palette(data)
            print("Server Reply is:" + server_reply_string)
            conn.send(server_reply)

print("Server job complete!\n")