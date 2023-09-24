import socket
from time import time, localtime, strftime
from requests import get, post
from threading import Thread
from queue import Empty, Queue
from json import dumps

class Server():
    def __init__(self):
        self.socket = socket.socket()
        server_address = ('', 20000)
        print('Старт сервера, порт {}'.format(server_address[1]))
        self.socket.bind(server_address)
        self.socket.listen()
        
        self.queue = Queue()
        
        rest_thread = Thread(target = self.consumer, args = (self.queue,))
        rest_thread.start()

    def consumer(self, queue):
        while True:
            try:
                mess = queue.get()
            except Empty:
                continue
            else:
                print(f'Обрабатываем сообщение {mess} \n')
                
                id_pac = self.request_from_georitm_id_pac(mess)

                if 'E' in mess:
                    print('Отправляем тревогу')
                    print()
                    self.send_alarm_to_pac(id_pac)
                    print('Тревога отправлена')
                    print()
                elif 'R' in mess:
                    print('Отменяем тревогу')
                    print()
                    self.send_cancel_to_pac(id_pac)
                    print('Тревога отменена')
                    print()
                
                queue.task_done()
                
    def request_from_georitm_id_pac(self, mess):
        url_test = 'http://localhost:8080/restapi/users/login/'
        payload = {'login': 'root', 'password': 'password'}
        response = post(url_test, json = payload)
        
        basic = response.json()['basic']
        headers = {'Authorization': 'Basic ' + basic}
        
        imei = mess[8 : 24]

        #objects/obj-search/
        url_test = 'http://localhost:8080/restapi/objects/obj-search/'
        
        payload = {"objType":1, "q":imei}
        response = post(url_test, headers = headers, json = payload)

        id_ritm = response.json()[0]['id']

        #objects/obj-card/
        url_test = 'http://localhost:8080/restapi/objects/obj-card/'
        payload = {'objectId': id_ritm}
        response = post(url_test, headers = headers, json = payload)

        id_pac = response.json()['settings']['equipmentIds']
        id_pac = id_pac[2 : -2]

        print(id_pac)
        return id_pac

    def send_alarm_to_pac(self, id_pac):
        #https://pakvcmk.ru/api/login
        url_test = 'https://demo.pakvcmk.ru/api/login'
        payload = {'username': 'emp220923', 'password': '7i0f8g'}
        response = post(url_test, json = payload)

        bearer = response.json()['token']
        headers = {'Authorization':'Bearer ' + bearer}
        
        #id_test = '2027d463-56c5-49fd-9f43-7af80f5e44df'

##        url_test = 'https://demo.pakvcmk.ru/api/objects/' + id_test
##        response = get(url_test, headers = headers)
        
        url_test = 'https://demo.pakvcmk.ru/api/alert'
        payload = {
                    "object_id": id_pac,
                    "events":[{
                                #"zone_id": "ID зоны",
                                "type_id": 0,
                                "comment": "Тестовая тревога"
                                }]
                    }
        response = post(url_test, headers = headers, json = payload)        
        
        print(dumps(response.json(), indent = 4))

    def send_cancel_to_pac(self, id_pac):
        url_test = 'https://demo.pakvcmk.ru/api/login'
        payload = {'username': 'emp220923', 'password': '7i0f8g'}
        response = post(url_test, json = payload)

        bearer = response.json()['token']
        headers = {'Authorization':'Bearer ' + bearer}

        url_test = 'https://demo.pakvcmk.ru/api/alerts'
        response = get(url_test, headers = headers)

        for alert in response.json():
            if alert['object_id'] == id_pac:
                id_alert = alert['alert_id']

        url_test = 'https://demo.pakvcmk.ru/api/alert/' + id_alert + '/' + 'cancel'
        payload = {'comment': 'Тестирование'}
        response = post(url_test, headers = headers, json = payload)
        
        print(response)

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
                        t = strftime('%d.%m.%Y %H:%M:%S', localtime(time()))
                        print(t)
                        
                        print(f'Получено из Ritm-link: {data_dec}')

                        if ('E' in data_dec) or ('R' in data_dec):

                            #print(f'Вставляем сообщение {data_dec} в очередь\n')
                            self.queue.put(data_dec)
                            
                            ack = chr(6).encode('utf-8')
                            connection.sendall(ack)
                    else:
                        print('Нет данных от:', client_address)
                        break
            except Exception as e:
                print(e)
            finally:
                connection.close()


server = Server()
server.connect_loop()
#server.send_alarm_to_pac()
#server.request_test()

