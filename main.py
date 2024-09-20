import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageDraw, ImageFont, ImageTk
import random
import string
from datetime import datetime
import client_form
import master_form
import operator_form
from ttkbootstrap import Style

# Данные пользователей
users_info = {
    "log11": {"password": "pass11", "fio": "Григорьев Семён Викторович", "role": "Клиент"},
    "log12": {"password": "pass12", "fio": "Сорокин Дмитрий Ильич", "role": "Клиент"},
    "log13": {"password": "pass13", "fio": "Белоусов Егор Ярославович", "role": "Клиент"},
    "log14": {"password": "pass14", "fio": "Суслов Михаил Александрович", "role": "Клиент"},
    "log2": {"password": "pass2", "fio": "Ильин Александр Андреевич", "role": "Мастер"},
    "log3": {"password": "pass3", "fio": "Никифоров Иван Дмитриевич", "role": "Мастер"},
    "log15": {"password": "pass15", "fio": "Васильев Вячеслав Александрович", "role": "Мастер"},
    "log4": {"password": "pass4", "fio": "Елисеев Артём Леонидович", "role": "Оператор"},
    "log5": {"password": "pass5", "fio": "Титов Сергей Кириллович", "role": "Оператор"},
    "log1": {"password": "pass1", "fio": "Носов Иван Михайлович", "role": "Менеджер"}
}

# Глобальные переменные для капчи и блокировок
attempts = 0
lockout = False
captcha_displayed = False

def generate_captcha():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def create_captcha_image(captcha_text):
    width, height = 200, 80
    image = Image.new('RGB', (width, height), 'white')
    font = ImageFont.load_default()
    draw = ImageDraw.Draw(image)
    for i, char in enumerate(captcha_text):
        draw.text((20 + i * 30, 20), char, font=font, fill='black')
    for _ in range(5):
        draw.line(((random.randint(0, width), random.randint(0, height)),
                    (random.randint(0, width), random.randint(0, height))), fill="black", width=2)
    return ImageTk.PhotoImage(image)

def start_timer():
    global lockout
    lockout = True
    button_login.config(state=tk.DISABLED, bootstyle="secondary")
    countdown(180)

def countdown(time_remaining):
    if time_remaining > 0:
        timer_label.config(text=f"Попробуйте снова через: {time_remaining // 60}:{time_remaining % 60:02}")
        root.after(1000, countdown, time_remaining - 1)
    else:
        unlock_interface()

def unlock_interface():
    global attempts, lockout
    attempts = 0
    lockout = False
    timer_label.config(text="")
    entry_login.config(state=tk.NORMAL)
    entry_password.config(state=tk.NORMAL)
    button_login.config(state=tk.NORMAL, bootstyle="success")
    entry_captcha.config(state=tk.NORMAL)

def show_captcha():
    captcha_value.set(generate_captcha())
    captcha_image = create_captcha_image(captcha_value.get())
    captcha_label.config(image=captcha_image)
    captcha_label.image = captcha_image

def refresh_captcha_code():
    show_captcha()

def login():
    global attempts, captcha_displayed
    if lockout:
        return

    username = entry_login.get()
    password = entry_password.get()

    # Проверка правильности логина и пароля
    if username in users_info and users_info[username]["password"] == password:
        user_info = users_info[username]
        fio = user_info["fio"]
        role = user_info["role"]

        messagebox.showinfo("Успех", f"Добро пожаловать, {role} {fio}!")
        root.withdraw()  # Скрываем окно авторизации
        if role == "Клиент":
            client_form.open_client_form(root, fio)
        elif role == "Мастер":
            master_form.open_master_form(root, fio)
        elif role == "Оператор":
            operator_form.open_operator_form(root, fio)
        elif role == "Менеджер":
            import manager_form
            manager_form.open_manager_form(root, fio)

        # Сбрасываем попытки и скрываем капчу после успешного входа
        attempts = 0
        captcha_displayed = False
        button_login.config(bootstyle='success')
        entry_captcha.pack_forget()  # Скрыть поле капчи
        refresh_captcha.pack_forget()  # Скрыть кнопку обновления капчи
        captcha_label.pack_forget()  # Скрыть изображение капчи

    else:
        # Логика для неверного логина/пароля
        attempts += 1
        messagebox.showerror("Ошибка", "Неправильный логин или пароль. Повторите попытку.")  # Сообщение об ошибке

        if attempts == 1 and not captcha_displayed:
            # Отображаем капчу после первой неудачной попытки
            show_captcha()
            entry_captcha.pack()  # Показать поле ввода капчи
            refresh_captcha.pack()  # Показать кнопку обновления капчи
            captcha_label.pack()  # Показать изображение капчи
            captcha_displayed = True
        elif attempts >= 2:
            # Блокировка интерфейса после 2 неудачных попыток
            messagebox.showerror("Ошибка", "Превышено количество попыток. Введите капчу и подождите 3 минуты.")
            start_timer()
            lock_interface()

        # Меняем стиль кнопки на красный (указывая на ошибку)
        button_login.config(bootstyle='danger')

def lock_interface():
    entry_login.config(state=tk.DISABLED)
    entry_password.config(state=tk.DISABLED)
    entry_captcha.config(state=tk.DISABLED)

def toggle_password_visibility():
    if entry_password.cget('show') == '*':
        entry_password.config(show='')
        toggle_password_button.config(text='Скрыть пароль')
    else:
        entry_password.config(show='*')
        toggle_password_button.config(text='Показать пароль')

def open_auth_form():
    global root, entry_login, entry_password, button_login, captcha_value, captcha_label, entry_captcha, timer_label, toggle_password_button, refresh_captcha

    root = tk.Tk()
    style = Style(theme='darkly')  # Установка темы
    root.title("Авторизация")
    root.geometry("920x800")
    root.resizable(True, True)

    frame = ttk.Frame(root)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    entry_login = ttk.Entry(frame, font=("Arial", 18), width=30)
    entry_login.insert(0, "Логин")
    entry_login.pack(pady=20)

    entry_password = ttk.Entry(frame, font=("Arial", 18), width=30, show="*")
    entry_password.insert(0, "Пароль")
    entry_password.pack(pady=20)

    button_login = ttk.Button(frame, text="Войти", command=login, bootstyle="success", width=20)
    button_login.pack(pady=40)

    toggle_password_button = ttk.Button(frame, text="Показать пароль", command=toggle_password_visibility)
    toggle_password_button.pack(pady=5)

    captcha_value = tk.StringVar()
    entry_captcha = ttk.Entry(frame, font=("Arial", 18), width=30)
    captcha_label = tk.Label(frame)
    refresh_captcha = ttk.Button(frame, text="Обновить капчу", command=refresh_captcha_code, bootstyle="secondary")

    timer_label = ttk.Label(frame, text="", font=("Arial", 18))
    timer_label.pack()

    # Изначально скрыть поле и кнопку капчи
    entry_captcha.pack_forget()
    refresh_captcha.pack_forget()
    captcha_label.pack_forget()

    show_captcha()  # Отображаем капчу при загрузке
    root.protocol("WM_DELETE_WINDOW", on_closing)  # Обработчик закрытия окна
    root.mainloop()

def on_closing():
    if messagebox.askokcancel("Выход", "Вы действительно хотите выйти?"):
        root.destroy()  # Закрытие приложения

open_auth_form()
