from tkinter import *
import ctypes
import re
import os
import json
from tkinter import messagebox

__name__ == "__main__"

#Меню "О программе"
def aboutp(self):
    about_text = """
    Название программы: KirCode
    Версия: 1.1
    Автор: Ваше имя
    Дата создания: 2025
    Описание: Графический текстовый редактор с открытым исходным кодом.
    """
    messagebox.showinfo("О программе", about_text)

#Файл Конфига
def rgb(rgb_tuple):
    """Конвертирует кортеж RGB в шестнадцатеричный формат для Tkinter"""
    return "#%02x%02x%02x" % rgb_tuple

class ColorConfig:
    def __init__(self, config_path='config.json'):
        self.config_path = config_path
        self.config = self.load_config()
        
    def load_config(self):
        """Загружает конфиг из JSON-файла"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # Создаем конфиг с настройками по умолчанию, если файла нет
            default_config = {
                "colors": {
                    "normal": [234, 234, 234],
                    "keywords": [234, 95, 95],
                    "comments": [95, 234, 165],
                    "string": [234, 162, 95],
                    "function": [95, 211, 234],
                    "background": [42, 42, 42]
                },
                "font": "Consolas 15"
            }
            self.save_config(default_config)
            return default_config
    
    def save_config(self, config=None):
        """Сохраняет конфиг в JSON-файл"""
        if config is None:
            config = self.config
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
    
    def get_color(self, name):
        """Возвращает цвет в формате Tkinter"""
        rgb_tuple = tuple(self.config['colors'][name])
        return rgb(rgb_tuple)
    
    def get_font(self):
        """Возвращает настройки шрифта"""
        return self.config['font']
    
    def update_color(self, name, rgb_values):
        """Обновляет цвет в конфиге"""
        self.config['colors'][name] = rgb_values
        self.save_config()

#Сохранение Файла
def savef(event=None):
    with open('file.txt', 'w', encoding='utf-8') as f:
        f.write(editArea.get('1.0', END))

#Горячие клавиши
def ctrlcvx(e):
    if e.keycode == 86 and e.keysym != 'v':
        cmd_paste()
    elif e.keycode == 67 and e.keysym != 'c':
        cmd_copy()
    elif e.keycode == 88 and e.keysym != 'x':
        cmd_cut()
def pythontest(event=None):
    with open('project.py', 'w', encoding='utf-8') as f:
        f.write(editArea.get('1.0', END))

    os.system('start cmd /K "python project.py"')
    editArea.insert('1.0', """saved
    """)

def changes(event=None):
    global previousText

    if editArea.get('1.0', END) == previousText:
        return

    for tag in editArea.tag_names():
        editArea.tag_remove(tag, "1.0", "end")

    i = 0
    for pattern, color in repl:
        for start, end in search_re(pattern, editArea.get('1.0', END)):
            editArea.tag_add(f'{i}', start, end)
            editArea.tag_config(f'{i}', foreground=color)

            i += 1

    previousText = editArea.get('1.0', END)

def search_re(pattern, text):
    matches = []
    text = text.splitlines()

    for i, line in enumerate(text):
        for match in re.finditer(pattern, line):

            matches.append(
                (f"{i + 1}.{match.start()}", f"{i + 1}.{match.end()}")
            )

    return matches

def rgb(rgb):
    return "#%02x%02x%02x" % rgb

ctypes.windll.shcore.SetProcessDpiAwareness(True)

root = Tk()
root.geometry('700x500')
root.title('KirCode 1.1')
previousText = ''

#normal = rgb((234, 234, 234))
#keywords = rgb((234, 95, 95))
#comments = rgb((95, 234, 165))
#string = rgb((234, 162, 95))
#function = rgb((95, 211, 234))
# Также определим цвет фона и шрифт
#background = rgb((42, 42, 42))
#font = 'Consolas 15'

if __name__ == "__main__":
    config = ColorConfig()
    
    # Получаем цвета
    normal = config.get_color('normal')
    keywords = config.get_color('keywords')
    comments = config.get_color('comments')
    string = config.get_color('string')
    function = config.get_color('function')
    background = config.get_color('background')
    font = config.get_font()
    
    print("Normal color:", normal)
    print("Font:", font)

repl = [
    ['(^| )(False|None|True|and|as|assert|async|await|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)($| )', keywords],
    ['".*?"', string],
    ['\'.*?\'', string],
    ['#.*?$', comments],
]

editArea = Text(
    root, background=background, foreground=normal, insertbackground=normal, relief=FLAT, borderwidth=30, font=font
)

editArea.pack(fill=BOTH, expand=1)

editArea.insert('1.0', """
""")

editArea.bind('<KeyRelease>', changes)
root.bind("<Control-KeyPress>", ctrlcvx)
root.bind('<Control-t>', pythontest)
root.bind('<Control-s>', savef)
root.bind('<Control-o>', aboutp)

changes()
root.mainloop()
