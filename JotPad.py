from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

def save_file():
    filename = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')])
    if filename:
        with open(filename, 'w') as f:
            f.write(text_field.get('1.0', 'end'))

def open_file():
    filename = filedialog.askopenfilename(defaultextension='.txt', filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')])
    if filename:
        with open(filename, 'r') as f:
            text_field.delete('1.0', 'end')
            text_field.insert('1.0', f.read())

root = Tk()
# Заголовок
root.title('Блокнот')
# Разрешение окна
root.geometry('600x700')

text_frame = Frame(root)
# Расположение виджета Frame в окне
text_frame.pack(fill=BOTH, expand=1)

text_field = Text(text_frame,
                 bg='black',
                 fg='lime',
                 padx=10,
                 pady=10,
                 wrap=WORD,
                 insertbackground='brown',
                 selectbackground='#8D917A',
                 spacing3=10,
                 width=30,
                 font='Arial 14 bold'
                 )
text_field.pack(expand=1, fill=BOTH, side=LEFT)

# Создание кнопки сохранения файла
save_button = Button(root, text='Сохранить', command=save_file)
save_button.pack(side=LEFT)

# Создание кнопки открытия файла
open_button = Button(root, text='Открыть', command=open_file)
open_button.pack(side=LEFT)

try:
    # Запуск главного цикла
    root.mainloop()
except Exception as e:
    messagebox.showerror('Ошибка', f'Произошла ошибка: {e}')
