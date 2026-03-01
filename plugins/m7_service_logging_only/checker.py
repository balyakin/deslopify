import ast
import os
from core.base_checker import BaseChecker


class M7ServiceLoggingOnlyChecker(BaseChecker):
    """Проверяет использование m7-service-logging вместо стандартного logging"""

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
            
        super(M7ServiceLoggingOnlyChecker, self).process_file(filename, tree)

    def visit_Import(self, node):
        """Анализирует обычные импорты

        Args:
            node: Узел AST импорта

        Returns:
            None
        """
        for alias in node.names:
            if alias.name == 'logging':
                self.add_error(self.current_file, node.lineno, "Use 'm7-service-logging' instead of standard 'logging'")
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        """Анализирует импорты из модулей

        Args:
            node: Узел AST импорта

        Returns:
            None
        """
        if node.module == 'logging':
            self.add_error(self.current_file, node.lineno, "Use 'm7-service-logging' instead of standard 'logging'")
        self.generic_visit(node)
