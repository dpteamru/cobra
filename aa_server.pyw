# test-server.py
import os
import socket
import sys
import struct

players = 0
turn = 1 #чей сейчас ожидается ход
file = 0 #чей файл доступен на сервере

def receive_file_size(sck: socket.socket):
    # Эта функция обеспечивает получение байтов, 
    # указывающих на размер отправляемого файла, 
    # который кодируется клиентом с помощью 
    # struct.pack(), функции, которая генерирует 
    # последовательность байтов, представляющих размер файла.
    fmt = "<Q"
    expected_bytes = struct.calcsize(fmt)
    received_bytes = 0
    stream = bytes()
    while received_bytes < expected_bytes:
        chunk = sck.recv(expected_bytes - received_bytes)
        stream += chunk
        received_bytes += len(chunk)
    filesize = struct.unpack(fmt, stream)[0]
    return filesize

def receive_file(sck: socket.socket, filename):
    # Сначала считываем из сокета количество 
    # байтов, которые будут получены из файла.
    filesize = receive_file_size(sck)
    # Открываем новый файл для сохранения
    # полученных данных.
    with open(filename, "wb") as f:
        received_bytes = 0
        # Получаем данные из файла блоками по
        # 1024 байта до объема
        # общего количество байт, сообщенных клиентом.
        while received_bytes < filesize:
            chunk = sck.recv(1024)
            if chunk:
                f.write(chunk)
                received_bytes += len(chunk)

def send_file(sck: socket.socket, filename):
    # Получение размера файла.
    filesize = os.path.getsize(filename)
    # В первую очередь сообщим серверу, 
    # сколько байт будет отправлено.
    sck.sendall(struct.pack("<Q", filesize))
    # Отправка файла блоками по 1024 байта.
    with open(filename, "rb") as f:
        while read_bytes := f.read(1024):
            sck.sendall(read_bytes)

# создаемTCP/IP сокет
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Привязываем сокет к порту
server_address = ('localhost', 10000)
print('Старт сервера на {} порт {}'.format(*server_address))
sock.bind(server_address)

# Слушаем входящие подключения
sock.listen(5)

while True:
    # ждем соединения
    print('Ожидание соединения...')
    connection, client_address = sock.accept()
    try:
        print('Подключено к:', client_address)
        # Принимаем данные порциями и ретранслируем их
        while True:
            data = connection.recv(16)
            data = data.decode()
            print(f'Получено: {data}')
            if 'name' in data:
                if players == 2:
                    players = 0
                players = players + 1
                mess = str(players)
                connection.sendall(mess.encode())
            elif 'turn' in data: #клиент говорит, что совершил ход и может отправить файл
                connection.sendall('file'.encode()) #разрешаем отправить файл
                receive_file(connection, "collection-server.json")

                if data == 'turn_1':
                    turn = 2
                    file = 1
                else:
                    turn = 1
                    file = 2
            elif 'file' in data: #клиент запрашивает файл удара другого клиента
                if data[-1] == str(file): #запрашиваемый файл есть на сервере
                    connection.sendall(data.encode())
                    send_file(connection, "collection-server.json")
                    file = 0
                else: #файл еще не получен сервером
                    connection.sendall('file_0'.encode())
                
            else:
                print('Нет данных от:', client_address)
                break

    finally:
        # Очищаем соединение
        connection.close()
