import random
import tkinter as tk
from tkinter import messagebox, ttk


class File:
    def __init__(self, filename):
        self.filename = filename

    def __str__(self):
        return self.filename


class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.files = []

    def __str__(self):
        return self.user_id

    def add_file(self, file, access_level_name=str(), access_level_number=int()):
        self.files.append((file, access_level_name, access_level_number))


access = {
    0: 'Полный запрет',  # 000
    1: 'Передача прав',  # 001
    2: 'Запись',  # 010
    3: 'Запись, Передача прав',  # 011
    4: 'Чтение',  # 100
    5: 'Чтение, Передача прав',  # 101
    6: 'Чтение, Запись',  # 110
    7: 'Полный доступ'  # 111
}
access_reverse = {value: key for key, value in access.items()}

# Предопределенные пользователи (3):
users = [User("admin"), User('ivan'), User('guest')]

# Предопределенные файлы (5):
files = [File('file1'), File('file2'), File('file3'), File('file4'), File('file5')]

# Предопределенные права доступа к файлу у пользователей
for i in range(len(users)):
    for z in range(len(files)):
        if i == 0:
            users[i].add_file(files[z], access[7], 7)
        else:
            access_level = random.choice(list(access.keys()))
            users[i].add_file(files[z], access[access_level], access_level)


def centered_window(window, width=int(), height=int()):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_position = (screen_width - width) // 2
    y_position = (screen_height - height) // 2

    window.geometry(f"{width}x{height}+{x_position}+{y_position}")


def create_auth_window():
    root = tk.Tk()
    root.title("Авторизация пользователя")

    centered_window(root, 350, 150)
    frame_login = tk.Frame(root)
    label_login = tk.Label(frame_login, text="Введите имя пользователя:")
    entry_login = tk.Entry(frame_login)

    def login():
        username = entry_login.get()
        user = next((user for user in users if user.user_id == username), None)
        if user:
            root.withdraw()
            cur_user = user
            create_user_file_window(cur_user, window=root)
        else:
            messagebox.showerror('Ошибка', 'Такого пользователя не существует.')

    button_login = tk.Button(root, text="Войти", command=login, width=16)

    frame_login.pack(side='top', pady=15)
    label_login.pack(side='top')
    entry_login.pack(pady=5, side='top')
    button_login.pack(pady=5)

    root.mainloop()


