import ast
import os
from core.base_checker import BaseChecker


class NoEnumCastChecker(BaseChecker):
    """Проверяет отсутствие кастов Enum к int (нужно использовать .value)"""

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
            
        super(NoEnumCastChecker, self).process_file(filename, tree)

    def visit_Call(self, node):
        """Анализирует вызовы функций

        Args:
            node: Узел AST вызова

        Returns:
            None
        """
        is_name = isinstance(node.func, ast.Name)
        if is_name and node.func.id == 'int' and len(node.args) == 1:
            arg = node.args[0]
            
            # Если аргумент - это доступ к атрибуту (например, MyEnum.STATUS)
            # или если в имени аргумента есть 'enum', 'status', 'type'
            is_attr = isinstance(arg, ast.Attribute)
            is_enum_like = False
            if is_attr:
                is_enum_like = True # Доступ к атрибуту в int() подозрителен
            
            is_name_arg = isinstance(arg, ast.Name)
            if is_name_arg:
                lower_name = arg.id.lower()
                if any(k in lower_name for k in ('enum', 'status', 'type', 'state')):
                    is_enum_like = True
            
            if is_enum_like:
                self.add_error(self.current_file, node.lineno, "Avoid int() cast for Enums. Use .value instead")
                
        self.generic_visit(node)
