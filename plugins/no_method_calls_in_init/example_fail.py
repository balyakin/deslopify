class Invalid:
    """Плохая инициализация"""
    def __init__(self, name):
        """Конструктор вызывает методы"""
        self.name = name
        self.setup()
        self.load_data()

    def setup(self):
        """Настройка"""
        pass

    def load_data(self):
        """Загрузка"""
        pass

class InvalidSuper:
    """Плохой вызов super"""
    def __init__(self):
        """Вызов метода родителя"""
        super(InvalidSuper, self).do_something()
