import ast
import os
from core.base_checker import BaseChecker


class UnnecessaryClassChecker(BaseChecker):
    """Проверяет наличие классов, используемых только как пространства имен"""

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
            
        super(UnnecessaryClassChecker, self).process_file(filename, tree)

    def _is_abstract_base_class(self, node):
        """Проверяет является ли класс абстрактным базовым классом

        Args:
            node: Узел AST класса

        Returns:
            Булево значение
        """
        for base in node.bases:
            is_name = isinstance(base, ast.Name)
            if is_name and base.id == 'ABC':
                return True
                
            is_attribute = isinstance(base, ast.Attribute)
            if is_attribute and base.attr == 'ABC':
                return True
        return False

    def visit_ClassDef(self, node):
        """Анализирует определение класса

        Args:
            node: Узел AST класса

        Returns:
            None
        """
        if self._is_abstract_base_class(node):
            return

        has_init = False
        has_instance_methods = False
        has_state_attributes = False
        
        # Проверяем методы и атрибуты класса
        for item in node.body:
            is_function = isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
            if is_function:
                if item.name == '__init__':
                    has_init = True
                    continue
                
                # Проверяем декораторы на предмет staticmethod или classmethod
                is_static = False
                for decorator in item.decorator_list:
                    is_name = isinstance(decorator, ast.Name)
                    if is_name and decorator.id in ('staticmethod', 'classmethod'):
                        is_static = True
                        break
                
                if not is_static:
                    has_instance_methods = True
            
            # Если есть простые присваивания в теле класса, это могут быть константы
            # Мы их пока не считаем за "состояние" в данном контексте, 
            # так как это могут быть просто пространства имен для констант.
            # Но если это не константы (верхний регистр), то возможно это состояние.
            if isinstance(item, ast.Assign):
                for target in item.targets:
                    is_name = isinstance(target, ast.Name)
                    if is_name and not target.id.isupper():
                        has_state_attributes = True

        # Если в классе нет __init__, нет методов экземпляра (без декораторов)
        # и нет атрибутов состояния (не констант), то класс не нужен.
        if not has_init and not has_instance_methods and not has_state_attributes:
            # Разрешаем пустые классы-исключения или просто пустые структуры, если они для чего-то нужны
            # Но если там только статические методы - это ошибка.
            has_methods = any(isinstance(i, (ast.FunctionDef, ast.AsyncFunctionDef)) for i in node.body)
            if has_methods:
                message = "Class '{0}' is used as a namespace. Use a module instead".format(node.name)
                self.add_error(self.current_file, node.lineno, message)
            
        self.generic_visit(node)
