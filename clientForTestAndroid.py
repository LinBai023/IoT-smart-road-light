import requests
import json
# fs = '1'
import time

count = 1
while True:
    try:
        r = requests.post("http://ec2-3-84-46-25.compute-1.amazonaws.com", data="getdata")
        print("##############")
        print(r.text)
        print("count: ", count)
        break
    except:
        count += 1
        time.sleep(3)
# print(r.headers)
# if r:
#     print(r.text.decode('utf-8'))
# print(r.text)

# import socket
# from socket import socket, AF_INET, SOCK_STREAM
# import os
# import sys

# s = socket(AF_INET, SOCK_STREAM)
# s.connect(('ec2-3-84-46-25.compute-1.amazonaws.com', 80))
# s.sendall('1'.encode('utf-8'))
# print("receive: ", s.recv(1024))


# while True:
#     # s2 = socket(AF_INET, SOCK_STREAM)
#     # s.connect(('ec2-3-84-46-25.compute-1.amazonaws.com', 80))  
#     # s2.listen(1)
#     print("receive: ", s.recv(1024))
    # conn, address = s.recv()
    # print("Connect with: ", addr)
    # msg = conn.recv(1024)
    # print(msg.decode('utf-8'))

# s.close()
# 