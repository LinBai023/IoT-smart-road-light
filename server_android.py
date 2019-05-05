import boto3
from boto3.dynamodb.conditions import Key,Attr
import time


import socket
import os
import sys

import requests

server = socket.socket()

try:
    addr = socket.getaddrinfo('ec2-3-84-46-25.compute-1.amazonaws.com', 80)[0][-1]
    server.bind(addr)
    server.listen(1)

    print("now listening")
except socket.error as msg:
    print("socket connection error: ", msg)
    sys.exit()

dbName = "TrafficSecond"
resource = boto3.resource('dynamodb',region_name='us-east-1')

# try:
#     resource.create_table(TableName=dbName, KeySchema=[{'AttributeName': 'Time', 'KeyType': 'HASH'}, ],
#         AttributeDefinitions=[{'AttributeName': 'Time', 'AttributeType': 'S'}, ],
#         ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5})
#     table = resource.Table(dbName)
#     time.sleep(15)
# except Exception as e:
#     print('Table already exists')
#     table = resource.Table(dbName)

while True:
    result = None
    conn, addr = server.accept()
    print("Connect with: ", addr)
    msg = conn.recv(1024)
    # print(msg.decode('utf-8'))

    receive_msg = msg.decode('utf-8')
    print(receive_msg)
    if receive_msg:
        allEntry = resource.Table(dbName).scan()
        timeList = []
        itemList = allEntry['Items']
        for row in itemList:
            timeList.append(row['Time'])
            # result.append(row)
        timeList.sort()
        lastTime = timeList[-1]
        for row in itemList:
            if row['Time'] == lastTime:
                result = row['Traffic']
        print("result: ",result)
        # if result == []:
        #     result = "1"
        response = "HTTP/1.1 200 OK\r\n\r\n " + str(result)
        conn.send(response.encode('utf-8'))
        # conn.sendall(.encode('utf-8'))
        print("sent")
    else:
        conn.send("HTTP/1.1 200 OK\r\n\r\n failure")
    time.sleep(2)

    conn.close()
