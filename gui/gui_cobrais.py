import tkinter as tk
import tkinter.font as font

from PIL import Image, ImageTk

import os

def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master = None, placeholder = None):
        super().__init__(master)

        if placeholder is not None:
            self.placeholder = placeholder
            self.placeholder_color = '#787878'
            self.default_fg_color = self['fg']

            self.bind("<FocusIn>", self.focus_in)
            self.bind("<FocusOut>", self.focus_out)

            self.put_placeholder()

        self.config(bg = '#f0f0f0', relief = tk.FLAT, font = 'Jost 14')

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def focus_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def focus_out(self, *args):
        if not self.get():
            self.put_placeholder()

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        w = 784
        h = 680
 
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
 
        x = int((sw - w) / 2)
        y = int((sh - h) / 2)
        
        self.geometry(f'{w}x{h}+{x}+{y}')
        self.resizable(False, False)
        self.config(bg = '#292929')

##        appImgP = tk.PhotoImage(file = resource_path('logo64.ico'))
##        self.iconphoto(0, appImgP)

        self.running = False

        self.img_oval_entry = tk.PhotoImage(file = 'img/oval_entry.png')

        #GeoRitm
        self.canvas_geo = tk.Canvas(self, height = 290, width = 344, bd = 0, highlightthickness = 0)#344
        self.canvas_geo_img = tk.PhotoImage(file = 'img/frame_geo.png')
        self.canvas_geo.create_image(0, 0, anchor = 'nw', image = self.canvas_geo_img)
        self.canvas_geo.place(x = 42, y = 42)

        self.label_geo_header = tk.Label(self.canvas_geo, text = 'Настройки GeoRitm')
        self.label_geo_header.config(font = 'Jost 22', fg = '#ffffff', bg = '#2f2f2f')
        self.label_geo_header.place(x = 32, y = 20, width = 281, height = 54)
        
        self.label_geo_ip = tk.Label(self.canvas_geo, image = self.img_oval_entry)
        self.label_geo_ip.place(x = 30, y = 86, width = 280, height = 43)

        self.entry_geo_ip = EntryWithPlaceholder(self.label_geo_ip, 'IP хоста')
        self.entry_geo_ip.place(x = 10, y = 0, width = 230, height = 40)

        self.label_geo_login = tk.Label(self.canvas_geo, image = self.img_oval_entry)
        self.label_geo_login.place(x = 30, y = 145, width = 280, height = 43)

        self.entry_geo_login = EntryWithPlaceholder(self.label_geo_login, 'Логин')
        self.entry_geo_login.place(x = 10, y = 0, width = 230, height = 40)

        self.label_geo_pass = tk.Label(self.canvas_geo, image = self.img_oval_entry)
        self.label_geo_pass.place(x = 30, y = 204, width = 280, height = 43)

        self.entry_geo_pass = EntryWithPlaceholder(self.label_geo_pass, 'Пароль')
        self.entry_geo_pass.place(x = 10, y = 0, width = 230, height = 40)

        #ПАК ВсМК
        self.canvas_pak = tk.Canvas(self, height = 230, width = 344, bd = 0, highlightthickness = 0)
        self.canvas_pak_img = tk.PhotoImage(file = 'img/frame_pak.png')
        self.canvas_pak.create_image(0, 0, anchor = 'nw', image = self.canvas_pak_img)
        self.canvas_pak.place(x = 400, y = 42)

        self.label_pak_header = tk.Label(self.canvas_pak, text = 'Настройки ПАК ВсМК')
        self.label_pak_header.config(font = 'Jost 22', fg = '#ffffff', bg = '#2f2f2f')
        self.label_pak_header.place(x = 32, y = 20, width = 281, height = 54)
        
        self.label_pak_login = tk.Label(self.canvas_pak, image = self.img_oval_entry)
        self.label_pak_login.place(x = 30, y = 86, width = 280, height = 43)

        self.entry_pak_login = EntryWithPlaceholder(self.label_pak_login, 'Логин')
        self.entry_pak_login.place(x = 10, y = 0, width = 230, height = 40)

        self.label_pak_pass = tk.Label(self.canvas_pak, image = self.img_oval_entry)
        self.label_pak_pass.place(x = 30, y = 145, width = 280, height = 43)

        self.entry_pak_pass = EntryWithPlaceholder(self.label_pak_pass, 'Пароль')
        self.entry_pak_pass.place(x = 10, y = 0, width = 230, height = 40)

        #CobraIS
        self.canvas_cis = tk.Canvas(self, height = 230, width = 702, bd = 0, highlightthickness = 0)
        self.canvas_cis_img = tk.PhotoImage(file = 'img/frame_cis.png')
        self.canvas_cis.create_image(0, 0, anchor = 'nw', image = self.canvas_cis_img)
        self.canvas_cis.place(x = 42, y = 350)

        self.label_cis_header = tk.Label(self.canvas_cis, text = 'Настройки сервера CobraIS')
        self.label_cis_header.config(font = 'Jost 22', fg = '#ffffff', bg = '#2f2f2f')
        self.label_cis_header.place(x = 150, y = 20, width = 400, height = 54)
        
        self.label_cis_ip = tk.Label(self.canvas_cis, image = self.img_oval_entry)
        self.label_cis_ip.place(x = 30, y = 86, width = 280, height = 43)

        self.entry_cis_ip = EntryWithPlaceholder(self.label_cis_ip, 'IP хоста')
        self.entry_cis_ip.place(x = 10, y = 0, width = 230, height = 40)

        self.label_cis_port = tk.Label(self.canvas_cis, image = self.img_oval_entry)
        self.label_cis_port.place(x = 30, y = 145, width = 280, height = 43)

        self.entry_cis_port = EntryWithPlaceholder(self.label_cis_port, 'Порт')
        self.entry_cis_port.place(x = 10, y = 0, width = 230, height = 40)

        self.label_cis_status = tk.Label(self.canvas_cis, text = 'Статус:  Сервер остановлен')
        self.label_cis_status.config(font = 'Jost 12', fg = '#c1c1c1', bg = '#2f2f2f')
        self.label_cis_status.place(x = 390, y = 96)

