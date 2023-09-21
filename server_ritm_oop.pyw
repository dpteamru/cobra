import socket
import time
import requests

class Server():
    def __init__(self):
        self.socket = socket.socket()
        server_address = ('', 20000)
        print('Старт сервера, порт {}'.format(server_address[1]))
        self.socket.bind(server_address)
        self.socket.listen()

    def request_test(self):
        url_test = 'http://localhost:8080/restapi/users/login/'
        payload = {'login': 'root', 'password': 'password'}

        response = requests.post(url_test, json = payload)
        
        basic = response.json()['basic']

        #objects/obj-search/
        url_test = 'http://localhost:8080/restapi/objects/obj-search/'
        headers = {'Authorization': 'Basic ' + basic}
        payload = {"objType":1, "q":"1000000000001280"}
        response = requests.post(url_test, headers = headers, json = payload)

        id_ritm = response.json()[0]['id']

        #objects/obj-card/
        url_test = 'http://localhost:8080/restapi/objects/obj-card/'
        headers = {'Authorization': 'Basic ' + basic}
        payload = {'objectId': id_ritm}
        response = requests.post(url_test, headers = headers, json = payload)

        print(response.text)

        id_pac = response.json()['settings']['equipmentIds']
        print(id_pac)

    def connect_loop(self):
        while True:
            print('Ожидание соединения...')
            connection, client_address = self.socket.accept()
            try:
                print('Подключено к:', client_address)
                while True:
                    data = connection.recv(32)
                    data_dec = data.decode()
                    if data_dec != '':
                        print(time.ctime( time.time() ))
                        print(f'Получено: {data}')
                        #print(f'Получено дек: {data_dec}')

                        if 'E' in data_dec:
                            print('Нужно отправить тревогу')
                            ack = chr(6).encode('utf-8')
                            connection.sendall(ack)
                        elif 'R' in data_dec:
                            print('Нужно отправить восстановление')
                            ack = chr(6).encode('utf-8')
                            connection.sendall(ack)
                    else:
                        print('Нет данных от:', client_address)
                        break
            finally:
                connection.close()


server = Server()
#server.connect_loop()
server.request_test()
