'''
Порядок действий на данный момент:
1. Подгрузить образ в докер
2. Создать папку c:\CobraIS
3. Положить туда файл settings.ini
4. Запустить гуи через экзешник
5. Можно нажимать на кнопки

'''

import tkinter as tk
import tkinter.font as font

import os

from subprocess import STARTUPINFO, STARTF_USESHOWWINDOW, SW_HIDE, check_output

startupinfo = STARTUPINFO()
startupinfo.dwFlags |= STARTF_USESHOWWINDOW
startupinfo.wShowWindow = SW_HIDE

def cmd(cmds):
    out = check_output(cmds, startupinfo = startupinfo).decode("utf-8")
    return out

def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master = None, placeholder = None, key = None, gui_settings = None):
        super().__init__(master)

        if placeholder is not None:
            self.placeholder_start = placeholder
            if key in gui_settings:
                self.placeholder = f'{placeholder}: {gui_settings[key]}'
            else:
                self.placeholder = placeholder
            self.placeholder_color = '#787878'
            #self.default_fg_color = self['fg']
            self.default_fg_color = '#787878'

            self.bind("<FocusIn>", self.focus_in)
            self.bind("<FocusOut>", self.focus_out)
            
            self.put_placeholder()

        self.config(bg = '#f0f0f0', relief = tk.FLAT, font = 'Jost 14')

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def focus_in(self, *args):
        self['fg'] = self.placeholder_color
        if self.get() == self.placeholder_start:
            self.delete('0', 'end')
            self.insert(0, f'{self.placeholder_start}: ')
##        if self['fg'] == self.placeholder_color:
##            self.delete('0', 'end')
##            self['fg'] = self.default_fg_color

    def focus_out(self, *args):
        if self.get() in [f'{self.placeholder_start}: ', f'{self.placeholder_start}:'] or \
           len(self.get()) < len(self.placeholder_start):
            self.delete('0', 'end')
            self.put_placeholder()
