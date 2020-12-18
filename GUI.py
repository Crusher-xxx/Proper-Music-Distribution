import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
import ListenerStorage
import Listener
import pathlib


class UserSelection:  # Страница авторизации
    def __init__(self):
        self.frame = tk.Frame(root)
        self.frame.grid(row=0, column=0)

        # Окно авторизации
        self.title = tk.Label(self.frame, text='Авторизация', font=(None, 14))
        self.title.grid(row=0, column=0, columnspan=2)

        # Окно выбора пользователя
        self.prompt = tk.Label(self.frame, text='Введите ID слушателя')
        self.prompt.grid(row=1, column=0)
        self.field = tk.Entry(self.frame)
        self.field.grid(row=1, column=1)
        self.button_enter = tk.Button(self.frame, text='Войти', command=self.enter)
        self.button_enter.grid(row=2, column=1, padx=10, pady=10)

        self.message = tk.Message(self.frame, text='или')
        self.message.grid(row=4, column=1)

        self.button_new = tk.Button(self.frame, text='Создать нового пользователя', command=self.new)
        self.button_new.grid(row=5, column=1, padx=10, pady=10)

    def enter(self):
        user = None
        try:
            for listener in listeners:
                if listener.ID == int(self.field.get()):
                    user = listener
        except ValueError:
            pass

        if user is not None:
            self.frame.destroy()
            UserMenu(user)
        else:
            tk.messagebox.showerror('Ошибка', 'Неправильный ID')

    def new(self):
        self.frame.destroy()
        UserCreation()


class UserCreation:  # Страница создания пользователя
    def __init__(self):
        self.frame = tk.Frame(root)
        self.frame.grid(row=0, column=0)

        self.title = tk.Label(self.frame, text='Создать нового пользователя', font=(None, 14))
        self.title.grid(row=0, column=0, columnspan=2)

        # Окно ввода информации
        self.prompt_name = tk.Label(self.frame, text='Введите имя')
        self.prompt_name.grid(row=1, column=0)
        self.field_name = tk.Entry(self.frame)
        self.field_name.grid(row=1, column=1, pady=5)

        self.prompt_gender = tk.Label(self.frame, text='Выберите пол')
        self.prompt_gender.grid(row=2, column=0, pady=5)
        self.genders = ['m', 'f']
        self.select_gender = ttk.Combobox(self.frame, values=self.genders, width=15, state='readonly')
        self.select_gender.grid(row=2, column=1)

        # Кнопки подтверждения и возврата
        self.button_create = tk.Button(self.frame, text='Создать', command=self.create)
        self.button_create.grid(row=3, column=1, padx=10, pady=10)
        self.button_back = tk.Button(self.frame, text='Назад', command=self.back)
        self.button_back.grid(row=3, column=0, padx=10, pady=10)

    def back(self):
        self.frame.destroy()
        UserSelection()

    def create(self):
        if self.field_name.get() and self.select_gender.get():
            last_id = listeners[-1].ID
            listeners.append(Listener.Listener(last_id + 1, self.field_name.get(), self.select_gender.get()))
            listeners.save()

            user_selection = UserSelection()
            user_selection.field.insert(0, listeners[-1].ID)
            user_selection.enter()
        else:
            tk.messagebox.showerror('Ошибка', 'Введите имя и выберите пол')


class UserMenu:  # Главная страница
    def __init__(self, user: Listener.Listener):
        self.frame = tk.Frame(root)
        self.frame.grid(row=0, column=0)
        self.user = user

        # Область пользователя
        self.frame_user_menu = tk.Frame(self.frame)
        self.frame_user_menu.grid(row=0, column=0, sticky='NW')
        # Имя пользователя
        self.label_user = tk.Label(self.frame_user_menu, text=f'Пользователь: {user.name} [{user.ID}]', font=(None, 14))
        self.label_user.grid(row=0, column=0, padx=5, pady=3, sticky='N')
        # Кнопка выхода
        self.button_exit = tk.Button(self.frame_user_menu, text='Выйти', command=self.exit)
        self.button_exit.grid(row=0, column=1, padx=5, pady=5, sticky='N')
        # Опции пользователя
        self.button_update_stats = tk.Button(self.frame_user_menu, text='Обновить статистику', command=self.update)
        self.button_update_stats.grid(row=1, column=0, sticky='NW', padx=5, pady=5)
        self.button_activate_subscription = tk.Button(self.frame_user_menu, text='Активировать подписку',
                                                      command=self.activate)
        self.button_activate_subscription.grid(row=2, column=0, sticky='NW', padx=5, pady=5)
        # Плеер
        self.label_music_selection = tk.Label(self.frame_user_menu, text='Выберите трек:')
        self.label_music_selection.grid(row=3, column=0, sticky='W', padx=5)
        self.combobox_track = ttk.Combobox(self.frame_user_menu, state='readonly', width=30, values=tracks)
        self.combobox_track.grid(row=4, column=0, sticky='W', padx=5, pady=5)
        self.combobox_track.bind("<<ComboboxSelected>>", self.unlock_play)
        self.button_play = tk.Button(self.frame_user_menu, text='Play', command=self.play)
        self.button_play.grid(row=4, column=1)
        self.button_play.configure(state='disabled')


        # Область статистики
        self.frame_stats = tk.Frame(self.frame)
        self.frame_stats.grid(row=0, column=2)
        # Окно статистики
        self.stats_label = tk.Label(self.frame_stats, text='Статистика', font=(None, 14))
        self.stats_label.grid(row=0, column=0, pady=5)
        self.stats_text = tk.Text(self.frame_stats)
        self.stats_text.grid(row=1, column=0)
        self.stats_text.insert(1.0, self.user.get_report())
        self.stats_text.configure(state='disabled')
        # Скроллбары статистики
        self.horiz_scroll = tk.Scrollbar(self.frame_stats, orient='horizontal')
        self.horiz_scroll.grid(row=2, column=0, sticky='NSEW')
        self.vert_scroll = tk.Scrollbar(self.frame_stats, orient='vertical')
        self.vert_scroll.grid(row=1, column=1, sticky='NSEW')
        self.stats_text.configure(xscrollcommand=self.horiz_scroll.set, yscrollcommand=self.vert_scroll.set)

    def exit(self):
        self.frame.destroy()
        UserSelection()

    def update(self):
        self.stats_text.configure(state='normal')
        self.stats_text.delete(1.0, 'end')
        self.stats_text.insert(1.0, self.user.get_report())
        self.stats_text.configure(state='disabled')

    def activate(self):
        if self.user.get_subscription_status() == 'active':
            tk.messagebox.showerror('Ошибка', 'Подписка уже активна')
        else:
            self.user.activate_subscription()
            listeners.save()
            self.update()

    def unlock_play(self, event=None):
        self.button_play.configure(state='normal')

    def play(self):
        if self.user.get_subscription_status() == 'active':
            self.user.add_listening_time(self.combobox_track.get(), 3)
            listeners.save()
            self.update()
        else:
            tk.messagebox.showerror('Ошибка', 'У вас нет подписки')


if __name__ == '__main__':
    root = tk.Tk()  # Создать окно
    root.title('Proper Music Distribution')  # Заголовок окна
    # root.geometry('800x600')  # Задать ширину и высоту окна

    listeners = ListenerStorage.ListenerStorage(pathlib.Path(__file__).parent / 'data.json')
    listeners.load()

    tracks = ['Sum 41', 'Pendulum', 'Slipknot', 'Eskimo Callboy', 'Oomph!']
    UserSelection()
    root.mainloop()