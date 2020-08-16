from socket import *
import os
import pickle

sender = ('sender ip', 12345)
conn = socket(AF_INET, SOCK_STREAM)
conn.connect(sender)
print(f'connected to the sender({sender[0]} port {sender[1]})')

preview = pickle.loads(conn.recv(1024))
file_name = str(preview[0])
file_size = int(preview[1])
print(f'file name: {file_name}, file size: {str(file_size)[:-6]} MB')

with open(f'1{file_name}', 'wb') as file:
    i = 0
    a = (1, 1, 1)
    while i < file_size:
        massage = conn.recv(512)
        file.write(massage)
        i += len(massage)
        if file_size / 3 < i < file_size / 2 and a[0]:
            print('30% send')
            a = (0, 1, 1)
        if file_size / 2 < i < (file_size / 10) * 8 and a[1]:
            print('50% send')
            a = (0, 0, 1)
        if (file_size / 10) * 8 < i < file_size and a[2]:
            print('80% send')
            a = (0, 0, 0)
        if i == file_size:
            print('100% send')

conn.close()
