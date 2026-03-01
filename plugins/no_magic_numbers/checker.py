import ast
import os
from core.base_checker import BaseChecker


class NoMagicNumbersChecker(BaseChecker):
    """Проверяет отсутствие магических чисел в коде"""

    # Разрешенные числа
    _ALLOWED_NUMBERS = (0, 1, -1, 100, 1024)

    def process_file(self, filename, tree):
        """Пропускает файлы тестов и устанавливает родительские связи

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
            
        # Проставляем родителей
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                child.parent = node
                
        super(NoMagicNumbersChecker, self).process_file(filename, tree)

    def _is_constant_definition(self, node):
        """Проверяет является ли узел определением константы (UPPER_CASE)

        Args:
            node: Узел AST

        Returns:
            Булево значение
        """
        # Идем вверх по дереву до присваивания
        parent = getattr(node, 'parent', None)
        if isinstance(parent, ast.Assign):
            for target in parent.targets:
                if isinstance(target, ast.Name) and target.id.isupper():
                    return True
        return False

    def visit_Num(self, node):
        """Анализирует числовые литералы (Python < 3.8)

        Args:
            node: Узел AST числа

        Returns:
            None
        """
        if node.n not in self._ALLOWED_NUMBERS:
            if not self._is_constant_definition(node):
                self.add_error(self.current_file, node.lineno, "Use named constants instead of magic number '{0}'".format(node.n))
        self.generic_visit(node)

    def visit_Constant(self, node):
        """Анализирует константы (Python >= 3.8)

        Args:
            node: Узел AST константы

        Returns:
            None
        """
        val = node.value
        if isinstance(val, (int, float)) and not isinstance(val, bool):
            if val not in self._ALLOWED_NUMBERS:
                if not self._is_constant_definition(node):
                    self.add_error(self.current_file, node.lineno, "Use named constants instead of magic number '{0}'".format(val))
        self.generic_visit(node)
