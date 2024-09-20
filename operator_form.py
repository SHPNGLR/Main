import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

requests = []  # Список заявок

def open_operator_form(root, user_fio):
    operator_root = tk.Toplevel(root)
    operator_root.title("Форма Оператора")
    operator_root.geometry("800x600")
    operator_root.resizable(True, True)

    label_welcome = ttk.Label(operator_root, text=f"Оператор: {user_fio}!", font=("Arial", 16))
    label_welcome.pack(pady=20)

    def update_request_list():
        request_list.delete(0, tk.END)
        for req in requests:
            request_list.insert(tk.END, f"ID: {req['ID']} | ФИО: {req['ФИО']} | Модель: {req['Модель']} | Дата: {req['Дата']}")

    def assign_date():
        selected = request_list.curselection()
        if selected:
            req_id = requests[selected[0]]["ID"]
            req = next(req for req in requests if req["ID"] == req_id)
            date_str = date_entry.get()
            try:
                date = datetime.strptime(date_str, "%d.%m.%Y")
                req["Дата ремонта"] = date.strftime("%d.%m.%Y")
                update_request_list()
                messagebox.showinfo("Успех", f"Дата ремонта назначена для заявки ID: {req_id}")
            except ValueError:
                messagebox.showerror("Ошибка", "Введите дату в формате ДД.ММ.ГГГГ")

    def assign_master():
        selected = request_list.curselection()
        if selected:
            req_id = requests[selected[0]]["ID"]
            req = next(req for req in requests if req["ID"] == req_id)
            master = master_var.get()
            req["Мастер"] = master
            update_request_list()
            messagebox.showinfo("Успех", f"Мастер назначен для заявки ID: {req_id}")

    ttk.Label(operator_root, text="Выберите заявку для редактирования").pack(pady=10)

    request_list = tk.Listbox(operator_root, width=80, height=15)
    request_list.pack(pady=10)

    date_label = ttk.Label(operator_root, text="Дата ремонта (ДД.ММ.ГГГГ):")
    date_label.pack(pady=5)
    date_entry = ttk.Entry(operator_root, width=20)
    date_entry.pack(pady=5)

    assign_date_button = ttk.Button(operator_root, text="Назначить дату ремонта", command=assign_date, bootstyle="success")
    assign_date_button.pack(pady=10)

    master_label = ttk.Label(operator_root, text="Выберите мастера:")
    master_label.pack(pady=5)
    master_var = tk.StringVar(value="Ильин Александр Андреевич")  # По умолчанию
    master_menu = ttk.Combobox(operator_root, textvariable=master_var, 
                                values=["Ильин Александр Андреевич", 
                                        "Никифоров Иван Дмитриевич", 
                                        "Васильев Вячеслав Александрович"], 
                                state="readonly")
    master_menu.pack(pady=5)

    assign_master_button = ttk.Button(operator_root, text="Назначить мастера", command=assign_master, bootstyle="primary")
    assign_master_button.pack(pady=10)

    def logout():
        operator_root.destroy()
        root.deiconify()  # Показать главное окно обратно

    operator_root.protocol("WM_DELETE_WINDOW", logout)  # Обработка закрытия окна
    logout_button = ttk.Button(operator_root, text="Выйти", command=logout, bootstyle="danger")
    logout_button.pack(pady=10)

    update_request_list()  # Инициализация списка заявок
