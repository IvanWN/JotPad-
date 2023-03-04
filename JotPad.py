from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import re

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

# Создание стека для хранения истории изменений
history_stack = []

def save_history():
    # Сохранение текущего состояния текстового поля в стеке
    history_stack.append(text_field.get('1.0', 'end'))

def undo_last_action():
    if len(history_stack) > 1:
        # Получение текущего состояния текстового поля
        curr_text = text_field.get('1.0', 'end')
        # Если текущий текст не равен последнему сохраненному состоянию
        if curr_text != history_stack[-1]:
            # Сохранение текущего состояния текстового поля
            save_history()
        # Удаление текущего состояния текстового поля из стека
        history_stack.pop()
        # Получение предыдущего состояния текстового поля
        prev_text = history_stack[-1]
        # Установка предыдущего состояния текстового поля
        text_field.delete('1.0', 'end')
        text_field.insert('1.0', prev_text)

# Добавление текущего состояния текстового поля в стек при изменении текста
text_field.bind("<KeyRelease>", lambda event: save_history())

def on_key_press(event):
    if event.state == 4 and event.keysym == 'z':
        undo_last_action()

# Сохранение начального состояния текстового поля
save_history()

# Привязка функции on_key_press к событию нажатия клавиши
text_field.bind('<Key>', on_key_press)

# Создание кнопки сохранения файла
save_button = Button(root, text='Сохранить', command=save_file)
save_button.pack(side=LEFT)

# Создание кнопки открытия файла
open_button = Button(root, text='Открыть', command=open_file)
open_button.pack(side=LEFT)

# Функция для поиска и выделения текста
def search_text():
    search_string = search_entry.get()
    if search_string:
        start_pos = '1.0'
        positions = []
        while True:
            # Поиск вхождений заданного текста в текстовом поле
            search_index = text_field.search(search_string, start_pos, stopindex=END)
            if not search_index:
                break
            end_pos = f"{search_index}+{len(search_string)}c"
            positions.append(search_index)
            text_field.tag_add("search", search_index, end_pos)
            start_pos = end_pos
        if positions:
            text_field.tag_config("search", background="green", foreground="white")
            text_field.focus_set()
            text_field.tag_raise("search")
            return positions
        else:
            messagebox.showinfo("Нет совпадений", "Не удалось найти совпадения.")

def highlight_next(delta):
    search_string = search_entry.get()
    if search_string:
        if not hasattr(highlight_next, "positions"):
            highlight_next.positions = search_text()
            if not highlight_next.positions:
                return
            highlight_next.current = -1
        highlight_next.current = (highlight_next.current + delta) % len(highlight_next.positions)
        pos = highlight_next.positions[highlight_next.current]
        text_field.tag_remove("current", "1.0", END)
        text_field.tag_add("current", pos, f"{pos}+{len(search_string)}c")
        text_field.focus_set()
        text_field.tag_raise("current")

def search(event=None):
    search_text()

root.bind('<Control-f>', search)

# Создание поля ввода и кнопки "поиск"
search_frame = Frame(root, bg='lightgray', height=30)
search_frame.pack(side=TOP, fill=X)
search_frame.place(relx=1.0, y=0, anchor=NE)

search_entry = Entry(search_frame, bg='white', width=30)
search_entry.pack(side=LEFT, padx=5)

search_button = Button(search_frame, text='Найти', command=search_text)
search_button.pack(side=LEFT, padx=5)

try:
    # Запуск главного цикла
    root.mainloop()
except Exception as e:
    messagebox.showerror('Ошибка', f'Произошла ошибка: {e}')
