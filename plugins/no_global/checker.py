import ast
import os
from core.base_checker import BaseChecker


class NoGlobalChecker(BaseChecker):
    """Проверяет отсутствие использования ключевого слова global"""

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
            
        super(NoGlobalChecker, self).process_file(filename, tree)

    def visit_Global(self, node):
        """Анализирует использование global

        Args:
            node: Узел AST

        Returns:
            None
        """
        self.add_error(self.current_file, node.lineno, "Never use the 'global' keyword")
        self.generic_visit(node)