##        if not self.get():
##            self.put_placeholder()

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        w = 712
        h = 760
 
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
 
        x = int((sw - w) / 2)
        y = int((sh - h) / 2)
        
        self.geometry(f'{w}x{h}+{x}+{y}')
        self.resizable(False, False)
        self.config(bg = '#292929')

        icon = tk.PhotoImage(file = resource_path('img/logo24.png'))
        self.iconphoto(True, icon)

        self.running = self.check_status()
        self.need_restart = False

        self.settings_file = resource_path('c:\CobraIS\settings.ini')

        self.gui_settings = {}
        self.load_settings()

        self.img_oval_entry = tk.PhotoImage(file = resource_path('img/oval_entry.png'))

        #GeoRitm
        self.canvas_geo = tk.Canvas(self, height = 230, width = 652, bd = 0, highlightthickness = 0)
        self.canvas_geo_img = tk.PhotoImage(file = resource_path('img/frame_geo.png'))
        self.canvas_geo.create_image(0, 0, anchor = 'nw', image = self.canvas_geo_img)
        self.canvas_geo.place(x = 30, y = 30)

        self.label_geo_header = tk.Label(self.canvas_geo, text = 'Настройки GeoRitm')
        self.label_geo_header.config(font = 'Jost 22', fg = '#ffffff', bg = '#2f2f2f')
        self.label_geo_header.place(x = 186, y = 20, width = 281, height = 54)
        
        self.label_geo_ip = tk.Label(self.canvas_geo, image = self.img_oval_entry)
        self.label_geo_ip.place(x = 30, y = 86, width = 280, height = 43)

        self.entry_geo_ip = EntryWithPlaceholder(self.label_geo_ip, 'IP хоста', 'geo_ip', self.gui_settings)
        self.entry_geo_ip.place(x = 10, y = 0, width = 230, height = 40)

        self.label_geo_port = tk.Label(self.canvas_geo, image = self.img_oval_entry)
        self.label_geo_port.place(x = 30, y = 145, width = 280, height = 43)

        self.entry_geo_port = EntryWithPlaceholder(self.label_geo_port, 'Порт', 'geo_port', self.gui_settings)
        self.entry_geo_port.place(x = 10, y = 0, width = 230, height = 40)

        self.label_geo_login = tk.Label(self.canvas_geo, image = self.img_oval_entry)
        self.label_geo_login.place(x = 340, y = 86, width = 280, height = 43)

        self.entry_geo_login = EntryWithPlaceholder(self.label_geo_login, 'Логин', 'login_georitm', self.gui_settings)
        self.entry_geo_login.place(x = 10, y = 0, width = 230, height = 40)

        self.label_geo_pass = tk.Label(self.canvas_geo, image = self.img_oval_entry)
        self.label_geo_pass.place(x = 340, y = 145, width = 280, height = 43)

        self.entry_geo_pass = EntryWithPlaceholder(self.label_geo_pass, 'Пароль', 'password_georitm', self.gui_settings)
        self.entry_geo_pass.place(x = 10, y = 0, width = 230, height = 40)

        #ПАК ВсМК
        self.canvas_pak = tk.Canvas(self, height = 170, width = 652, bd = 0, highlightthickness = 0)
        self.canvas_pak_img = tk.PhotoImage(file = resource_path('img/frame_pak.png'))
        self.canvas_pak.create_image(0, 0, anchor = 'nw', image = self.canvas_pak_img)
        self.canvas_pak.place(x = 30, y = 270)

        self.label_pak_header = tk.Label(self.canvas_pak, text = 'Настройки ПАК ВсМК')
        self.label_pak_header.config(font = 'Jost 22', fg = '#ffffff', bg = '#2f2f2f')
        self.label_pak_header.place(x = 176, y = 20, width = 281, height = 54)
        
        self.label_pak_login = tk.Label(self.canvas_pak, image = self.img_oval_entry)
        self.label_pak_login.place(x = 30, y = 86, width = 280, height = 43)

        self.entry_pak_login = EntryWithPlaceholder(self.label_pak_login, 'Логин', 'username_pac', self.gui_settings)
        self.entry_pak_login.place(x = 10, y = 0, width = 230, height = 40)

        self.label_pak_pass = tk.Label(self.canvas_pak, image = self.img_oval_entry)
        self.label_pak_pass.place(x = 340, y = 86, width = 280, height = 43)

        self.entry_pak_pass = EntryWithPlaceholder(self.label_pak_pass, 'Пароль', 'password_pac', self.gui_settings)
        self.entry_pak_pass.place(x = 10, y = 0, width = 230, height = 40)

        #CobraIS
        self.canvas_cis = tk.Canvas(self, height = 230, width = 652, bd = 0, highlightthickness = 0)
        self.canvas_cis_img = tk.PhotoImage(file = resource_path('img/frame_cis.png'))
        self.canvas_cis.create_image(0, 0, anchor = 'nw', image = self.canvas_cis_img)
        self.canvas_cis.place(x = 30, y = 450)

        self.label_cis_header = tk.Label(self.canvas_cis, text = 'Настройки сервера CobraIS')
        self.label_cis_header.config(font = 'Jost 22', fg = '#ffffff', bg = '#2f2f2f')
        self.label_cis_header.place(x = 126, y = 20, width = 400, height = 54)
        
        self.label_cis_ip = tk.Label(self.canvas_cis, image = self.img_oval_entry)
        self.label_cis_ip.place(x = 30, y = 86, width = 280, height = 43)

        self.entry_cis_ip = EntryWithPlaceholder(self.label_cis_ip, 'IP хоста', 'host', self.gui_settings)
        self.entry_cis_ip.place(x = 10, y = 0, width = 230, height = 40)

        self.label_cis_port = tk.Label(self.canvas_cis, image = self.img_oval_entry)
        self.label_cis_port.place(x = 30, y = 145, width = 280, height = 43)

        self.entry_cis_port = EntryWithPlaceholder(self.label_cis_port, 'Порт', 'port', self.gui_settings)
        self.entry_cis_port.place(x = 10, y = 0, width = 230, height = 40)

        if self.running:
            self.label_cis_status = tk.Label(self.canvas_cis, text = 'Статус:  Сервер запущен')
        else:
            self.label_cis_status = tk.Label(self.canvas_cis, text = 'Статус:  Сервер остановлен')
        self.label_cis_status.config(font = 'Jost 12', fg = '#c1c1c1', bg = '#2f2f2f')
        self.label_cis_status.place(x = 340, y = 96)

        self.image_list = [tk.PhotoImage(file = resource_path('img/oval_button_start.png')),
                           tk.PhotoImage(file = resource_path('img/oval_button_stop.png'))]

        if self.running:
            self.img_oval_button = self.image_list[1]
        else:
            self.img_oval_button = self.image_list[0]
        self.label_cis_button = tk.Label(self.canvas_cis, image = self.img_oval_button)
        self.label_cis_button.place(x = 340, y = 145, width = 280, height = 43)
        self.label_cis_button.bind('<Button-1>', self.start_stop)

        self.img_save_button = tk.PhotoImage(file = resource_path('img/oval_button_save.png'))
        self.label_save_button = tk.Label(self, image = self.img_save_button)
        self.label_save_button.place(x = 215, y = 690, width = 280, height = 43)
        self.label_save_button.bind('<Button-1>', self.save_config)

        mainmenu = tk.Menu(self)
        self.config(menu = mainmenu) 
 
        licensemenu = tk.Menu(mainmenu, tearoff=0)
        licensemenu.add_command(label = 'Ввести ключ')

        helpmenu = tk.Menu(mainmenu, tearoff=0)
        helpmenu.add_command(label = 'О программе')
        helpmenu.add_command(label = 'Документация')
        
        mainmenu.add_cascade(label = 'Лицензия', menu = licensemenu)
        mainmenu.add_cascade(label = 'Справка', menu = helpmenu)

    def load_settings(self):
        # добавить проверку что папка существует
        if not os.path.exists(self.settings_file): #если файла настроек .ini еще нет        
            #проверяем есть ли наш контейнер
            name_container = 'cobrais'
            
            returned_output = cmd('docker ps -a')
            if f' {name_container}' in returned_output:
                #если есть копируем файл настроек из него
                cmds = f'docker cp {name_container}:/cobra/config/settings.ini c:\CobraIS'
                returned_output = cmd(cmds)
            else:
                #если контейнера нет то просто создаем пустой файл настроек
                open(self.settings_file, 'w').close()

        #загружаем настройки в гуи
        with open(self.settings_file, 'r') as file:
            lines = file.readlines()
            
        for i in range(0, len(lines)):
            line = lines[i]
            line = line[ : -1]
            if line != '':
                j = line.find('=')
                self.gui_settings[line[ : j-1]] = line[j+2 : ]
        s = self.gui_settings['url_api_georitm'][7 : -9]
        self.gui_settings['geo_ip'] = s[ : s.find(':')]
        self.gui_settings['geo_port'] = s[s.find(':')+1 : ]

    def start_stop(self, event):
        if self.running:
            returned_output = cmd('docker stop cobrais')
            print(f'{returned_output[ : -1]} stopped')
            if self.need_restart: #если нужна перезагрузка
                #остановить и удалить контейнер
                returned_output = cmd('docker rm cobrais')
                print(f'{returned_output[ : -1]} delete')
            
            self.running = False
            self.label_cis_button.config(image = self.image_list[0])
            self.label_cis_status.config(text = 'Статус:  Сервер остановлен')
        else: #сервер остановлен
            if self.need_restart: #если нужна перезагрузка
                returned_output = cmd('docker ps -a')
                if ' cobrais' in returned_output:
                    returned_output = cmd('docker rm cobrais')
                    print(f'{returned_output[ : -1]} delete')
                
                #пересобираем контейнер с новыми настройками сети
                host = self.gui_settings['host']
                port = self.gui_settings['port']
                cmds = f'docker create --name cobrais -v C:\CobraIS:/cobra/config -p {port}:{port} dpteam/cobra-integration-server'
                returned_output = cmd(cmds)
                print(f'{returned_output[ : -1]} create')
                returned_output = cmd('docker start cobrais')
                print(f'{returned_output[ : -1]} start')

                self.need_restart = False
            else:
                #если контейнера нет, то нужно его создать
                cmds = 'docker ps --format "table {{.Names}}" -a'
                returned_output = cmd(cmds)
                print(returned_output[ : -1])
                if 'cobrais' not in returned_output:
                    host = self.gui_settings['host']
                    port = self.gui_settings['port']
                    cmds = f'docker create --name cobrais -v C:\CobraIS:/cobra/config -p {port}:{port} --restart always dpteam/cobra-integration-server'
                    returned_output = cmd(cmds)
                    print(f'{returned_output[ : -1]} create')
                    
                #запускаем контейнер
                returned_output = cmd('docker start cobrais')
                print(f'{returned_output} start')
                
            
            self.running = True            
            self.label_cis_button.config(image = self.image_list[1])
            self.label_cis_status.config(text = 'Статус:  Сервер запущен')

    def save_config(self, event):
        temp = {}
        s = self.entry_cis_ip.get()
        temp['host'] = s[s.find(':')+2 : ]
        s = self.entry_cis_port.get()
        temp['port'] = s[s.find(':')+2 : ]
        geo_ip = self.entry_geo_ip.get()
        geo_port = self.entry_geo_port.get()
        temp['url_api_georitm'] = f'http://{geo_ip[10 : ]}:{geo_port[6 : ]}/restapi/'
        s = self.entry_geo_login.get()
        temp['login_georitm'] = s[s.find(':')+2 : ]
        s = self.entry_geo_pass.get()
        temp['password_georitm'] = s[s.find(':')+2 : ]
        s = self.entry_pak_login.get()
        temp['username_pac'] = s[s.find(':')+2 : ]
        s = self.entry_pak_pass.get()
        temp['password_pac'] = s[s.find(':')+2 : ]
        temp['url_api_pac'] = 'https://demo.pakvcmk.ru/api/'
        
        with open(self.settings_file, 'w') as file:
            for key, value in temp.items():
                file.write(f'{key} = {value}\n')
                
        if (self.gui_settings['host'] != temp['host']) or (self.gui_settings['port'] != temp['port']):
            #если были изменены настройки сервера кобраис то нужно пересобирать контейнер
            if self.running:
                self.label_cis_status.config(text = 'Статус: Требуется перезагрузка')
            self.need_restart = True
        
        self.gui_settings = temp

    def check_status(self):
        cmds = 'docker ps --format "table {{.Names}}"'
        returned_output = cmd(cmds)
        #print(returned_output)
        if 'cobrais' in returned_output:
            return True
        return False

if __name__ == "__main__":
    app = App()
    app.title('CobraIS Configuration')
    app.mainloop()