def create_user_file_window(cur_user, window):
    user_file_window = tk.Toplevel(window)
    user_file_window.title("Таблица пользователей и файлов")
    centered_window(user_file_window, 960, 490)

    menu_frame = tk.Frame(user_file_window)
    menu_frame.pack(side='top', fill='x', padx=20, pady=(20, 0))

    current_user_label = tk.Label(menu_frame, text=f"Текущий пользователь: {str(cur_user)}")
    current_user_label.pack(side='left')

    def logout():
        user_file_window.destroy()
        create_auth_window()

    logout_button = tk.Button(menu_frame, text='Выйти', command=logout, width=20)
    logout_button.pack(side='right')

    table = ttk.Treeview(user_file_window, columns=('User', 'File1', 'File2', 'File3', 'File4', 'File5'),
                         show='headings', height=len(users))

    table.heading('User', text='Пользователь', anchor=tk.CENTER)
    table.heading('File1', text='Файл 1')
    table.heading('File2', text='Файл 2')
    table.heading('File3', text='Файл 3')
    table.heading('File4', text='Файл 4')
    table.heading('File5', text='Файл 5')

    for col in ('User', 'File1', 'File2', 'File3', 'File4', 'File5'):
        table.column(col, anchor=tk.CENTER)
        table.column(col, width=50)

    def update_table():
        for row in table.get_children():
            table.delete(row)

        for u in range(len(users)):
            values = [str(users[u])]
            for f in range(len(files)):
                access_level_name = (users[u].files[f][1])
                values.extend([access_level_name])
            table.insert('', 'end', values=values)

    update_table()
    table.pack(fill='both', side='top', pady=(20, 0), padx=20)

    usernames = [str(u) for u in users if u != cur_user]

    combobox_frame = tk.Frame(user_file_window)
    combobox_frame.pack(side='top', pady=5)

    combobox_users = ttk.Combobox(combobox_frame, values=usernames)
    combobox_users.pack(pady=5, padx=(4, 0))

    combobox_frame.place(relx=0.5, rely=0.38, anchor='center')

    def on_user_select(event):
        selected_user = combobox_users.get()
        refresh_files(selected_user)
        item_id = None
        for item in table.get_children():
            if table.item(item, 'values')[0] == selected_user:
                item_id = item
                break

        if item_id:
            table.selection_remove(table.selection())
            table.selection_add(item_id)

    combobox_users.bind("<<ComboboxSelected>>", on_user_select)

    user_files_label_frames = []
    full_options = []

    files_frame = tk.Frame(user_file_window)
    files_frame.pack(fill='x', pady=(0, 20), padx=20)

    def refresh_files(selected_user):
        for file_label_frame in user_files_label_frames:
            file_label_frame.destroy()

        for optns in full_options:
            for optn in optns[1:]:
                optn.destroy()

        user_files_label_frames.clear()
        full_options.clear()

        selected_user_obj = next((s for s in users if str(s) == selected_user), None)

        sel_user_file_accesses = [user_file[1] for user_file in selected_user_obj.files]

        for step, (cur_file, cur_access_user_name, cur_access_number) in enumerate(cur_user.files):
            if cur_access_number % 2 == 1:
                file_label_frame = ttk.LabelFrame(files_frame, text=f'Файл {step + 1}')
                file_label_frame.pack(side='left', padx=13)

                files_frame.place(rely=0.5, relx=0.02)

                options = [step]
                var_access = tk.StringVar()
                find = False

                def create_option(file_obj, access_name):
                    return lambda: handle_option_click(file_obj, access_name)

                def handle_option_click(file_obj, access_name):
                    cur_number = None
                    for cur_go, (cur_object_file, cur_acc_name, cur_acc_number) in enumerate(cur_user.files):
                        if file_obj == cur_object_file:
                            cur_number = cur_user.files[cur_go][2]
                    if cur_number is not None:
                        for go, (object_file, acc_name, acc_number) in enumerate(selected_user_obj.files):
                            if file_obj == object_file:
                                access_number = int(access_reverse[access_name])

                                if cur_number == 1:
                                    if access_number & 0b001 != 0:
                                        if (acc_name == 'Полный запрет' or acc_name == 'Запись'
                                                or acc_name == 'Чтение' or acc_name == 'Чтение, Запись'):
                                            if acc_number + 1 == access_number:
                                                selected_user_obj.files[go] = [file_obj, access[acc_number + 1],
                                                                               acc_number + 1]
                                                messagebox.showinfo('Успех', 'Вы успешно поменяли права '
                                                                             f'{selected_user_obj} на {cur_file}.')
                                            else:
                                                messagebox.showerror('Ошибка', 'У вас недостаточно прав!')
                                        else:
                                            messagebox.showerror('Ошибка', 'Невозможно выдать права!')
                                    else:
                                        messagebox.showerror('Ошибка', 'У вас недостаточно прав!')

                                elif cur_number == 3:
                                    if access_number & 0b010 != 0:
                                        if (acc_name == 'Полный запрет' or acc_name == 'Передача прав' or
                                                acc_name == 'Чтение'):
                                            if acc_number + 2 == access_number:
                                                selected_user_obj.files[go] = [file_obj, access[acc_number + 2],
                                                                               acc_number + 2]
                                                messagebox.showinfo('Успех', 'Вы успешно поменяли права '
                                                                             f'{selected_user_obj} на {cur_file}.')
                                            else:
                                                messagebox.showerror('Ошибка', 'У вас недостаточно прав!')
                                        else:
                                            messagebox.showerror('Ошибка', 'Невозможно выдать права!')
                                    else:
                                        messagebox.showerror('Ошибка', 'У вас недостаточно прав!')

                                elif cur_number == 5:
                                    if access_number & 0b100 != 0:
                                        if (acc_name == 'Полный запрет' or acc_name == 'Передача прав'
                                                or acc_name == 'Запись' or acc_name == 'Запись, Передача прав'):
                                            if acc_number + 4 == access_number:
                                                selected_user_obj.files[go] = [file_obj, access[acc_number + 4],
                                                                               acc_number + 4]
                                                messagebox.showinfo('Успех', 'Вы успешно поменяли права '
                                                                             f'{selected_user_obj} на {cur_file}.')
                                            else:
                                                messagebox.showerror('Ошибка', 'У вас недостаточно прав!')
                                        else:
                                            messagebox.showerror('Ошибка', 'Невозможно выдать права!')
                                    else:
                                        messagebox.showerror('Ошибка', 'У вас недостаточно прав!')

                                elif cur_number == 7:
                                    selected_user_obj.files[go] = [file_obj, access_name, int(access_number)]
                                    messagebox.showinfo('Успех', 'Вы успешно поменяли права '
                                                                 f'{selected_user_obj} на {cur_file}.')
                                else:
                                    messagebox.showerror('Ошибка', 'У вас недостаточно прав!')
                                refresh_files(selected_user)
                                update_table()
                                selected = combobox_users.get()
                                refresh_files(selected)
                                item_id = None
                                for item in table.get_children():
                                    if table.item(item, 'values')[0] == selected:
                                        item_id = item
                                        break

                                if item_id:
                                    table.selection_remove(table.selection())
                                    table.selection_add(item_id)

                for acc in access.values():
                    option = tk.Radiobutton(file_label_frame, text=acc, value=acc, variable=var_access,
                                            command=create_option(cur_file, acc))
                    option.pack(anchor='w')
                    options.append(option)
                    if sel_user_file_accesses[step] in option['text'] and find is False:
                        option.select()
                        find = True

                user_files_label_frames.append(file_label_frame)
                full_options.append(options)

    user_file_window.mainloop()


def start():
    create_auth_window()


start()
