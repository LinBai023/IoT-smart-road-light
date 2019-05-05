# from socket import socket, AF_INET, SOCK_STREAM

# s = socket(AF_INET, SOCK_STREAM)
# s.connect(('ec2-34-239-118-107.compute-1.amazonaws.com', 80))
# s.sendall('1-06-2018,Wednesday,7,7,39,37'.encode('utf-8'))

# import requests

# fs = '1,2,3,4'
# r = requests.post(url="http://ec2-34-239-118-107.compute-1.amazonaws.com", data=fs)

from socket import socket, AF_INET, SOCK_STREAM

s = socket(AF_INET, SOCK_STREAM)
s.connect(('ec2-34-239-118-107.compute-1.amazonaws.com', 80))
s.sendall('3,8,45,28'.encode('utf-8'))                                        