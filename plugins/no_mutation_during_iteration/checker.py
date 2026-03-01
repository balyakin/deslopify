import ast
import os
from core.base_checker import BaseChecker


class NoMutationDuringIterationChecker(BaseChecker):
    """Проверяет изменение списка/словаря во время итерации"""

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
            
        super(NoMutationDuringIterationChecker, self).process_file(filename, tree)

    def visit_For(self, node):
        """Анализирует циклы for

        Args:
            node: Узел AST цикла

        Returns:
            None
        """
        # Название итерируемого объекта
        iter_name = None
        if isinstance(node.iter, ast.Name):
            iter_name = node.iter.id
        elif isinstance(node.iter, ast.Call):
            # Проверка для list(my_dict.keys()) - это безопасно
            if isinstance(node.iter.func, ast.Name) and node.iter.func.id in ('list', 'set'):
                pass # Это копия, мутация разрешена
            elif isinstance(node.iter.func, ast.Attribute) and node.iter.func.attr in ('keys', 'values', 'items'):
                if isinstance(node.iter.func.value, ast.Name):
                    iter_name = node.iter.func.value.id

        if iter_name:
            # Ищем вызовы .pop(), .remove(), del или .clear() для этого объекта внутри тела цикла
            for sub_node in ast.walk(node):
                # Проверка del obj[key]
                if isinstance(sub_node, ast.Delete):
                    for target in sub_node.targets:
                        if isinstance(target, ast.Subscript) and isinstance(target.value, ast.Name):
                            if target.value.id == iter_name:
                                self.add_error(
                                    self.current_file, 
                                    sub_node.lineno, 
                                    "Don't delete items from '{0}' while iterating over it".format(iter_name)
                                )
                
                # Проверка obj.pop(), obj.remove()
                if isinstance(sub_node, ast.Call) and isinstance(sub_node.func, ast.Attribute):
                    if isinstance(sub_node.func.value, ast.Name) and sub_node.func.value.id == iter_name:
                        if sub_node.func.attr in ('pop', 'remove', 'clear'):
                            self.add_error(
                                self.current_file, 
                                sub_node.lineno, 
                                "Don't mutate '{0}' while iterating over it (use pop/remove)".format(iter_name)
                            )
                            
        self.generic_visit(node)
