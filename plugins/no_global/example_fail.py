# Плохая практика: использование global
counter = 0

def increment():
    """Инкремент глобальной переменной"""
    global counter
    counter += 1

def reset():
    """Сброс"""
    global counter
    counter = 0
