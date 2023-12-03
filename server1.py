import re
from socket import *
import random
import ast
import threading
import time
import argparse

SERVER1 = "172.18.12.189"
SERVER2 = "172.18.12.189"
SERVER3 = "172.18.12.189"
SERVER4 = "172.18.12.189"

class SocketThread(threading.Thread):
    """
    Class for multithreading TCP socket.
    """
    def __init__(self, connection, client_info, buffer_size=1024, recv_timeout=5):
        threading.Thread.__init__(self)
        self.connection = connection
        self.client_info = client_info
        self.buffer_size = buffer_size
        self.recv_timeout = recv_timeout

    def run(self):
        """
        Function to get client weights and create local files for each client
        """
        self.full_data = ''
        while True:
            self.start_time = time.time()
            received_data, status = self.recv_data()

            if received_data != None:
                self.full_data = received_data

            if status == 0:
                self.connection.close()
                print("Connection closed with {client} due to inactivity or error.".format(client=self.client_info))
                break


    def recv_data(self):
        """
        Function to call recv() until all data received from client.
        outputs:	received_data=data from client
                1=keep connection open, 0=close connection
        """
        received_data = ''
        while True:
            try:
                self.connection.settimeout(self.recv_timeout)
                data = self.connection.recv(self.buffer_size).decode('utf-8')
                received_data += data

                if data == '' and len(received_data) == 0:
                    if (time.time() - self.start_time) > self.recv_timeout:
                        return None, 0 #connection inactive
            
                elif data == '' and len(received_data) > 0:
                    try:
                        return received_data, 1

                    except BaseException as e:
                        print("Error decoding client data: {msg}.\n".format(msg=e))
                        return None, 0
    
                else: self.start_time = time.time() #reset timeout counter

            except BaseException as e:
                print("Error receiving data from {client}: {msg}.\n".format(client=self.client_info,msg=e))
                return None, 0


def server_get():
    """
    Function to get info from customer.
    """
    serverSocket = socket(AF_INET,SOCK_STREAM)
    serverSocket.bind((SERVER1,10800))
    print("Socket created at {ip}".format(ip=SERVER1))

    serverSocket.listen(1)
    print('Listening for connection...')
    
    connection, customer = serverSocket.accept()
    print("New connection from client: {client}".format(client=customer))
    socket_thread = SocketThread(connection=connection, client_info=customer, buffer_size=1024, recv_timeout=5)
    socket_thread.start()
    
    socket_thread.join()
    return socket_thread.full_data
    


def send_to_server(server, port, id, data, encrypt):
    """
    Function to send data fragment to respected server.
    """
    soc = socket(AF_INET, SOCK_STREAM)
    soc.connect((server, port))

    if (encrypt):
        msg = "["+str(id)+"],["+str(data).strip('][')+"]"
    else:
        msg = "["+str(id)+","+str(data).strip('][')+"]"
        
    soc.sendall(msg.encode('utf-8'))
    print("\nData sent to: {server}".format(server=server))
    print(msg)

    soc.close()


def split_data(data, encrypt):
    """
    Function to split data for each server.
    """
    customer_id = random.randint(pow(10,4), pow(10,5)-1)        #create random 5-digit id for nonsensitive data
    card_id = random.randint(pow(10,6), pow(10,7)-1)            #create random 7-digit id for sensitive data
    
    data = ast.literal_eval(data)                               #convert string to list
    
    send_to_server(SERVER2, 10600, customer_id, card_id, encrypt)        #send mappings to server 2
    send_to_server(SERVER3, 11000, card_id, data[2:4], encrypt)          #send sensitive data to server 3
    send_to_server(SERVER4, 19500, customer_id, data[0:2], encrypt)      #send nonsensitive data to server 4


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-e','--encrypt',action='store_true',help='Encrypt user data.')
    arg = parser.parse_args()

    data = server_get()
    split_data(data, arg.encrypt)