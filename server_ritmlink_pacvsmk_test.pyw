import socket

#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock = socket.socket()

# Привязываем сокет к порту

host = socket.gethostname()
print(host)
hhost = socket.getfqdn(host)
print(hhost)
hhhost = socket.getfqdn()
print(hhhost)
addr = socket.getaddrinfo(host, 3000)
print(addr)

server_address = (host, 20000)
print('Старт сервера на {} порт {}'.format(*server_address))
sock.bind(server_address)

# Слушаем входящие подключения
sock.listen()

while True:
    # ждем соединения
    print('Ожидание соединения...')
    connection, client_address = sock.accept()
    try:
        print('Подключено к:', client_address)
        # Принимаем данные порциями
        while True:
            data = connection.recv(32)
            #print(data)
            data = data.decode()
            if data != '':
                print(f'Получено: {data}')
            else:
                print('Нет данных от:', client_address)
                break

    finally:
        # Очищаем соединение
        connection.close()

