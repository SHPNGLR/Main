import tkinter as tk
from ttkbootstrap import ttk
from tkinter import messagebox

# Пример списка заявок, которые будут доступны мастеру
requests = [
    {"ID": 1, "ФИО": "Григорьев Семён Викторович", "Модель": "Принтер", "Проблема": "Не печатает"},
    {"ID": 2, "ФИО": "Сорокин Дмитрий Ильич", "Модель": "Сканер", "Проблема": "Не сканирует"}
]

def open_master_form(root, user_fio):
    # Создаем новое окно для формы мастера
    master_root = tk.Toplevel(root)
    master_root.title("Форма Мастера")
    master_root.geometry("800x600")
    master_root.resizable(True, True)

    # Приветствие мастера
    label_welcome = ttk.Label(master_root, text=f"Мастер: {user_fio}!", font=("Arial", 16))
    label_welcome.pack(pady=20)

    # Фрейм для основного содержимого
    content_frame = ttk.Frame(master_root)
    content_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    # Заголовок
    ttk.Label(content_frame, text="Записи мастера", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

    # Список заявок
    request_list = tk.Listbox(content_frame, width=70, height=20)
    request_list.grid(row=1, column=0, columnspan=2, pady=10)

    # Обновление списка заявок
    def update_master_request_list():
        request_list.delete(0, tk.END)
        if not requests:
            request_list.insert(tk.END, "Нет активных заявок.")
        else:
            for req in requests:
                request_list.insert(tk.END, f"ID: {req['ID']} | ФИО: {req['ФИО']} | Модель: {req['Модель']} | Проблема: {req['Проблема']}")

    # Удаление выбранной заявки
    def delete_request():
        selected = request_list.curselection()
        if selected:
            req_id = requests[selected[0]]["ID"]
            requests[:] = [req for req in requests if req["ID"] != req_id]
            update_master_request_list()
            messagebox.showinfo("Успех", f"Заявка ID: {req_id} выполнена и удалена!")
        else:
            messagebox.showwarning("Ошибка", "Выберите заявку для удаления.")

    # Кнопка для удаления заявки
    delete_button = ttk.Button(content_frame, text="Отметить как выполненную", command=delete_request, bootstyle="success")
    delete_button.grid(row=2, column=0, pady=10)

    # Выход из формы мастера
    def logout():
        master_root.destroy()  # Закрываем окно мастера
        root.deiconify()  # Возвращаем главное окно авторизации

    # Кнопка выхода
    logout_button = ttk.Button(content_frame, text="Выйти", command=logout, bootstyle="danger")
    logout_button.grid(row=2, column=1, pady=10)

    # Обновляем список заявок при открытии формы
    update_master_request_list()
