# ============================================
# controller.py - КОНТРОЛЛЕР
# ============================================
# Связывает Model и View
# Обрабатывает команды пользователя

from model import Book, AudioBook, BookManager
from view import ConsoleView


class BookController:
    """Контроллер - управляет приложением"""
    
    def __init__(self):
        self.manager = BookManager()  # Модель
        self.view = ConsoleView()      # Представление
    
    def run(self):
        """ГЛАВНЫЙ ЦИКЛ ПРОГРАММЫ"""
        # Пробуем загрузить данные при старте
        if self.manager.load_from_json():
            self.view.show_message("Данные загружены из JSON")
        
        while True:
            self.view.show_menu()
            choice = self.view.get_choice("Выберите действие: ", 11)
            
            if choice == 0:
                save = input("Сохранить перед выходом? (y/n): ").lower()
                if save == 'y':
                    self.manager.save_to_json()
                self.view.show_goodbye()
                break
            
            elif choice == 1:
                self.add_book(is_audio=False)
            elif choice == 2:
                self.add_book(is_audio=True)
            elif choice == 3:
                self.show_all_books()
            elif choice == 4:
                self.edit_book()
            elif choice == 5:
                self.delete_book()
            elif choice == 6:
                self.filter_by_genre()
            elif choice == 7:
                self.filter_by_pages()
            elif choice == 8:
                self.undo_action()
            elif choice == 9:
                self.show_queue()
            elif choice == 10:
                self.save_data()
            elif choice == 11:
                self.load_data()
    
    def add_book(self, is_audio=False):
        """Добавить книгу"""
        self.view.show_message("Добавление новой книги...")
        
        title = self.view.get_string_input("Название: ")
        author = self.view.get_string_input("Автор: ")
        genre = self.view.get_string_input("Жанр: ")
        
        if is_audio:
            duration = self.view.get_number_input("Длительность (минут): ")
            book = AudioBook(title, author, genre, duration)
        else:
            pages = self.view.get_number_input("Количество страниц: ")
            book = Book(title, author, genre, pages)
        
        status = self.view.get_status_input()
        book.set_status(status)
        
        if self.manager.add_book(book):
            self.view.show_message(f"Книга '{title}' добавлена!")
    
    def show_all_books(self):
        """Показать все книги"""
        books = self.manager.get_all_books()
        self.view.show_books(books)
        
        if books:
            show = input("\nПоказать подробности? (y/n): ").lower()
            if show == 'y':
                num = self.view.get_number_input("Номер книги: ", 1)
                if 1 <= num <= len(books):
                    self.view.show_book_details(books[num-1])
    
    def edit_book(self):
        """Редактировать книгу"""
        books = self.manager.get_all_books()
        if not books:
            self.view.show_message("Нет книг!", True)
            return
        
        self.view.show_books(books)
        num = self.view.get_number_input("Номер книги: ", 1)
        
        if 1 <= num <= len(books):
            book = books[num-1]
            self.view.show_book_details(book)
            
            field = self.view.get_edit_field()
            index = num - 1
            
            if field == 1:
                new = self.view.get_string_input("Новое название: ")
                self.manager.update_book(index, "title", new)
            elif field == 2:
                new = self.view.get_string_input("Новый автор: ")
                self.manager.update_book(index, "author", new)
            elif field == 3:
                new = self.view.get_string_input("Новый жанр: ")
                self.manager.update_book(index, "genre", new)
            elif field == 4:
                if hasattr(book, 'get_duration'):
                    new = self.view.get_number_input("Новая длительность: ")
                    self.manager.update_book(index, "duration", new)
                else:
                    new = self.view.get_number_input("Новое количество страниц: ")
                    self.manager.update_book(index, "pages", new)
            elif field == 5:
                new = self.view.get_status_input()
                self.manager.update_book(index, "status", new)
            
            self.view.show_message("Книга обновлена!")
    
    def delete_book(self):
        """Удалить книгу"""
        books = self.manager.get_all_books()
        if not books:
            self.view.show_message("Нет книг!", True)
            return
        
        self.view.show_books(books)
        num = self.view.get_number_input("Номер книги для удаления: ", 1)
        
        if 1 <= num <= len(books):
            book = books[num-1]
            confirm = input(f"Удалить '{book.get_title()}'? (y/n): ").lower()
            if confirm == 'y':
                if self.manager.delete_book(num-1):
                    self.view.show_message("Книга удалена!")
    
    def filter_by_genre(self):
        """Фильтрация по жанру"""
        genre = input("Введите жанр: ").strip()
        filtered = self.manager.filter_by_genre(genre)
        self.view.show_books(filtered)
        self.view.show_message(f"Найдено: {len(filtered)}")
    
    def filter_by_pages(self):
        """Фильтрация по страницам"""
        max_pages = self.view.get_number_input("Максимум страниц: ")
        filtered = self.manager.filter_by_pages(max_pages)
        self.view.show_books(filtered)
        self.view.show_message(f"Найдено: {len(filtered)}")
    
    def undo_action(self):
        """Отменить действие (СТЕК)"""
        if self.manager.undo():
            self.view.show_undo_success()
        else:
            self.view.show_undo_fail()
    
    def show_queue(self):
        """Показать очередь (FIFO)"""
        actions = self.manager.get_all_actions()
        self.view.show_actions(actions)
    
    def save_data(self):
        """Сохранить в JSON"""
        if self.manager.save_to_json():
            self.view.show_message("Сохранено в books.json!")
        else:
            self.view.show_message("Ошибка сохранения!", True)
    
    def load_data(self):
        """Загрузить из JSON"""
        if self.manager.load_from_json():
            self.view.show_message("Загружено из books.json!")
        else:
            self.view.show_message("Файл не найден!", True)