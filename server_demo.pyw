import sys
import socket
from time import time, localtime, strftime
from requests import get, post
from threading import Thread
from queue import Empty, Queue
from json import dumps
from settings import *

log_file = open(log_filename, 'w+')
sys.stdout = log_file

class Server():
    def __init__(self):
        self.socket = socket.socket()
        server_address = ('', port)
        print('Старт сервера, порт {}'.format(server_address[1]))
        self.socket.bind(server_address)
        self.socket.listen()
        
        self.queue = Queue()
        
        rest_thread = Thread(target = self.consumer, args = (self.queue,))
        rest_thread.start()

        self.alerts = []

    def consumer(self, queue):
        while True:
            try:
                mess = queue.get()
            except Empty:
                continue
            else:
                print(f'Обрабатываем сообщение {mess} \n')
                
                imei = mess[7 : 23]

                if 'E' in mess:
                    print('Отправляем тревогу')
                    print()
                    id_pac = self.request_from_georitm_id_pac(mess)
                    alert_pac = self.send_alarm_to_pac(id_pac)
                    alert = {'imei': imei,
                             'code': mess[24 : 27],
                             'zona': mess[28 : 30],
                             'plume': mess[30 : 33],
                             'alert_id': alert_pac['alert_id']}
                    self.alerts.append(alert)
                    print('Тревога отправлена')
                    print()
                elif 'R' in mess:
                    print('Восстановление')
                    print()
                    alert = [alert for alert in self.alerts if alert['imei'] == imei]
                    if alert != []:
                        alert = alert[0]
                        id_alert = alert['alert_id']
                        self.send_event_to_pac(alert)
                        self.alerts.remove(alert)
                        print('Восстановление отправлено')
                        print()
                        
                    else:
                        print('Для данного сообщения о восстановлении нет сохраненных тревог')
                        print('Не получилось послать восстановление')
                
                queue.task_done()
                
    def request_from_georitm_id_pac(self, mess):
        url = f'{url_api_georitm}users/login/'
        payload = {'login': login_georitm, 'password': password_georitm}
        response = post(url, json = payload)
        
        basic = response.json()['basic']
        headers = {'Authorization': f'Basic {basic}'}
        
        imei = mess[7 : 23]

        url = f'{url_api_georitm}objects/obj-search/'
        
        payload = {"objType":1, "q":imei}
        response = post(url, headers = headers, json = payload)

        id_ritm = response.json()[0]['id']

        url = f'{url_api_georitm}objects/obj-card/'
        payload = {'objectId': id_ritm}
        response = post(url, headers = headers, json = payload)

        id_pac = response.json()['settings']['equipmentIds']
        id_pac = id_pac[2 : -2]

        return id_pac

    def send_alarm_to_pac(self, id_pac):
        url = f'{url_api_pac_demo}login'
        payload = {'username': username_pac_demo, 'password': password_pac_demo}
        response = post(url, json = payload)

        bearer = response.json()['token']
        headers = {'Authorization':f'Bearer {bearer}'}
        
        url = f'{url_api_pac_demo}alert'
        payload = {
                    "object_id": id_pac,
                    "events":[{
                                #"zone_id": "ID зоны",
                                "type_id": 0,
                                "comment": "Тестовая тревога"
                                }]
                    }
        
        response = post(url, headers = headers, json = payload)
        
        #print(dumps(response.json(), indent = 4))

        return response.json()

##    def send_cancel_to_pac(self, id_alert):
##        url_test = 'https://demo.pakvcmk.ru/api/login'
##        payload = {'username': 'emp220923', 'password': '7i0f8g'}
##        response = post(url_test, json = payload)
##
##        bearer = response.json()['token']
##        headers = {'Authorization':'Bearer ' + bearer}
##
##        url_test = 'https://demo.pakvcmk.ru/api/alert/' + id_alert + '/' + 'cancel'
##        payload = {'comment': 'Тестирование'}
##        response = post(url_test, headers = headers, json = payload)
##        
##        print(response)

    def send_event_to_pac(self, alert):
        url = f'{url_api_pac_demo}login'
        payload = {'username': username_pac_demo, 'password': password_pac_demo}
        response = post(url, json = payload)

        bearer = response.json()['token']
        headers = {'Authorization':'Bearer ' + bearer}

        alert_id = alert['alert_id']
        imei = alert['imei']
        code = alert['code']

        url = f'{url_api_pac_demo}alert/{alert_id}/event'
        comment = f'Восстановление (R). Прибор: {imei}. Код события: {code}.3'
        payload = {
                    #"zone_id": "ID зоны",
                    #"type_id": 3,
                    "comment": comment
                    }
        
        response = post(url, headers = headers, json = payload)

        #print(dumps(response.json(), indent = 4))

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
                            mess_code = data_dec[24 : 27]
                            if (int(mess_code) < 300):
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
                log_file.close()


server = Server()
server.connect_loop()

#mess = '5337 181000000000001280E76000000¶'
##id_pac = server.request_from_georitm_id_pac(mess)

##id_test = '2027d463-56c5-49fd-9f43-7af80f5e44df'
##alert = server.send_alarm_to_pac('2027d463-56c5-49fd-9f43-7af80f5e44df')
##print(alert)
#server.send_event_to_pac('cf7f74a3-c691-4f67-a2d8-6d8ce15ea53f')

##server.send_cancel_to_pac('7ed09509-c9f3-4c81-8978-880720e4c41b')