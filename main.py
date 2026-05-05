import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

# --- Конфигурация ---
DATA_FILE = "data.json"

# --- Логика работы с данными ---
def load_data():
    """Загружает данные из JSON файла или возвращает пустой список."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    return []

def save_data(data):
    """Сохраняет список записей в JSON файл."""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# --- Логика фильтрации и отображения ---
def display_records(filter_func=None):
    """Отображает записи в таблице, применяя фильтр, если он передан."""
    for i in tree.get_children():
        tree.delete(i)
    
    records = data if filter_func is None else list(filter(filter_func, data))
    
    for record in records:
        precip = "Да" if record["precipitation"] else "Нет"
        tree.insert("", tk.END, values=(
            record["date"],
            record["temperature"],
            record["description"],
            precip
        ))

def filter_by_date():
    """Фильтрует записи по выбранной дате."""
    selected_date = date_filter.get()
    if not selected_date:
        display_records()
        return
    display_records(lambda r: r["date"] == selected_date)

def filter_by_temp():
    """Фильтрует записи по температуре (выше введённого значения)."""
    try:
        temp_value = float(temp_filter.get())
        display_records(lambda r: r["temperature"] > temp_value)
    except ValueError:
        messagebox.showerror("Ошибка", "Пожалуйста, введите число для температуры.")

def clear_filters():
    """Сбрасывает фильтры и показывает все записи."""
    date_filter.set("")
    temp_filter.delete(0, tk.END)
    display_records()

# --- Логика добавления записи ---
def add_record():
    """Добавляет новую запись после валидации."""
    date = entry_date.get()
    temp = entry_temp.get()
    desc = entry_desc.get()
    precip = precip_var.get() == 1

    # Валидация
    if not date or not temp or not desc:
        messagebox.showerror("Ошибка", "Все поля (Дата, Температура, Описание) обязательны для заполнения.")
        return

    try:
        # Проверка формата даты и преобразование температуры в число
        datetime.strptime(date, "%Y-%m-%d")
        temp_float = float(temp)
    except ValueError:
        messagebox.showerror("Ошибка", "Неверный формат даты (ГГГГ-ММ-ДД) или температуры.")
        return

    # Создание записи и добавление в список
    new_record = {
        "date": date,
        "temperature": temp_float,
        "description": desc,
        "precipitation": precip
    }
    
    data.append(new_record)
    save_data(data)
    
    # Обновление интерфейса и очистка полей ввода
    display_records()
    entry_date.delete(0, tk.END)
    entry_temp.delete(0, tk.END)
    entry_desc.delete(0, tk.END)
    precip_var.set(0)
    
# --- Инициализация данных ---
data = load_data()

# --- Создание главного окна ---
root = tk.Tk()
root.title("Дневник погоды")
root.geometry("800x500")
root.resizable(False, False)

# --- Основной фрейм для виджетов ---
main_frame = ttk.Frame(root, padding="10")
main_frame.pack(fill=tk.BOTH, expand=True)

# --- Панель добавления записи ---
add_frame = ttk.LabelFrame(main_frame, text="Добавить новую запись", padding="10")
add_frame.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")

ttk.Label(add_frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, padx=5, pady=5)
entry_date = ttk.Entry(add_frame, width=15)
entry_date.grid(row=0, column=1, padx=5, pady=5)
entry_date.insert(0, datetime.now().strftime("%Y-%m-%d")) # Текущая дата по умолчанию

ttk.Label(add_frame, text="Температура:").grid(row=1, column=0, padx=5, pady=5)
entry_temp = ttk.Entry(add_frame, width=15)
entry_temp.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(add_frame, text="Описание:").grid(row=2, column=0, padx=5, pady=5)
entry_desc = ttk.Entry(add_frame, width=30)
entry_desc.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

ttk.Label(add_frame, text="Осадки:").grid(row=3, column=0, padx=5, pady=5)
precip_var = tk.IntVar()
ttk.Checkbutton(add_frame, text="Да", variable=precip_var).grid(row=3, column=1, padx=5, pady=5)

ttk.Button(add_frame, text="Добавить запись", command=add_record).grid(row=4, column=0, columnspan=2, pady=15)


# --- Панель фильтрации ---
filter_frame = ttk.LabelFrame(main_frame, text="Фильтрация", padding="10")
filter_frame.grid(row=1, column=0, pady=10, sticky="nsew")

ttk.Label(filter_frame, text="По дате:").grid(row=0, column=0, padx=5)
date_filter = tk.StringVar()
ttk.Entry(filter_frame, textvariable=date_filter).grid(row=0, column=1, padx=5)
ttk.Button(filter_frame, text="Найти", command=filter_by_date).grid(row=0, column=2, padx=5)

ttk.Label(filter_frame, text="Температура >").grid(row=1, column=0, padx=5)
temp_filter = ttk.Entry(filter_frame)
temp_filter.grid(row=1, column=1, padx=5)
ttk.Button(filter_frame, text="Найти", command=filter_by_temp).grid(row=1, column=2, padx=5)
ttk.Button(filter_frame, text="Сбросить фильтры", command=clear_filters).grid(row=2, columnspan=3)


# --- Таблица для отображения записей ---
tree_frame = ttk.Frame(main_frame)
tree_frame.grid(row=2, columnspan=2)

columns = ("Дата", "Температура", "Описание", "Осадки")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=vsb.set)

for col in columns:
    tree.heading(col, text=col)
tree.column("Дата", width=120)
tree.column("Температура", width=100)
tree.column("Описание", width=300)
tree.column("Осадки", width=80)

tree.pack(side="left", fill="both", expand=True)
vsb.pack(side="right", fill="y")


# --- Запуск приложения ---
if __name__ == "__main__":
    display_records() # Показать все записи при старте
    root.mainloop()
