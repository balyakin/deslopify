class ValidStatefulClass:
    """Класс с состоянием"""
    def __init__(self, name):
        """Инициализация"""
        self.name = name

class NamespaceWithConstants:
    """Класс только с константами (допустимо для группировки)"""
    MAX_RETRY = 5
    TIMEOUT = 10

class MixinClass:
    """Класс-миксин без __init__, но с методами экземпляра"""
    def do_something(self):
        """Метод экземпляра"""
        print("doing")

class AbstractBase(ABC):
    """Абстрактный класс"""
    @abstractmethod
    def run(self):
        """Метод"""
        pass
