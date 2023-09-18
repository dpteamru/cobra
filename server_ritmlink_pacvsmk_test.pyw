import socket
import time

#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock = socket.socket()

# Привязываем сокет к порту

host = socket.gethostname()
print(host)
addr = socket.getaddrinfo(host, 20000)
print(addr)

server_address = ('', 20000)
print('Старт сервера на {} порт {}'.format(*server_address))
sock.bind(server_address)

# Слушаем входящие подключения
sock.listen()

ack = chr(6)
ack = ack.encode('utf-8')
print(ack)

while True:
    # ждем соединения
    print('Ожидание соединения...')
    connection, client_address = sock.accept()
    try:
        print('Подключено к:', client_address)
        # Принимаем данные порциями
        while True:
            data = connection.recv(32)
            print(data)
            data_dec = data.decode()
            if data_dec != '':
                
                print(time.ctime( time.time() ))
                print(f'Получено: {data}')
                print(f'Получено дек: {data_dec}')
                
                connection.sendall(ack)
            else:
                print('Нет данных от:', client_address)
                break

    finally:
        # Очищаем соединение
        connection.close()

