class Valid:
    """Хорошая инициализация"""
    def __init__(self, name):
        """Конструктор только инициализирует"""
        super(Valid, self).__init__()
        self.name = name
        self.items = []
