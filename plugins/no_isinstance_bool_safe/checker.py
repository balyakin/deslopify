import ast
import os
from core.base_checker import BaseChecker


class NoIsinstanceBoolSafeChecker(BaseChecker):
    """Проверяет использование type(a) is int вместо isinstance(a, int)"""

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
            
        super(NoIsinstanceBoolSafeChecker, self).process_file(filename, tree)

    def visit_Call(self, node):
        """Анализирует вызовы функций

        Args:
            node: Узел AST вызова

        Returns:
            None
        """
        is_isinstance = isinstance(node.func, ast.Name) and node.func.id == 'isinstance'
        if is_isinstance and len(node.args) == 2:
            second_arg = node.args[1]
            # Проверяем, что второй аргумент - int или float
            is_int_or_float = False
            if isinstance(second_arg, ast.Name) and second_arg.id in ('int', 'float'):
                is_int_or_float = True
            elif isinstance(second_arg, ast.Tuple):
                for elt in second_arg.elts:
                    if isinstance(elt, ast.Name) and elt.id in ('int', 'float'):
                        is_int_or_float = True
                        break
            
            if is_int_or_float:
                self.add_error(
                    self.current_file, 
                    node.lineno, 
                    "Use 'type(a) is int' instead of 'isinstance(a, int)' for boolean safety"
                )

        self.generic_visit(node)