##        self.btn_start_stop = tk.Button(self.canvas_cis, image = self.img_oval_button, command = self.start_stop)
##        #self.btn_start_stop = tk.Button(self.canvas_cis, command = self.start_stop)
##        self.btn_start_stop.config(text = 'ЗАПУСИТЬ', bd = 0, highlightthickness = 0, relief = 'flat')
##        self.btn_start_stop.place(x = 390, y = 145)

        self.image_list = [tk.PhotoImage(file = resource_path('img/oval_button_start.png')),
                           tk.PhotoImage(file = resource_path('img/oval_button_stop.png'))]
        self.img_oval_button = self.image_list[0]
        self.label_cis_button = tk.Label(self.canvas_cis, image = self.img_oval_button)
        self.label_cis_button.place(x = 390, y = 145, width = 280, height = 43)
        self.label_cis_button.bind('<Button-1>', self.start_stop)

        self.img_save_button = tk.PhotoImage(file = resource_path('img/oval_button_save.png'))
        self.label_save_button = tk.Label(self, image = self.img_save_button)
        self.label_save_button.place(x = 260, y = 600, width = 280, height = 43)
        self.label_save_button.bind('<Button-1>', self.save_config)

##        self.btn_save = tk.Button(self, text = 'Сохранить\nнастройки', command = self.save_config)
##        self.btn_save['font'] = font.Font(size = 16)
##        self.btn_save.place(x = 244, y = 180)

        mainmenu = tk.Menu(self)
        self.config(menu = mainmenu) 
 
        licensemenu = tk.Menu(mainmenu, tearoff=0)
        licensemenu.add_command(label = 'Ввести ключ')

        helpmenu = tk.Menu(mainmenu, tearoff=0)
        helpmenu.add_command(label = 'О программе')
        helpmenu.add_command(label = 'Документация')
        
        mainmenu.add_cascade(label = 'Лицензия', menu = licensemenu)
        mainmenu.add_cascade(label = 'Справка', menu = helpmenu)

    def start_stop(self, event):
        if self.running:
            self.running = False
            self.label_cis_button.config(image = self.image_list[0])
            self.label_cis_status.config(text = 'Статус:  Сервер остановлен')
        else:
            self.running = True
            self.label_cis_button.config(image = self.image_list[1])
            self.label_cis_status.config(text = 'Статус:  Сервер запущен')

    def save_config(self, event):
        pass
        


if __name__ == "__main__":
    app = App()
    app.title('CobraIS Configuration')
    app.mainloop()
