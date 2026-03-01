class Utils:
    """Утилитный класс, используемый только как пространство имен"""
    @staticmethod
    def add(a, b):
        """Сложение"""
        return a + b

    @classmethod
    def create(cls):
        """Фабрика"""
        return cls()

class InternalUtils:
    """Еще один утилитный класс"""
    def log_something():
        """Статический метод без декоратора (в Python 2/3 без self это статический метод по факту)"""
        print("log")
