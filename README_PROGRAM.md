## README_PROGRAM.md
# 1. Импорт библиотек и настройка окружения
~~~Bash
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
~~~
### Что делает:

tkinter — основная библиотека для создания графического интерфейса (окна, кнопки, поля ввода).

ttk — модуль «тематических» виджетов (используется для создания современной таблицы Treeview).

messagebox — всплывающие окна (предупреждения, ошибки, подтверждения).

datetime — работа с датой и временем (автоматическая подстановка текущей даты выдачи).
# 2. Инициализация класса и главного окна
~~~Bash
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
        self.add_dummy_data()
~~~
### Что делает:

__init__ — конструктор класса, вызывается при запуске приложения.

Задаёт заголовок окна и его初始 размер (800×500 пикселей).

Создаёт список self.games — это «база данных» в оперативной памяти. Каждая запись — список из 6 элементов:

[0] ID записи (уникальный номер)

[1] Название игры

[2] Имя получателя

[3] Дата выдачи

[4] Срок возврата

[5] Статус («Выдана» / «Возвращена»)

self.next_id — счётчик для генерации уникальных ID. После перезапуска сбрасывается на 1 (данные не сохраняются).

Вызывает два метода:

setup_ui() — строит интерфейс.

add_dummy_data() — в вашей версии он только обновляет таблицу (тестовые данные убраны).
# 3. Построение интерфейса — метод setup_ui()
## 3. Построение интерфейса — метод setup_ui()
~~~Bash
input_frame = tk.LabelFrame(self.root, text="Выдача игры", padx=10, pady=10)
input_frame.pack(fill="x", padx=10, pady=5)
~~~
### Что делает:
~~~Bash
создаёт рамку с заголовком «Выдача игры» и прикрепляет её к верхней части окна, растягивая по ширине.
tk.Label(input_frame, text="Название игры:").grid(row=0, column=0, sticky="w")
self.entry_title = tk.Entry(input_frame, width=25)
self.entry_title.grid(row=0, column=1, padx=5, pady=2)

