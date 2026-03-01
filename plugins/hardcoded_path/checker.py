import ast
import os
import re
from core.base_checker import BaseChecker


class HardcodedPathChecker(BaseChecker):
    """Проверяет наличие жестко заданных абсолютных путей в коде"""

    # Регулярные выражения для поиска путей (UNIX и Windows)
    # Ищем строки, начинающиеся с /Users/, /home/, C:\, D:\ и т.д.
    _PATH_REGEX = re.compile(r'^(/Users/|/home/|[A-Za-z]:\\)', re.IGNORECASE)

    def process_file(self, filename, tree):
        """Пропускает файлы тестов

        Args:
            filename: Имя обрабатываемого файла
            tree: AST дерево файла

        Returns:
            None
        """
        file_basename = os.path.basename(filename)
        is_test_file = file_basename.startswith('test_')
        
        if is_test_file:
            return
            
        super(HardcodedPathChecker, self).process_file(filename, tree)

    def visit_Str(self, node):
        """Анализирует строковые константы (для Python < 3.8)

        Args:
            node: Узел AST строки

        Returns:
            None
        """
        if self._PATH_REGEX.match(node.s):
            self.add_error(self.current_file, node.lineno, "Hardcoded absolute path found: '{0}'".format(node.s))
            
        self.generic_visit(node)

    def visit_Constant(self, node):
        """Анализирует константы (для Python >= 3.8)

        Args:
            node: Узел AST константы

        Returns:
            None
        """
        is_str = isinstance(node.value, str)
        if is_str and self._PATH_REGEX.match(node.value):
            self.add_error(self.current_file, node.lineno, "Hardcoded absolute path found: '{0}'".format(node.value))
            
        self.generic_visit(node)
