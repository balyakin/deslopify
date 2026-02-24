import ast


class BaseChecker(ast.NodeVisitor):
    """Базовый класс для всех плагинов проверки кода"""

    def __init__(self):
        """Инициализирует базовые атрибуты чекера"""
        super(BaseChecker, self).__init__()
        self.errors = []
        self.current_file = ""

    def add_error(self, file_path, line_number, message):
        """Добавляет найденную ошибку в общий список

        Args:
            file_path: Путь к файлу
            line_number: Номер строки
            message: Текст ошибки

        Returns:
            None
        """
        error_info = {
            'file': file_path,
            'line': line_number,
            'message': message
        }
        self.errors.append(error_info)

    def process_file(self, filename, tree):
        """Запускает фазу сбора данных для конкретного файла

        Args:
            filename: Имя обрабатываемого файла
            tree: AST дерево файла

        Returns:
            None
        """
        self.current_file = filename
        self.visit(tree)

    def finalize(self):
        """Запускает фазу финального анализа по всему проекту

        Returns:
            Список найденных ошибок
        """
        return self.errors
