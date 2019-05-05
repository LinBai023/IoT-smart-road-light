from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn import svm
import pandas as pd
import numpy as np
from numpy import genfromtxt
import boto3
from boto3.dynamodb.conditions import Key,Attr
import time
from decimal import Decimal


import socket
import os
import sys

server = socket.socket()

try:
    addr = socket.getaddrinfo('ec2-34-239-118-107.compute-1.amazonaws.com', 80)[0][-1]
    server.bind(addr)
    server.listen(1)

    print("now listening")
except socket.error as msg:
    print("socket connection error: ", msg)
    sys.exit()


dbName = "TrafficSecond"
resource = boto3.resource('dynamodb',region_name='us-east-1')

# load data
train_data = genfromtxt("train_set.csv", delimiter=',')
x_train = train_data[1:,2:6]
y_train = train_data[1:, 6]
# print(y_train)

# test_data = genfromtxt("test_set1.csv", delimiter=',')
# x_test = test_data[1:,2:6]
# y_test = test_data[1:, 6]



# train the model
clf = svm.SVC(0.8, kernel = 'rbf', gamma = 20, decision_function_shape='ovr')
clf.fit(x_train, y_train)


# server = socket.socket()

# try:
#     addr = socket.getaddrinfo('ec2-34-239-118-107.compute-1.amazonaws.com', 80)[0][-1]
#     server.bind(addr)
#     server.listen(1)

#     print("now listening")
# except socket.error as msg:
#     print("socket connection error: ", msg)
#     sys.exit()



try:
    resource.create_table(TableName=dbName, KeySchema=[{'AttributeName': 'Time', 'KeyType': 'HASH'}, ],
        AttributeDefinitions=[{'AttributeName': 'Time', 'AttributeType': 'S'}, ],
        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5})
    table = resource.Table(dbName)
    time.sleep(15)
except Exception as e:
    print('Table already exists')
    table = resource.Table(dbName)

while True:
    conn, addr = server.accept()
    print("Connect with: ", addr)
    msg = conn.recv(1024)
    print(msg.decode('utf-8'))

    if msg:
        test_data = []
        receive_msg = msg.decode('utf-8')
        receive_data = receive_msg.split(",")
        print("receive_data", receive_data)
        for i in range(len(receive_data)):
            print("data[i]: ", receive_data[i])
            test_data.append(int(receive_data[i]))
        
        test_x = [test_data]
        # print(test_x)
        y_pred = clf.predict(test_x)
        # print(clf.predict(test_x))
        pre_y_list = np.asarray(y_pred)
        pre_y = pre_y_list[0]
        prediction = dict()
        currentTime = time.time()
        prediction['Time'] = str(currentTime)
        prediction['Traffic'] = str(pre_y)
        response = table.put_item(Item = prediction)
        print("response: ", response)


server.close()




