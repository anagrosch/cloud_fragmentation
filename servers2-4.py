from socket import *
import ast
import time
import threading

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
                print('full = ', self.full_data)

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
            

def recv_data(server, port):
    """
    Function to receive data fragment from Server 1.
    Return  :   data
    """
    soc = socket(AF_INET, SOCK_STREAM)
    soc.bind((server, port))
    print("Socket created at {ip}".format(ip=server))

    soc.listen(1)
    print('Listening for connection...')

    connection, customer = soc.accept()
    print("New connection from client: {client}".format(client=customer))
    socket_thread = SocketThread(connection=connection, client_info=customer, buffer_size=1024, recv_timeout=5)
    socket_thread.start()
    
    while (len(socket_thread.full_data) <= 0):
        time.sleep(1)
    
    
    data = ast.literal_eval(socket_thread.full_data)                               #convert string to list
    return data


def print_server2(data):
    """
    Function to print Server 2's data.
    """
    print('Mappings')
    print('========')
    print("customer_id:\t{id}".format(id=data[0]))
    print("card_id:\t{id}".format(id=data[1]))


def print_server3(data):
    """
    Function to print Server 3's data.
    """
    print('Sensitive data')
    print('==============')
    print("card_id:\t{id}".format(id=data[0]))
    print("\ncredit card #:\t{num}".format(num=data[1]))
    print("\ncredit card ccv:\t{ccv}".format(ccv=data[2]))


def print_server4(data):
    """
    Function to print Server 4's data.
    """
    print('Non-sensitive data')
    print('==================')
    print("customer_id:\t{id}".format(id=data[0]))
    print("\nname:\t{name}".format(name=data[1]))
    print("\nphone #:\t{num}".format(num=data[2]))


if __name__ == "__main__":
    server_num = input('Enter server #(2,3,4): ')

    if (server_num == '2'):
        data = recv_data(SERVER2,10600)
        print_server2(data)
    elif (server_num == '3'):
        data = recv_data(SERVER3, 11000)
        print_server3(data)
    elif (server_num == '4'):
        data = recv_data(SERVER4, 19500)
        print_server4(data)
    else:
        print('Invalid server input.')
