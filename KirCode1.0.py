from tkinter import *
import ctypes
import re
import os

def savef(event=None):
    with open('file.txt', 'w', encoding='utf-8') as f:
        f.write(editArea.get('1.0', END))

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
root.title('KirCode 1.0')
previousText = ''

normal = rgb((234, 234, 234))
keywords = rgb((234, 95, 95))
comments = rgb((95, 234, 165))
string = rgb((234, 162, 95))
function = rgb((95, 211, 234))
# Также определим цвет фона и шрифт
background = rgb((42, 42, 42))
font = 'Consolas 15'

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

changes()
root.mainloop()