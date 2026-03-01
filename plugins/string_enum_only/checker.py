import ast
import os
from core.base_checker import BaseChecker


class StringEnumOnlyChecker(BaseChecker):
    """Проверяет чтобы все Enum были строковыми (наследовались от str)"""

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
            
        super(StringEnumOnlyChecker, self).process_file(filename, tree)

    def visit_ClassDef(self, node):
        """Анализирует определение класса

        Args:
            node: Узел AST класса

        Returns:
            None
        """
        is_enum = False
        has_str_base = False
        
        for base in node.bases:
            # Проверяем наследование от Enum или IntEnum
            is_name_enum = isinstance(base, ast.Name) and base.id in ('Enum', 'IntEnum')
            is_attr_enum = isinstance(base, ast.Attribute) and base.attr in ('Enum', 'IntEnum')
            
            if is_name_enum or is_attr_enum:
                is_enum = True
                
            # Проверяем наследование от str
            is_str = isinstance(base, ast.Name) and base.id == 'str'
            if is_str:
                has_str_base = True
        
        if is_enum and not has_str_base:
            self.add_error(self.current_file, node.lineno, "Enum '{0}' should inherit from 'str' to be a string enum".format(node.name))
                
        self.generic_visit(node)
