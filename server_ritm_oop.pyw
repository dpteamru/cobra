import socket
import time
import requests
from threading import Thread

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

        id_pac = response.json()['settings']['equipmentIds']
        id_pac = id_pac[2 : -2]

        print(id_pac)
        
        print(response.text)

    def send_alarm_to_pac(self):
        #https://pakvcmk.ru/api/login
        url_test = 'https://demo.pakvcmk.ru/api/login'
        payload = {'username': 'emp220923', 'password': '7i0f8g'}
        response = requests.post(url_test, json = payload)

        bearer = response.json()['token']

        headers = {'Authorization':'Bearer ' + bearer}
        id_test = '2027d463-56c5-49fd-9f43-7af80f5e44df'

##        url_test = 'https://demo.pakvcmk.ru/api/objects/' + id_test
##        response = requests.get(url_test, headers = headers)
        
        url_test = 'https://demo.pakvcmk.ru/api/alert'
        payload = {
                    "object_id": id_test,
                    "events":[{
                                #"zone_id": "ID зоны",
                                "type_id": 0,
                                "comment": "Тестовая тревога"
                                }]
                    }
        response = requests.post(url_test, headers = headers, json = payload)        
        
        print(response.text)
    

    def connect_loop(self):
        while True:
            print('Ожидание соединения...')
            connection, client_address = self.socket.accept()
            try:
                print('Подключено к:', client_address)
                while True:
                    data = connection.recv(64)
                    data_dec = data.decode()
                    if data_dec != '':
                        print(time.ctime( time.time() ))
                        #print(f'Получено: {data}')
                        print(f'Получено: {data_dec}')

                        if 'E' in data_dec:
                            print('Нужно отправить тревогу')
                            thread = Thread(target = self.send_alarm_to_pac)
                            thread.start()
                            #self.send_alarm_to_pac()
                            print('Тревога отправлена')
                            
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
server.connect_loop()
#server.send_alarm_to_pac()
#server.request_test()

