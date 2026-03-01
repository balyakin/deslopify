import ast
import os
from core.base_checker import BaseChecker


class NoUuidInTestsChecker(BaseChecker):
    """Проверяет отсутствие генерации случайных UUID в тестах"""

    def process_file(self, filename, tree):
        """Проверяет ТОЛЬКО файлы тестов

        Args:
            filename: Имя обрабатываемого файла
            tree: AST дерево файла

        Returns:
            None
        """
        file_basename = os.path.basename(filename)
        is_test_file = file_basename.startswith('test_') or 'example' in file_basename
        
        # Если это не тест, пропускаем проверку (в обычном коде UUID разрешены)
        if not is_test_file:
            return
            
        super(NoUuidInTestsChecker, self).process_file(filename, tree)

    def visit_Call(self, node):
        """Анализирует вызовы функций

        Args:
            node: Узел AST вызова

        Returns:
            None
        """
        is_attribute = isinstance(node.func, ast.Attribute)
        if is_attribute:
            attr = node.func
            is_uuid_module = isinstance(attr.value, ast.Name) and attr.value.id == 'uuid'
            
            # Проверка uuid.uuid4() или uuid.uuid1()
            if is_uuid_module and attr.attr in ('uuid1', 'uuid4'):
                self.add_error(self.current_file, node.lineno, "Use hardcoded constants instead of random UUID in tests")
                
        self.generic_visit(node)