tk.Label(input_frame, text="Имя получателя:").grid(row=0, column=2, sticky="w")
self.entry_user = tk.Entry(input_frame, width=25)
self.entry_user.grid(row=0, column=3, padx=5, pady=2)
~~~
### Что делает: 
создаёт поля ввода для названия игры и имени получателя, располагая их в одну строку (сетка grid).
~~~Bash
tk.Label(input_frame, text="Срок возврата (ГГГГ-ММ-ДД):").grid(row=1, column=0, sticky="w")
self.entry_date = tk.Entry(input_frame, width=25)
self.entry_date.grid(row=1, column=1, padx=5, pady=2)
self.entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
~~~
### Что делает:
~~~Bash
создаёт поле для срока возврата и автоматически подставляет текущую дату в формате ГГГГ-ММ-ДД (например, 2026-11-19).
btn_add = tk.Button(input_frame, text="Выдать игру", command=self.add_game, bg="#e1f5fe")
btn_add.grid(row=1, column=3, padx=5, pady=5, sticky="ew")
~~~
### Что делает: 
кнопка «Выдать игру», при нажатии вызывает метод add_game(). Светло-голубой фон (#e1f5fe) для визуального выделения.
## 3.2. Блок поиска
~~~Bash
search_frame = tk.Frame(self.root)
search_frame.pack(fill="x", padx=10, pady=5)

tk.Label(search_frame, text="Поиск (Название или Имя):").pack(side="left")
self.entry_search = tk.Entry(search_frame, width=30)
self.entry_search.pack(side="left", padx=5)
self.entry_search.bind("<KeyRelease>", self.filter_table)
~~~
### Что делает:

Создаёт строку поиска.

bind("<KeyRelease>", ...) — ключевая фишка: фильтрация таблицы запускается при каждом отпускании клавиши (то есть в реальном времени, без нажатия кнопки «Найти»).
## 3.3. Таблица (Treeview)
~~~Bash
columns = ("ID", "Название", "Получатель", "Дата выдачи", "Срок возврата", "Статус")
self.tree = ttk.Treeview(self.root, columns=columns, show="headings", selectmode="browse")
~~~
### Что делает:

Создаёт таблицу с 6 колонками.

show="headings" — скрывает служебную колонку с номерами строк, показывает только заданные столбцы.

selectmode="browse" — разрешает выделять только одну строку за раз (нельзя выбрать несколько).
~~~bash
for col in columns:
    self.tree.heading(col, text=col)
    self.tree.column(col, width=100)

self.tree.column("ID", width=40)
self.tree.column("Название", width=150)
self.tree.column("Статус", width=120)
~~~
### Что делает:
 настраивает заголовки и ширину колонок (ID — узкий, Название и Статус — шире).
~~~Bash
self.tree.pack(fill="both", expand=True, padx=10, pady=5)

self.tree.tag_configure('returned', background='#e8f5e9') # Зеленый
self.tree.tag_configure('active', background='#ffebee')   # Красный
~~~
### Что делает:

Размещает таблицу и позволяет ей растягиваться.

Создаёт цветовые теги:

returned
 (зелёный фон) — игра возвращена.

active
 (красный фон) — игра ещё у посетителя.
## 3.4. Кнопки действий (нижняя панель)
~~~Bash
action_frame = tk.Frame(self.root)
action_frame.pack(fill="x", padx=10, pady=10)

btn_return = tk.Button(action_frame, text="Отметить возврат", command=self.return_game, bg="#c8e6c9")
btn_return.pack(side="left", padx=5)

btn_delete = tk.Button(action_frame, text="Удалить запись", command=self.delete_game)
btn_delete.pack(side="right", padx=5)
~~~
### Что делает:

Кнопка «Отметить возврат» (зелёная) — слева. Вызывает return_game().

Кнопка «Удалить запись» — справа. Вызывает delete_game().

Разнесены по разным сторонам, чтобы случайно не нажать «Удалить» вместо «Возврат».

# 4. Добавление игры — метод add_game()
~~~bash
def add_game(self):
    title = self.entry_title.get().strip()
    user = self.entry_user.get().strip()
    due_date = self.entry_date.get().strip()
    issue_date = datetime.now().strftime("%Y-%m-%d")
~~~
### Что делает:
 считывает данные из полей. .strip() убирает случайные пробелы по краям. Дата выдачи ставится автоматически (сегодняшняя).

~~~bash
if not title or not user:
    messagebox.showwarning("Ошибка", "Заполните название игры и имя получателя!")
    return
~~~
### Что делает:
 проверка — название и имя обязательны. Если пусто — выводит предупреждение и прерывает выполнение.
~~~bash
try:
    datetime.strptime(due_date, "%Y-%m-%d")
except ValueError:
    messagebox.showerror("Ошибка", "Неверный формат даты. Используйте ГГГГ-ММ-ДД")
    return
~~~
### Что делает:
 проверяет, что введённая дата соответствует формату ГГГГ-ММ-ДД. Если нет — сообщает об ошибке.

~~~bash
game_id = self.next_id
self.next_id += 1
self.games.append([game_id, title, user, issue_date, due_date, "Выдана"])

self.refresh_table()

self.entry_title.delete(0, tk.END)
self.entry_user.delete(0, tk.END)
~~~
### Что делает:

Формирует новую запись со статусом «Выдана».

Добавляет её в список self.games.

Обновляет таблицу.

Очищает поля названия и имени (дату оставляет, чтобы было удобно выдавать несколько игр подряд одному человеку).

# 5. Обновление и фильтрация таблицы
## 5.1. refresh_table() — перерисовка таблицы
~~~bash
def refresh_table(self, filter_text=""):
    for row in self.tree.get_children():
        self.tree.delete(row)

    for game in self.games:
        if filter_text.lower() in game[1].lower() or filter_text.lower() in game[2].lower():
            tag = 'returned' if game[5] == "Возвращена" else 'active'
            self.tree.insert("", "end", values=game, tags=(tag,))
~~~
### Что делает:

Полностью очищает таблицу (self.tree.delete для каждой строки).

Проходит по списку self.games и добавляет только те записи, которые содержат текст поиска (в названии или имени, без учёта регистра).

Присваивает каждой строке тег цвета в зависимости от статуса.

💡 Почему так? Treeview не поддерживает «обновление на месте», поэтому проще всего очищать и заполнять заново при любом изменении данных.

## 5.2. filter_table() — обработчик поиска
~~~bash
def filter_table(self, event):
    search_term = self.entry_search.get()
    self.refresh_table(search_term)
~~~
### Что делает: 
вызывается при каждом нажатии/отпускании клавиши в поле поиска. Берёт текст и передаёт его в refresh_table().

## 6. Вспомогательный метод — get_selected_game()
~~~bash
def get_selected_game(self):
    selected_item = self.tree.selection()
    if not selected_item:
        messagebox.showinfo("Внимание", "Выберите игру в таблице.")
        return None

    values = self.tree.item(selected_item)['values']
    game_id = int(values[0])

    for game in self.games:
        if game[0] == game_id:
            return game
    return None
~~~
### Что делает:

Проверяет, выбрана ли строка в таблице.

Если нет — показывает подсказку «Выберите игру» и возвращает None.

Если да — извлекает ID из выделенной строки и находит соответствующий объект в списке self.games.

🎯 Зачем нужен этот метод? Чтобы не дублировать код в return_game() и delete_game(). Обе кнопки сначала вызывают get_selected_game(), а потом работают с найденной записью.

# 7. Отметка о возврате — метод return_game()
~~~bash
def return_game(self):
    game = self.get_selected_game()
    if not game:
        return

    if game[5] == "Возвращена":
        messagebox.showinfo("Инфо", "Эта игра уже возвращена.")
        return

    game[5] = "Возвращена"
    self.refresh_table(self.entry_search.get())
    messagebox.showinfo("Успех", f"Игра '{game[1]}' возвращена!")
~~~
### Что делает:

Получает выбранную игру через get_selected_game().

Если ничего не выбрано — прерывается.

Если игра уже возвращена — сообщает об этом (защита от двойного нажатия).

Меняет статус на «Возвращена» — строка автоматически перекрасится в зелёный.

Обновляет таблицу, сохраняя текущий фильтр поиска.

Показывает подтверждение.

# 8. Удаление записи — метод delete_game()
~~~bash
def delete_game(self):
    game = self.get_selected_game()
    if not game:
        return

    if messagebox.askyesno("Подтверждение", f"Удалить запись об игре '{game[1]}'?"):
        self.games.remove(game)
        self.refresh_table(self.entry_search.get())
~~~
### Что делает:

Получает выбранную игру.

Спрашивает подтверждение (askyesno) — защита от случайного удаления.

Если пользователь нажал «Да» — удаляет запись из списка и перерисовывает таблицу.

# 9. Заглушка add_dummy_data()
~~~Bash
def add_dummy_data(self):
    self.next_id = 1
    self.refresh_table()
~~~
### Что делает в вашей версии:
 просто сбрасывает счётчик ID и обновляет (пустую) таблицу при запуске. Изначально здесь добавлялись тестовые записи, но вы их убрали — теперь приложение стартует с чистой таблицей.

# 10. Точка входа — запуск приложения
~~~bash
if __name__ == "__main__":
    root = tk.Tk()
    app = BoardGameRentalApp(root)
    root.mainloop()
Что делает:

if __name__ == "__main__": — гарантия, что код выполнится только при прямом запуске файла (а не при импорте как модуля)
~~~
### Что делает:
tk.Tk() — создаёт главное окно.

BoardGameRentalApp(root) — создаёт экземпляр приложения.

root.mainloop() — запускает бесконечный цикл обработки событий (окно остаётся открытым и реагирует на действия).


