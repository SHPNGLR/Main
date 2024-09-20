import tkinter as tk
from tkinter import messagebox  # Добавлен импорт messagebox
from ttkbootstrap import ttk

def open_manager_form(root, user_fio):
    # Создаем новое окно для формы менеджера
    manager_root = tk.Toplevel(root)
    manager_root.title("Форма Менеджера")
    manager_root.geometry("800x600")
    manager_root.resizable(True, True)

    # Приветственное сообщение для менеджера
    label_welcome = ttk.Label(manager_root, text=f"Менеджер: {user_fio}!", font=("Arial", 16))
    label_welcome.pack(pady=20)

    # Функция для просмотра логов входов пользователей (пример)
    def view_logins():
        messagebox.showinfo("Логи входа", "Здесь будут отображаться логи входа пользователей.")

    # Кнопка для просмотра логов входов
    view_logins_button = ttk.Button(manager_root, text="Просмотр входов", command=view_logins, bootstyle="info")
    view_logins_button.pack(pady=10)

    # Функция для выхода и возврата к окну авторизации
    def logout():
        manager_root.destroy()  # Закрываем окно менеджера
        root.deiconify()  # Возвращаем главное окно (окно авторизации)

    # Кнопка выхода
    logout_button = ttk.Button(manager_root, text="Выйти", command=logout, bootstyle="danger")
    logout_button.pack(pady=10)

    # Обработка закрытия окна через стандартное закрытие (крестик)
    manager_root.protocol("WM_DELETE_WINDOW", logout)

