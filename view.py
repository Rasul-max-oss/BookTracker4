# ============================================
# view.py - ПРЕДСТАВЛЕНИЕ (ввод и вывод)
# ============================================
# Здесь ТОЛЬКО общение с пользователем
# Никакой логики!

class ConsoleView:
    """Класс для работы с консолью"""
    
    @staticmethod
    def show_menu():
        """Показать главное меню"""
        print("\n" + "=" * 50)
        print("        📚 BOOK TRACKER 📚")
        print("=" * 50)
        print("1. 📖 Добавить книгу")
        print("2. 🎧 Добавить аудиокнигу")
        print("3. 📋 Показать все книги")
        print("4. ✏️ Редактировать книгу")
        print("5. 🗑️ Удалить книгу")
        print("6. 🔍 Фильтр по жанру")
        print("7. 📄 Фильтр по страницам")
        print("8. ↩️ Отменить действие (СТЕК)")
        print("9. 📊 Показать очередь действий")
        print("10. 💾 Сохранить в JSON")
        print("11. 📂 Загрузить из JSON")
        print("0. 🚪 Выход")
        print("-" * 50)
    
    @staticmethod
    def show_books(books):
        """Показать список книг"""
        if not books:
            print("\n📭 Нет книг в библиотеке!")
            return
        
        print("\n" + "-" * 70)
        print(f"{'№':<4} {'Название':<25} {'Автор':<20} {'Статус':<12}")
        print("-" * 70)
        
        for i, book in enumerate(books):
            status_icon = "✅" if book.get_status() == "Done" else "🔄" if book.get_status() == "In Progress" else "📖"
            print(f"{i+1:<4} {book.get_title()[:25]:<25} {book.get_author()[:20]:<20} {status_icon} {book.get_status()}")
        
        print("-" * 70)
    
    @staticmethod
    def show_book_details(book):
        """Показать подробную информацию о книге"""
        print("\n" + "📖" * 25)
        print(f"Название: {book.get_title()}")
        print(f"Автор: {book.get_author()}")
        print(f"Жанр: {book.get_genre()}")
        
        # Полиморфизм - проверяем тип книги
        if hasattr(book, 'get_duration'):
            print(f"Длительность: {book.get_duration()} минут")
        else:
            print(f"Страниц: {book.get_pages()}")
        
        print(f"Статус: {book.get_status()}")
        print("📖" * 25)
    
    @staticmethod
    def get_string_input(prompt):
        """Получить строку с проверкой на пустоту (ВАЛИДАЦИЯ)"""
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("❌ Поле не может быть пустым!")
    
    @staticmethod
    def get_number_input(prompt, min_value=1):
        """Получить число с проверкой (ВАЛИДАЦИЯ)"""
        while True:
            try:
                value = int(input(prompt))
                if value >= min_value:
                    return value
                print(f"❌ Число должно быть больше {min_value - 1}!")
            except ValueError:
                print("❌ Введите целое число!")
    
    @staticmethod
    def get_choice(prompt, max_choice):
        """Получить выбор из меню"""
        while True:
            try:
                choice = int(input(prompt))
                if 0 <= choice <= max_choice:
                    return choice
                print(f"❌ Выберите 0-{max_choice}")
            except ValueError:
                print("❌ Введите число!")
    
    @staticmethod
    def get_status_input():
        """Получить статус с проверкой"""
        print("\nСтатусы: 1 - To Do, 2 - In Progress, 3 - Done")
        while True:
            try:
                choice = int(input("Выберите статус: "))
                if choice == 1:
                    return "To Do"
                elif choice == 2:
                    return "In Progress"
                elif choice == 3:
                    return "Done"
                print("Выберите 1, 2 или 3")
            except ValueError:
                print("Введите число!")
    
    @staticmethod
    def get_edit_field():
        """Выбрать поле для редактирования"""
        print("\nЧто редактируем?")
        print("1. Название")
        print("2. Автор")
        print("3. Жанр")
        print("4. Страницы/Длительность")
        print("5. Статус")
        
        while True:
            try:
                choice = int(input("Ваш выбор: "))
                if 1 <= choice <= 5:
                    return choice
                print("Выберите 1-5")
            except ValueError:
                print("Введите число!")
    
    @staticmethod
    def show_message(message, is_error=False):
        """Показать сообщение"""
        if is_error:
            print(f"⚠️ {message}")
        else:
            print(f"✅ {message}")
    
    @staticmethod
    def show_actions(actions):
        """Показать очередь действий"""
        if not actions:
            print("\n📭 Нет действий в очереди")
        else:
            print("\n📋 ОЧЕРЕДЬ ДЕЙСТВИЙ (FIFO):")
            for i, action in enumerate(actions, 1):
                print(f"  {i}. {action}")
    
    @staticmethod
    def show_goodbye():
        print("\n👋 До свидания!")
    
    @staticmethod
    def show_undo_success():
        print("✅ Действие отменено (СТЕК)!")
    
    @staticmethod
    def show_undo_fail():
        print("❌ Нет действий для отмены!")