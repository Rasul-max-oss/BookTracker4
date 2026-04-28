# ============================================
# model.py - МОДЕЛЬ (данные и бизнес-логика)
# ============================================
# Здесь мы храним классы Book, AudioBook и BookManager
# Никакого ввода-вывода! Только данные и логика.

import json                    # Для работы с JSON файлами
from collections import deque  # Для создания очереди
import os                      # Для проверки существования файла


# ============================================
# КЛАСС BOOK - модель одной книги
# ============================================

class Book:
    """Класс, представляющий одну книгу"""
    
    def __init__(self, title, author, genre, pages):
        # ПРИВАТНЫЕ поля (инкапсуляция) - начинаются с _
        self._title = title      # Название книги
        self._author = author    # Автор
        self._genre = genre      # Жанр
        self._pages = pages      # Количество страниц
        self._status = "To Do"   # Статус: To Do, In Progress, Done
    
    # ========== ГЕТТЕРЫ (получаем значения) ==========
    
    def get_title(self):
        """Вернуть название книги"""
        return self._title
    
    def get_author(self):
        """Вернуть автора"""
        return self._author
    
    def get_genre(self):
        """Вернуть жанр"""
        return self._genre
    
    def get_pages(self):
        """Вернуть количество страниц"""
        return self._pages
    
    def get_status(self):
        """Вернуть статус"""
        return self._status
    
    # ========== СЕТТЕРЫ (изменяем значения с ПРОВЕРКОЙ) ==========
    
    def set_title(self, title):
        """Изменить название с проверкой на пустоту"""
        if not title or not title.strip():
            raise ValueError("Название не может быть пустым!")  # Валидация
        self._title = title.strip()
    
    def set_author(self, author):
        """Изменить автора с проверкой на пустоту"""
        if not author or not author.strip():
            raise ValueError("Автор не может быть пустым!")
        self._author = author.strip()
    
    def set_genre(self, genre):
        """Изменить жанр с проверкой на пустоту"""
        if not genre or not genre.strip():
            raise ValueError("Жанр не может быть пустым!")
        self._genre = genre.strip()
    
    def set_pages(self, pages):
        """Изменить количество страниц с проверкой (должно быть > 0)"""
        try:
            pages = int(pages)
            if pages <= 0:
                raise ValueError("Страниц должно быть больше 0!")
            self._pages = pages
        except ValueError:
            raise ValueError("Количество страниц должно быть числом!")
    
    def set_status(self, status):
        """Изменить статус (To Do, In Progress, Done)"""
        valid_statuses = ["To Do", "In Progress", "Done"]
        if status in valid_statuses:
            self._status = status
        else:
            raise ValueError(f"Статус должен быть: {valid_statuses}")
    
    # ========== МЕТОДЫ ДЛЯ РАБОТЫ С JSON ==========
    
    def to_dict(self):
        """Превращаем книгу в словарь (для сохранения в JSON)"""
        return {
            "title": self._title,
            "author": self._author,
            "genre": self._genre,
            "pages": self._pages,
            "status": self._status
        }
    
    @classmethod
    def from_dict(cls, data):
        """Создаем книгу из словаря (для загрузки из JSON)"""
        book = cls(data["title"], data["author"], data["genre"], data["pages"])
        book.set_status(data["status"])
        return book
    
    # ========== ДЛЯ КРАСИВОГО ВЫВОДА ==========
    
    def __str__(self):
        """Что показывать при print(книга)"""
        return f"{self._title} - {self._author} ({self._pages} стр.) - {self._status}"


# ============================================
# НАСЛЕДОВАНИЕ И ПОЛИМОРФИЗМ
# Класс AudioBook наследуется от Book
# ============================================

class AudioBook(Book):
    """Аудиокнига - наследник класса Book (пример полиморфизма)"""
    
    def __init__(self, title, author, genre, duration):
        # Вызываем конструктор родителя
        super().__init__(title, author, genre, 0)
        self._duration = duration  # Длительность в минутах
    
    def get_duration(self):
        return self._duration
    
    def set_duration(self, duration):
        try:
            duration = int(duration)
            if duration <= 0:
                raise ValueError("Длительность должна быть больше 0!")
            self._duration = duration
        except ValueError:
            raise ValueError("Длительность должна быть числом!")
    
    # ПЕРЕОПРЕДЕЛЯЕМ метод to_dict (полиморфизм)
    def to_dict(self):
        data = super().to_dict()
        data["duration"] = self._duration
        data["is_audio"] = True
        return data
    
    # ПЕРЕОПРЕДЕЛЯЕМ метод __str__ (полиморфизм)
    def __str__(self):
        return f"🎧 {self.get_title()} - {self.get_author()} ({self._duration} мин.) - {self.get_status()}"


# ============================================
# КЛАСС BOOKMANAGER - управляет всеми книгами
# Здесь находятся СТЕК и ОЧЕРЕДЬ
# ============================================

