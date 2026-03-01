# Хорошая практика: передача аргументов
def increment(value):
    """Инкремент"""
    return value + 1

# Глобальные константы без global разрешены
VERSION = "1.0.0"

def get_version():
    """Чтение константы"""
    return VERSION
