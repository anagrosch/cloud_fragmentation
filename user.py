#   File run on user interacting with cloud

from ctypes import sizeof
from socket import *
from gm_cryptosystem import *
import argparse
import ast

SERVER1 = "172.18.12.189"

def get_data():
    """
    Function to get data from user to send to cloud.
    """
    info = []
    print('Welcome to Cloud Bank!')
    print('======================')

    info.append(input('Enter name: '))
    info.append(input('Enter phone number: '))
    info.append(input('Enter credit card number: '))
    info.append(input('Enter card ccv: '))

    return info


def client_send(data):
    """
    Function to send info to cloud.
    """
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((SERVER1, 10800))
    print('Connected to server.')

    clientSocket.sendall(data.encode('utf-8'))
    print("{data} sent.".format(data=data))
    print(len(data))
    clientSocket.close()


def encrypt_input(data):
    """
    Function to encrypt user's info with Goldwasser-micali cryptosystem.
    """
    #Goldwasser-micali cryptosystem keys
    c1_keys = generate_key()

    #encrypt each item in data list
    data = ast.literal_eval(data)                               #convert string to list
    print("before:\t{i}".format(i=data))
    
    for index in range(len(data)):
        data[index] = encrypt(data[index], c1_keys['pub'])
    
    #print("after:\t{i}\n".format(i=data))
    
    return c1_keys, str(data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-e','--encrypt',action='store_true',help='Encrypt user data.')
    arg = parser.parse_args()

    info = str(get_data())
    if (arg.encrypt):
        c1_keys, info = encrypt_input(info)
        print("GM keys:\t{k}\n".format(k=c1_keys))
    client_send(info)