import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Привязываем сокет к порту
server_address = ('127.0.0.1', 3000)
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

