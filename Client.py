from email import message
import socket
from warnings import catch_warnings
import tqdm
import os
import argparse

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 1024 * 500 #4KB

def send_file(host, port):
    # create the client socket
    s = socket.socket()
    print(f"[+] Connecting to {host}:{port}")
    s.connect((host, port))
    print("[+] Connected.\n")

    while(True):
        print('Select on of this list: \n 1) Get\n 2) Put\n 3) Ls\n 4) Quit')
        choose = input()
        ###################################################################################
        if (choose == '1'):
            s.send('1'.encode())
            print('Enter server file name for download...')
            filename = input()
            s.send(filename.encode())
            while(True):
                try:
                    received = s.recv(BUFFER_SIZE).decode()
                    if received =='not found':
                        print("Your file name not found! Try again...")
                        break
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
                            bytes_read = s.recv(BUFFER_SIZE)
                            if not bytes_read:    
                                # nothing is received
                                # file transmitting is done
                                continue
                            # write to the file the bytes we just received
                            f.write(bytes_read)
                            break
                            # update the progress bar
                            # progress.update(len(bytes_read))
                            
                    print("file successfully recieved.\n")
                    break
                except:
                    break
        ###################################################################################
        if (choose == '2'): # if user want to upload a file
            s.send("2".encode())
            print('Enter your file path with name')
            filename = input() #get file path from client for upload the file to server
            try:
                filesize = os.path.getsize(filename) #check if the file not exist
            except:
                print("File Not Found. Try again please!\n")
                continue
            s.send(f"{filename}{SEPARATOR}{filesize}".encode())
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
                    s.sendall(bytes_read)
                    # update the progress bar
                    # progress.update(len(bytes_read))
            print("File successfully uploaded.\n")
        #######################################################################################
        if (choose=='3'):
            s.send("3".encode())
            while(True):
                dir = s.recv(BUFFER_SIZE).decode()
                if dir != "":
                    print(dir)
                    break;
        #######################################################################################
        # close the socket
        if (choose=='4'): #???????????????????????
            s.send("4".encode())
            s.close()
            break
        #######################################################################################

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Simple File Sender")
    parser.add_argument("host", help="The host/IP address of the receiver")
    parser.add_argument("-p", "--port", help="Port to use, default is 5001", default=5001)
    args = parser.parse_args()
    host = args.host
    port = args.port
    send_file(host, port)