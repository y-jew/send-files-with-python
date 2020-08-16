from socket import *
import os
import time
import pickle

client = ('', 12345)
send = socket(AF_INET, SOCK_STREAM)
send.bind(client)
send.listen(1)
client_socket, address = send.accept()
print(f'new client connected ({address[0]} port {address[1]})')

photo_path = input('please type the file path to send: ')
start_time = time.time()
name = os.path.basename(photo_path)
photo = open(photo_path, 'rb')
file_size = os.path.getsize(photo_path)
print(f'file name: {name}, file size: {str(file_size)[:-6]} MB\nsending file...')
preview = (name, file_size)
client_socket.sendall(pickle.dumps(preview))

send_photo = photo.read(512)
client_socket.sendall(send_photo)
i = len(send_photo)
a = (1, 1, 1)
while i < file_size:
    send_photo = photo.read(512)
    client_socket.sendall(send_photo)
    i += len(send_photo)
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


client_socket.close()
send.close()
photo.close()
end_time = time.time()
print(f'\nSending {str(file_size)[:-6]} MB in {str(int(end_time - start_time))} seconds')
