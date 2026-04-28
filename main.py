# ============================================
# main.py - ТОЧКА ВХОДА
# ============================================
# Самый простой файл - просто запускает приложение

from controller import BookController


print("🚀 ЗАПУСК BOOK TRACKER...")
app = BookController()
app.run()