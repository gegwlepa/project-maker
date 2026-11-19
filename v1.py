import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class BoardGameRentalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Прокат настольных игр")
        self.root.geometry("800x500")

        # Список для хранения данных (вместо базы данных)
        # Формат: [ID, Название, Имя получателя, Дата выдачи, Срок возврата, Статус]
        self.games = []
        self.next_id = 1

        self.setup_ui()
        self.add_dummy_data() # Добавим пару примеров для наглядности

    def setup_ui(self):
        # --- Фрейм ввода данных ---
        input_frame = tk.LabelFrame(self.root, text="Выдача игры", padx=10, pady=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        # Поля ввода
        tk.Label(input_frame, text="Название игры:").grid(row=0, column=0, sticky="w")
        self.entry_title = tk.Entry(input_frame, width=25)
        self.entry_title.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(input_frame, text="Имя получателя:").grid(row=0, column=2, sticky="w")
        self.entry_user = tk.Entry(input_frame, width=25)
        self.entry_user.grid(row=0, column=3, padx=5, pady=2)

        tk.Label(input_frame, text="Срок возврата (ГГГГ-ММ-ДД):").grid(row=1, column=0, sticky="w")
        self.entry_date = tk.Entry(input_frame, width=25)
        self.entry_date.grid(row=1, column=1, padx=5, pady=2)
        # Подсказка в поле
        self.entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # Кнопка добавления
        btn_add = tk.Button(input_frame, text="Выдать игру", command=self.add_game, bg="#e1f5fe")
        btn_add.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

        # --- Фрейм поиска ---
        search_frame = tk.Frame(self.root)
        search_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(search_frame, text="Поиск (Название или Имя):").pack(side="left")
        self.entry_search = tk.Entry(search_frame, width=30)
        self.entry_search.pack(side="left", padx=5)
        self.entry_search.bind("<KeyRelease>", self.filter_table) # Поиск при вводе

        # --- Таблица (Treeview) ---
        columns = ("ID", "Название", "Получатель", "Дата выдачи", "Срок возврата", "Статус")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", selectmode="browse")
        
        # Настройка заголовков
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        self.tree.column("ID", width=40)
        self.tree.column("Название", width=150)
        self.tree.column("Статус", width=120)

        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        # Теги для раскрашивания строк
        self.tree.tag_configure('returned', background='#e8f5e9') # Зеленый для возвращенных
        self.tree.tag_configure('active', background='#ffebee')   # Красный для активных

        # --- Кнопки действий ---
        action_frame = tk.Frame(self.root)
        action_frame.pack(fill="x", padx=10, pady=10)

        btn_return = tk.Button(action_frame, text="Отметить возврат", command=self.return_game, bg="#c8e6c9")
        btn_return.pack(side="left", padx=5)

        btn_delete = tk.Button(action_frame, text="Удалить запись", command=self.delete_game)
        btn_delete.pack(side="right", padx=5)

    def add_game(self):
        title = self.entry_title.get().strip()
        user = self.entry_user.get().strip()
        due_date = self.entry_date.get().strip()
        issue_date = datetime.now().strftime("%Y-%m-%d")

        if not title or not user:
            messagebox.showwarning("Ошибка", "Заполните название игры и имя получателя!")
            return

        # Простая проверка формата даты
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте ГГГГ-ММ-ДД")
            return

        # Добавляем в список данных
        game_id = self.next_id
        self.next_id += 1
        self.games.append([game_id, title, user, issue_date, due_date, "Выдана"])

        # Обновляем таблицу
        self.refresh_table()
        
        # Очищаем поля
        self.entry_title.delete(0, tk.END)
        self.entry_user.delete(0, tk.END)

    def refresh_table(self, filter_text=""):
        # Очищаем таблицу
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Заполняем заново
        for game in self.games:
            # Если есть текст для поиска, проверяем совпадение
            if filter_text.lower() in game[1].lower() or filter_text.lower() in game[2].lower():
                tag = 'returned' if game[5] == "Возвращена" else 'active'
                self.tree.insert("", "end", values=game, tags=(tag,))

    def filter_table(self, event):
        search_term = self.entry_search.get()
        self.refresh_table(search_term)

    def get_selected_game(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showinfo("Внимание", "Выберите игру в таблице.")
            return None
        
        # Получаем ID выбранной строки
        values = self.tree.item(selected_item)['values']
        game_id = int(values[0])
        
        # Находим игру в нашем списке
        for game in self.games:
            if game[0] == game_id:
                return game
        return None

    def return_game(self):
        game = self.get_selected_game()
        if not game:
            return

        if game[5] == "Возвращена":
            messagebox.showinfo("Инфо", "Эта игра уже возвращена.")
            return

        # Меняем статус
        game[5] = "Возвращена"
        self.refresh_table(self.entry_search.get()) # Обновляем с учетом фильтра
        messagebox.showinfo("Успех", f"Игра '{game[1]}' возвращена!")

    def delete_game(self):
        game = self.get_selected_game()
        if not game:
            return
        
        if messagebox.askyesno("Подтверждение", f"Удалить запись об игре '{game[1]}'?"):
            self.games.remove(game)
            self.refresh_table(self.entry_search.get())

    def add_dummy_data(self):
        # Добавим тестовые данные при запуске
        self.next_id = 1
        self.refresh_table()

if __name__ == "__main__":
    root = tk.Tk()
    app = BoardGameRentalApp(root)
    root.mainloop()