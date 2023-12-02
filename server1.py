from socket import *
import random
import ast
import threading
import time

SERVER1 = "172.18.12.189"
SERVER2 = "172.18.4.243"
SERVER3 = "172.18.4.243"
SERVER4 = "172.18.4.243"

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
        self.param_count = 0
        self.full_data = ''
        while True:
            self.start_time = time.time()
            received_data, status = self.recv_data()

            if received_data != None:
                self.full_data = received_data
                self.param_count += 1

            if status == 0:
                self.confirm_data()

                self.connection.close()
                print("Connection closed with {client} due to inactivity or error.".format(client=self.client_info))
                #return self.full_data


    def recv_data(self):
        """
        Function to call recv() until all data received from client.
        outputs:	received_data=data from client
                1=keep connection open, 0=close connection
        """
        received_data = b''
        while True:
            try:
                self.connection.settimeout(self.recv_timeout)
                data = self.connection.recv(self.buffer_size)
                received_data += data

                if data == b'':
                    received_data = b''

                    if (time.time() - self.start_time) > self.recv_timeout:
                        return None, 0 #connection inactive
            
                elif str(data)[-2] == '.':
                    if len(received_data) > 0:
                        try:
                            return received_data, 1

                        except BaseException as e:
                            print("Error decoding client data: {msg}.\n".format(msg=e))
                            return None, 0
    
                else: self.start_time = time.time() #reset timeout counter

            except BaseException as e:
                print("Error receiving data from {client}: {msg}.\n".format(client=self.client_info,msg=e))
                return None, 0


    def confirm_data(self):
        """
        Function to send confirmation of received data to client.
        """
        msg = "Server received data."
        self.connection.sendall(msg.encode('utf-8'))
        print("Sent data confirmation to client: {client}".format(client=self.client_info))


def server_get():
    """
    Function to get info from customer.
    """
    serverSocket = socket(AF_INET,SOCK_STREAM)
    serverSocket.bind((SERVER1,10800))
    print("Socket created at {ip}".format(ip=SERVER1))

    serverSocket.listen(1)
    print('Listening for connection...')
    
    while True:
        try:
            connection, customer = serverSocket.accept()
            print("New connection from client: {client}".format(client=customer))

            socket_thread = SocketThread(connection=connection, client_info=customer, buffer_size=1024, recv_timeout=5)
            socket_thread.start()

        except:
            serverSocket.close()
            break
        
    return socket_thread.full_data


def send_to_server(server, port, id, data):
    """
    Function to send data fragment to respected server.
    """
    soc = socket(AF_INET, SOCK_STREAM)
    soc.connect((server, port))

    msg = "["+str(id)+","+str(data).strip('][')+"]"
    soc.sendall(msg.encode('utf-8'))
    print("\nData sent to: {server}".format(server=server))
    print(msg)

    soc.close()


def split_data(data):
    """
    Function to split data for each server.
    """
    customer_id = random.randint(pow(10,4), pow(10,5)-1)        #create random 5-digit id for nonsensitive data
    card_id = random.randint(pow(10,6), pow(10,7)-1)            #create random 7-digit id for sensitive data
    
    data = ast.literal_eval(data)                               #convert string to list
    
    send_to_server(SERVER2, 10600, customer_id, card_id)        #send mappings to server 2
    send_to_server(SERVER3, 11000, card_id, data[2:4])          #send sensitive data to server 3
    send_to_server(SERVER4, 19500, customer_id, data[0:2])      #send nonsensitive data to server 4


if __name__ == "__main__":
    data = server_get()
    split_data(data)