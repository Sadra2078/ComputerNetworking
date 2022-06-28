"""
Server receiver of the file
"""
import re
import socket
import tqdm
import os
import threading
# device's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001
# receive 4096 bytes each time
BUFFER_SIZE = 1024 * 500
SEPARATOR = "<SEPARATOR>"
# create the server socket
# TCP socket
s = socket.socket()
# bind the socket to our local address
s.bind((SERVER_HOST, SERVER_PORT))
# enabling our server to accept connections
# 5 here is the number of unaccepted connections that
# the system will allow before refusing new connections
s.listen(5)
# print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
# # accept connection if there is any
# client_socket, address = s.accept()
# # if below code is executed, that means the sender is connected
# print(f"[+] {address} is connected.")
dir = os.listdir()
# receive the file infos
# receive using client socket, not server socket
def x(client_socket):
    while(True):
        choose = client_socket.recv(BUFFER_SIZE).decode()
        #upload a file to client ##################################################################################
        if (choose=='1'):
            while(True):
                filename = client_socket.recv(BUFFER_SIZE).decode()
                if filename in dir:
                    filesize = os.path.getsize(filename) #check if the file not exist
                    client_socket.send(f"{filename}{SEPARATOR}{filesize}".encode())
                    # start sending the file
                    # progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
                    open(filename, "rb")
                    with open(filename, "rb") as f:
                        while True:
                            # read the bytes from the file
                            bytes_read = f.read(BUFFER_SIZE)
                            if not bytes_read:
                                # file transmitting is done
                                break

                            # we use sendall to assure transimission in 
                            # busy networks
                            client_socket.sendall(bytes_read)
                            # update the progress bar
                            # progress.update(len(bytes_read))
                    print("File successfully uploaded.\n")
                    break
                else:
                    print("File Not Found.\n")
                    client_socket.send("not found".encode())
                    break
        #get a file from client ###################################################################################
        if(choose=='2'):
            try:
                received = client_socket.recv(BUFFER_SIZE).decode()
                filename, filesize = received.split(SEPARATOR)
                # remove absolute path if there is
                filename = os.path.basename(filename)
                # convert to integer
                filesize = int(filesize)
                # start receiving the file from the socket
                # and writing to the file stream
                # progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
                with open(filename, "wb") as f:
                    while True:
                        # read 1024 bytes from the socket (receive)
                        bytes_read = client_socket.recv(BUFFER_SIZE)
                        if not bytes_read:    
                            # nothing is received
                            # file transmitting is done
                            break
                        # write to the file the bytes we just received
                        f.write(bytes_read)
                        break
                        # update the progress bar
                        # progress.update(len(bytes_read))
                print("File successfully recieved.\n")
            except:
                continue
        if (choose=='3'):   # file list ################################################################################
            file_list = '\t***FILE LIST***\n\n'
            for d in dir:
                file_list = file_list + '\t' +  d + "\n"
            client_socket.send(file_list.encode())
            print("file list sent.")
        if (choose=='4'):     # Quit and close the the client & server  ################################################
            client_socket.close()    # close the client socket
            print(f"[-] {address} is disconnected.")     
            break                   
            # s.close()   # close the server socket



if __name__ == "__main__": 
    while(True):
        print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
        # accept connection if there is any
        client_socket, address = s.accept()
        # if below code is executed, that means the sender is connected
        print(f"[+] {address} is connected.")
        t = threading.Thread(target=x, args=(client_socket,)) 
        t.start()
        # t.join()
        # creating thread 
