import ast
import os
from core.base_checker import BaseChecker


class NoStringConcatenationChecker(BaseChecker):
    """Проверяет склейку строк через '+' (нужно использовать форматирование)"""

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
            
        super(NoStringConcatenationChecker, self).process_file(filename, tree)

    def visit_BinOp(self, node):
        """Анализирует бинарные операции

        Args:
            node: Узел AST бинарной операции

        Returns:
            None
        """
        is_add = isinstance(node.op, ast.Add)
        if not is_add:
            return

        # Проверяем, является ли одна из сторон строковой константой
        # (или результатом другой склейки строк)
        left_is_str = False
        right_is_str = False
        
        # Проверка для Python 3.8+
        if hasattr(ast, 'Constant'):
            if isinstance(node.left, ast.Constant) and isinstance(node.left.value, str):
                left_is_str = True
            if isinstance(node.right, ast.Constant) and isinstance(node.right.value, str):
                right_is_str = True
        
        # Проверка для Python < 3.8
        if hasattr(ast, 'Str'):
            if isinstance(node.left, ast.Str):
                left_is_str = True
            if isinstance(node.right, ast.Str):
                right_is_str = True
                
        # Также проверяем, если одна из сторон - другая бинарная операция (склейка цепочкой)
        if not left_is_str and isinstance(node.left, ast.BinOp) and isinstance(node.left.op, ast.Add):
            left_is_str = True
            
        if left_is_str or right_is_str:
            # Исключаем простые пути в стиле 'prefix/' + filename
            # но только если это короткие строки.
            self.add_error(
                self.current_file, 
                node.lineno, 
                "Avoid string concatenation with '+'. Use f-strings or .format() instead"
            )

        self.generic_visit(node)
