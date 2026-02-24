import os
import ast
from core.base_checker import BaseChecker


class TryExceptPassChecker(BaseChecker):
    """Проверяет наличие блоков except в которых используется только pass"""

    def process_file(self, filename, tree):
        """Пропускает файлы тестов перед запуском анализа

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
            
        super(TryExceptPassChecker, self).process_file(filename, tree)

    def visit_ExceptHandler(self, node):
        """Анализирует обработчики исключений

        Args:
            node: Узел AST

        Returns:
            None
        """
        statements_count = len(node.body)
        has_one_statement = statements_count == 1
        
        is_pass_statement = False
        if has_one_statement:
            is_pass_statement = isinstance(node.body[0], ast.Pass)
            
        if has_one_statement and is_pass_statement:
            error_message = "Found try/except block with only 'pass'"
            self.add_error(self.current_file, node.lineno, error_message)
            
        self.generic_visit(node)
