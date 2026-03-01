try:
    1 / 0
except ZeroDivisionError:
    # Правильный способ
    logger.exception("Division by zero")

try:
    some_func()
except Exception:
    # Обычный лог разрешен если это не ошибка
    print("Normal print")
    log.info("Finished attempt") # Но мы разрешаем info если это просто статус
