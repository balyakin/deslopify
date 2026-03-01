import ast
import os
from core.base_checker import BaseChecker


class NoMethodCallsInInitChecker(BaseChecker):
    """Проверяет отсутствие вызовов методов в конструкторе (кроме super)"""

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
            
        super(NoMethodCallsInInitChecker, self).process_file(filename, tree)

    def visit_FunctionDef(self, node):
        """Анализирует стандартные функции

        Args:
            node: Узел AST

        Returns:
            None
        """
        if node.name == '__init__':
            self._check_init_body(node.body)
        self.generic_visit(node)

    def _check_init_body(self, body):
        """Рекурсивно проверяет тело __init__ на наличие вызовов методов self

        Args:
            body: Список узлов AST тела функции

        Returns:
            None
        """
        for stmt in body:
            # Ищем вызовы в текущем стейтменте
            for sub_node in ast.walk(stmt):
                is_call = isinstance(sub_node, ast.Call)
                if not is_call:
                    continue
                    
                is_attr = isinstance(sub_node.func, ast.Attribute)
                if is_attr:
                    # Проверяем вызов self.something()
                    is_self = isinstance(sub_node.func.value, ast.Name) and sub_node.func.value.id == 'self'
                    if is_self:
                        self.add_error(self.current_file, sub_node.lineno, "Don't call methods in __init__")
                
                # Проверка super().__init__() - это разрешено
                # Но другие вызовы super().method() - нет
                is_super_call = False
                is_name_super = isinstance(sub_node.func, ast.Attribute) and \
                                isinstance(sub_node.func.value, ast.Call) and \
                                isinstance(sub_node.func.value.func, ast.Name) and \
                                sub_node.func.value.func.id == 'super'
                
                if is_name_super and sub_node.func.attr != '__init__':
                    self.add_error(self.current_file, sub_node.lineno, "Don't call super methods (other than __init__) in constructor")
