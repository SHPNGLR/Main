import tkinter as tk
from tkinter import messagebox
from ttkbootstrap import ttk
from datetime import datetime

# Список заявок и начальный ID заявки
requests = []
request_id = 1

# Словарь ФИО и номера телефонов
phone_book = {
    "Григорьев Семён Викторович": "89219567849",
    "Сорокин Дмитрий Ильич": "89219567841",
    "Белоусов Егор Ярославович": "89219567842",
    "Суслов Михаил Александрович": "89219567843"
}

def open_client_form(root, user_fio):
    # Скрываем главное окно
    root.withdraw()

    client_form = tk.Toplevel(root)
    client_form.title("Форма Клиента")
    client_form.geometry("800x600")
    client_form.resizable(True, True)

    label_welcome = ttk.Label(client_form, text=f"Клиент: {user_fio}!", font=("Arial", 16))
    label_welcome.grid(row=0, column=0, columnspan=2, pady=20, padx=20, sticky="nsew")

    def is_valid_phone(phone):
        return phone.isdigit() and len(phone) == 11

    def delete_request():
        selected = request_list.curselection()
        if selected:
            req_id = requests[selected[0]]["ID"]
            requests[:] = [req for req in requests if req["ID"] != req_id]
            update_request_list()

    def edit_request():
        selected = request_list.curselection()
        if selected:
            req_id = requests[selected[0]]["ID"]
            req = next(req for req in requests if req["ID"] == req_id)
            name_entry.set(req["ФИО"])
            model_var.set(req["Модель"])
            problem_entry.delete("1.0", tk.END)
            problem_entry.insert("1.0", req["Проблема"])
            phone_entry.delete(0, tk.END)
            phone_entry.insert(0, req["Телефон"])
            status_label.config(text=f"Редактирование заявки ID: {req['ID']}")
            submit_button.config(text="Сохранить изменения", command=lambda: save_changes(req_id))
            delete_request()

    def save_changes(req_id):
        name = name_entry.get().strip()
        model = model_var.get()
        problem = problem_entry.get("1.0", tk.END).strip()
        phone = phone_entry.get().strip()

        if name and problem and is_valid_phone(phone):
            req = next(req for req in requests if req["ID"] == req_id)
            req.update({"ФИО": name, "Модель": model, "Проблема": problem, "Телефон": phone})
            update_request_list()
            submit_button.config(text="Отправить заявку", command=submit_request)
            status_label.config(text=f"Заявка ID: {req_id} обновлена")
            # Сброс формы
            name_entry.set("")
            model_var.set(" ")
            problem_entry.delete("1.0", tk.END)
            phone_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Ошибка", "Заполните все поля корректно!")

    def submit_request():
        global request_id
        name = name_entry.get().strip()
        model = model_var.get()
        date = datetime.now().strftime("%d.%m.%Y %H:%M")
        problem = problem_entry.get("1.0", tk.END).strip()
        phone = phone_entry.get().strip()

        if name and problem and is_valid_phone(phone):
            request = {"ID": request_id, "ФИО": name, "Модель": model, "Дата": date, "Проблема": problem, "Телефон": phone}
            requests.append(request)
            request_id += 1
            status_label.config(text=f"Статус заявки: Заявка принята, ID: {request['ID']}")
            # Очистка формы
            name_entry.set("")
            model_var.set(" ")
            problem_entry.delete("1.0", tk.END)
            phone_entry.delete(0, tk.END)
            update_request_list()
        else:
            messagebox.showerror("Ошибка", "Заполните все поля корректно!")

    def update_request_list():
        request_list.delete(0, tk.END)
        for req in requests:
            request_list.insert(tk.END, f"ID: {req['ID']} | Дата: {req['Дата']}")

    def on_name_select(event):
        name = name_entry.get()
        phone = phone_book.get(name, "")
        if phone:
            phone_entry.delete(0, tk.END)
            phone_entry.insert(0, phone)
        else:
            messagebox.showinfo("Информация", "Номер телефона не найден.")

    content_frame = ttk.Frame(client_form)
    content_frame.grid(row=1, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")

    content_frame.columnconfigure(0, weight=1)
    content_frame.columnconfigure(1, weight=2)

    ttk.Label(content_frame, text="Записаться на ремонт", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10, sticky="nsew")

    ttk.Label(content_frame, text="ФИО:").grid(row=1, column=0, sticky="e", padx=10)
    name_entry = ttk.Combobox(content_frame, values=list(phone_book.keys()), state="readonly")
    name_entry.bind("<<ComboboxSelected>>", on_name_select)
    name_entry.grid(row=1, column=1, pady=5, sticky="w")

    ttk.Label(content_frame, text="Модель:").grid(row=2, column=0, sticky="e", padx=10)
    model_var = tk.StringVar(value=" ")
    model_entry = ttk.Combobox(content_frame, textvariable=model_var, values=["Принтер", "Сканер", "Ксерокс", "Факс", "МФУ"], state="readonly")
    model_entry.grid(row=2, column=1, pady=5, sticky="w")

    ttk.Label(content_frame, text="Проблема:").grid(row=3, column=0, sticky="ne", padx=10)
    problem_entry = tk.Text(content_frame, width=30, height=5)
    problem_entry.grid(row=3, column=1, pady=5, sticky="w")

    ttk.Label(content_frame, text="Телефон:").grid(row=4, column=0, sticky="e", padx=10)
    phone_entry = ttk.Entry(content_frame, width=30)
    phone_entry.grid(row=4, column=1, pady=5, sticky="w")

    submit_button = ttk.Button(content_frame, text="Отправить заявку", command=submit_request, bootstyle="success")
    submit_button.grid(row=5, column=0, columnspan=2, pady=10)

    status_label = ttk.Label(content_frame, text="Статус заявки: Ожидание")
    status_label.grid(row=6, column=0, columnspan=2, pady=10)

    request_list = tk.Listbox(content_frame, width=80, height=15)
    request_list.grid(row=7, column=0, columnspan=2, pady=10)

    edit_button = ttk.Button(content_frame, text="Редактировать", command=edit_request, bootstyle="warning")
    edit_button.grid(row=8, column=0, pady=5)

    delete_button = ttk.Button(content_frame, text="Удалить", command=delete_request, bootstyle="danger")
    delete_button.grid(row=8, column=1, pady=5)

    logout_button = ttk.Button(content_frame, text="Выйти", command=lambda: logout(client_form, root), bootstyle="danger")
    logout_button.grid(row=9, column=0, columnspan=2, pady=10)

def logout(client_window, root):
    client_window.destroy()
    root.deiconify()  # Возвращаем главное окно
