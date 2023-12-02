from socket import *
import ast

SERVER2 = "172.18.4.243"
SERVER3 = "172.18.4.243"
SERVER4 = "172.18.4.243"

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

    while True:
        try:
            connection, sender = soc.accept()
            print("New connection from client: {client}".format(client=sender))

            data = connection.recv(4098).decode()
            connection.close()
            return ast.literal_eval(data)                               #convert string to list

        except:
            soc.close()


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
    print("credit card #:\t{num}".format(num=data[1]))
    print("credit card ccv:\t{ccv}".format(ccv=data[2]))


def print_server4(data):
    """
    Function to print Server 4's data.
    """
    print('Non-sensitive data')
    print('==================')
    print("customer_id:\t{id}".format(id=data[0]))
    print("name:\t{name}".format(name=data[1]))
    print("phone #:\t{num}".format(num=data[2]))


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
