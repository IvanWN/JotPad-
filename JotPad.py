from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

# Создание тем
themes = {
    'Стандартная': {
        'bg': 'white',
        'fg': 'black',
        'insertbackground': 'black',
        'selectbackground': '#C4C4C4'
    },
    'Тёмная': {
        'bg': 'black',
        'fg': 'white',
        'insertbackground': 'white',
        'selectbackground': '#8D917A'
    }
}

# Создание шрифтов
fonts = ['Arial 14 bold', 'Courier 12', 'Times 16 italic']
current_font = 'Times 16 italic'

def set_theme(theme):
    theme_params = themes[theme]
    text_field.config(bg=theme_params['bg'],
                      fg=theme_params['fg'],
                      insertbackground=theme_params['insertbackground'],
                      selectbackground=theme_params['selectbackground'])

def set_font(font):
    global current_font
    current_font = font
    text_field.tag_configure("font", font=current_font)
    text_field.tag_add("font", "1.0", "end")

def save_file():
    text = text_field.get('1.0', 'end').strip()
    if text:
        filename = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')])
        if filename:
            with open(filename, 'w') as f:
                f.write(f"{{\n{text}\nfont='{current_font}'\n}}")
    else:
        messagebox.showwarning('Предупреждение', 'Нельзя сохранять пустой файл!')


def open_file():
    global current_font
    filename = filedialog.askopenfilename(defaultextension='.txt', filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')])
    if filename:
        with open(filename, 'r') as f:
            text = f.read()
            current_font_pattern = re.search(r'font=\{(.*)\}', text)
            if current_font_pattern:
                current_font = current_font_pattern.group(1)
                text = re.sub(r'font=\{.*\}', '', text)
            text_field.delete('1.0', 'end')
            text_field.insert('1.0', text)
            text_field.tag_configure("font", font=current_font)
            text_field.tag_add("font", "1.0", "end")

root = Tk()
# Заголовок
root.title('Блокнот')
# Разрешение окна
root.geometry('600x700')

# Создание меню
menu_bar = Menu(root)

# Создание вкладки "Файл"
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='Открыть', command=open_file)
file_menu.add_command(label='Сохранить', command=save_file)
file_menu.add_separator()
file_menu.add_command(label='Закрыть', command=root.quit)
menu_bar.add_cascade(label='Файл', menu=file_menu)

# Создание вкладки "Вид"
view_menu = Menu(menu_bar, tearoff=0)
theme_menu = Menu(view_menu, tearoff=0)
for theme in themes.keys():
    theme_menu.add_command(label=theme, command=lambda t=theme: set_theme(t))
view_menu.add_cascade(label='Тема', menu=theme_menu)
font_menu = Menu(view_menu, tearoff=0)
for font in fonts:
    font_menu.add_command(label=font, command=lambda f=font: set_font(f))
view_menu.add_cascade(label='Шрифт', menu=font_menu)
menu_bar.add_cascade(label='Вид', menu=view_menu)

# Установка созданного меню в окне
root.config(menu=menu_bar)

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
                 font=current_font
                 )
text_field.pack(expand=1, fill=BOTH, side=LEFT)
set_theme("Стандартная")

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