class BookManager:
    """Управление коллекцией книг"""
    
    def __init__(self):
        self._books = []              # Список всех книг
        self._undo_stack = []         # СТЕК для отмены действий (LIFO)
        self._action_queue = deque()  # ОЧЕРЕДЬ для истории действий (FIFO)
    
    # ========== CRUD ОПЕРАЦИИ ==========
    
    def add_book(self, book):
        """ДОБАВИТЬ книгу"""
        self._books.append(book)
        # Сохраняем в СТЕК для возможной отмены
        self._undo_stack.append({
            "type": "add",
            "index": len(self._books) - 1,
            "book": book.to_dict()
        })
        # Добавляем в ОЧЕРЕДЬ (история действий)
        self._action_queue.append(f"Добавлена книга: {book.get_title()}")
        return True
    
    def delete_book(self, index):
        """УДАЛИТЬ книгу по индексу"""
        if 0 <= index < len(self._books):
            deleted = self._books.pop(index)
            # Сохраняем в СТЕК
            self._undo_stack.append({
                "type": "delete",
                "index": index,
                "book": deleted.to_dict()
            })
            # Добавляем в ОЧЕРЕДЬ
            self._action_queue.append(f"Удалена книга: {deleted.get_title()}")
            return True
        return False
    
    def update_book(self, index, field, value):
        """ОБНОВИТЬ книгу"""
        if 0 <= index < len(self._books):
            book = self._books[index]
            old_value = None
            
            # Сохраняем старое значение
            if field == "title":
                old_value = book.get_title()
                book.set_title(value)
            elif field == "author":
                old_value = book.get_author()
                book.set_author(value)
            elif field == "genre":
                old_value = book.get_genre()
                book.set_genre(value)
            elif field == "pages":
                old_value = book.get_pages()
                book.set_pages(value)
            elif field == "status":
                old_value = book.get_status()
                book.set_status(value)
            
            # Сохраняем в СТЕК
            self._undo_stack.append({
                "type": "update",
                "index": index,
                "field": field,
                "old_value": old_value,
                "new_value": value
            })
            # Добавляем в ОЧЕРЕДЬ
            self._action_queue.append(f"Обновлена книга: {book.get_title()}")
            return True
        return False
    
    # ========== ОТМЕНА ДЕЙСТВИЯ (РАБОТА СО СТЕКОМ) ==========
    
    def undo(self):
        """Отменить последнее действие - используем СТЕК (LIFO)"""
        if not self._undo_stack:
            return False
        
        last = self._undo_stack.pop()
        
        if last["type"] == "add":
            # Отменяем добавление - удаляем книгу
            self._books.pop(last["index"])
            self._action_queue.append("Отмена: удаление добавленной книги")
            
        elif last["type"] == "delete":
            # Отменяем удаление - возвращаем книгу
            book = Book.from_dict(last["book"])
            self._books.insert(last["index"], book)
            self._action_queue.append("Отмена: восстановление удаленной книги")
            
        elif last["type"] == "update":
            # Отменяем обновление - возвращаем старое значение
            book = self._books[last["index"]]
            if last["field"] == "title":
                book.set_title(last["old_value"])
            elif last["field"] == "author":
                book.set_author(last["old_value"])
            elif last["field"] == "genre":
                book.set_genre(last["old_value"])
            elif last["field"] == "pages":
                book.set_pages(last["old_value"])
            elif last["field"] == "status":
                book.set_status(last["old_value"])
            self._action_queue.append("Отмена: возврат старого значения")
        
        return True
    
    # ========== РАБОТА С ОЧЕРЕДЬЮ ==========
    
    def get_next_action(self):
        """Получить следующее действие из ОЧЕРЕДИ (FIFO)"""
        if self._action_queue:
            return self._action_queue.popleft()
        return None
    
    def get_all_actions(self):
        """Получить ВСЕ действия из очереди"""
        actions = []
        while self._action_queue:
            actions.append(self._action_queue.popleft())
        return actions
    
    # ========== ФИЛЬТРАЦИЯ ==========
    
    def filter_by_genre(self, genre):
        """Фильтр по жанру"""
        if not genre:
            return self._books
        genre_lower = genre.lower()
        return [b for b in self._books if genre_lower in b.get_genre().lower()]
    
    def filter_by_pages(self, max_pages):
        """Фильтр по максимальному количеству страниц"""
        try:
            max_pages = int(max_pages)
            return [b for b in self._books if b.get_pages() <= max_pages and b.get_pages() > 0]
        except:
            return self._books
    
    # ========== JSON (СОХРАНЕНИЕ И ЗАГРУЗКА) ==========
    
    def save_to_json(self, filename="books.json"):
        """СОХРАНИТЬ все книги в JSON файл"""
        try:
            data = [book.to_dict() for book in self._books]
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Ошибка: {e}")
            return False
    
    def load_from_json(self, filename="books.json"):
        """ЗАГРУЗИТЬ книги из JSON файла"""
        if not os.path.exists(filename):
            return False
        
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            self._books = []
            for item in data:
                if item.get("is_audio", False):
                    book = AudioBook(
                        item["title"],
                        item["author"],
                        item["genre"],
                        item["duration"]
                    )
                else:
                    book = Book(
                        item["title"],
                        item["author"],
                        item["genre"],
                        item["pages"]
                    )
                book.set_status(item["status"])
                self._books.append(book)
            return True
        except Exception as e:
            print(f"Ошибка: {e}")
            return False
    
    # ========== ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ ==========
    
    def get_all_books(self):
        return self._books.copy()
    
    def get_book(self, index):
        if 0 <= index < len(self._books):
            return self._books[index]
        return None