import ast
import os
from core.base_checker import BaseChecker


class UseIsoparseChecker(BaseChecker):
    """Проверяет использование isoparse() из dateutil.parser для строк с датой"""

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
            
        super(UseIsoparseChecker, self).process_file(filename, tree)

    def visit_Call(self, node):
        """Анализирует вызовы функций

        Args:
            node: Узел AST вызова

        Returns:
            None
        """
        is_attr = isinstance(node.func, ast.Attribute)
        if is_attr:
            attr = node.func
            # Проверка datetime.strptime(...)
            is_datetime = isinstance(attr.value, ast.Name) and attr.value.id == 'datetime'
            if is_datetime and attr.attr == 'strptime':
                self.add_error(
                    self.current_file, 
                    node.lineno, 
                    "Use from dateutil.parser import isoparse instead of datetime.strptime"
                )
            
            # Проверка date.fromisoformat(...) или datetime.fromisoformat(...)
            if attr.attr == 'fromisoformat':
                self.add_error(
                    self.current_file, 
                    node.lineno, 
                    "Use isoparse() from dateutil.parser instead of .fromisoformat()"
                )
                
        self.generic_visit(node)
