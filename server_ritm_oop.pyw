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

        #id_req = 500

##        #objects/objects-tree-set/ +
##        url_test = 'http://localhost:8080/restapi/objects/objects-tree-set/'
##        headers = {'Authorization': 'Basic ' + basic}
##        payload = {'groupType': 1}
        
##        #objects/obj/ +
##        url_test = 'http://localhost:8080/restapi/objects/obj/'
##        headers = {'Authorization': 'Basic ' + basic}
##        payload = {"objectId": [252]}

        #objects/obj-card/ +
        url_test = 'http://localhost:8080/restapi/objects/obj-card/'
        headers = {'Authorization': 'Basic ' + basic}
        payload = {'objectId': 312}

##        #objects/obj-by-extid/
##        url_test = 'http://localhost:8080/restapi/objects/obj-by-extid/'
##        headers = {'Authorization': 'Basic ' + basic}
##        payload = {'extId': [594], 'tz': 3}

##        #objects/obj-details/
##        url_test = 'http://localhost:8080/restapi/objects/obj-details/'
##        headers = {'Authorization': 'Basic ' + basic}
##        payload = {'objectId':[594], 'tz':3}

##        #alerts/objects-in-alarm/
##        url_test = 'http://localhost:8080/restapi/alerts/objects-in-alarm/'
##        headers = {'Authorization': 'Basic ' + basic}
##        
        response = requests.post(url_test, headers = headers, json = payload)
##        #response = requests.post(url_test, json = payload)
##        response = requests.post(url_test, headers = headers)
##
##        #список внутренних id объектов, которые находятся в тревоге
##        id_list_inAlarm = [obj_in_alarm['id'] for obj_in_alarm in response.json()]
##        print(id_list_inAlarm)
##
##        #теперь берём карточки этих объектов и сравниваем imei из сообщения ритм-линк с imei в карточке
##        url_test = 'http://localhost:8080/restapi/objects/obj-card/'
##        headers = {'Authorization': 'Basic ' + basic}
##        
##        payload = {'objectId': id_list_inAlarm[0]}
##        response = requests.post(url_test, headers = headers, json = payload)
##        print(response.text)
##
##        payload = {'objectId': id_list_inAlarm[1]}
##        response = requests.post(url_test, headers = headers, json = payload)
##        print(response.text)
        
        #print(response.request.headers)
        print(response.text)

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
