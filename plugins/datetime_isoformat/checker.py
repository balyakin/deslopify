import ast
import os
from core.base_checker import BaseChecker


class DatetimeIsoformatChecker(BaseChecker):
    """Проверяет преобразование дат в строку (нужно использовать .isoformat())"""

    _DATE_KEYWORDS = ('date', 'time', 'dt', 'created', 'updated', 'at')

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
            
        super(DatetimeIsoformatChecker, self).process_file(filename, tree)

    def _is_date_like(self, node):
        """Проверяет узел на сходство с датой по имени переменной

        Args:
            node: Узел AST

        Returns:
            Булево значение
        """
        is_name = isinstance(node, ast.Name)
        if is_name:
            name_lower = node.id.lower()
            return any(k in name_lower for k in self._DATE_KEYWORDS)
            
        is_attr = isinstance(node, ast.Attribute)
        if is_attr:
            attr_lower = node.attr.lower()
            return any(k in attr_lower for k in self._DATE_KEYWORDS)
            
        return False

    def visit_Call(self, node):
        """Анализирует вызовы функций

        Args:
            node: Узел AST вызова

        Returns:
            None
        """
        is_name = isinstance(node.func, ast.Name)
        
        # Проверка str(dt)
        if is_name and node.func.id == 'str' and len(node.args) == 1:
            if self._is_date_like(node.args[0]):
                self.add_error(self.current_file, node.lineno, "Use .isoformat() to convert datetime to string")
        
        # Проверка dt.strftime(...)
        is_attr = isinstance(node.func, ast.Attribute)
        if is_attr and node.func.attr == 'strftime':
            if self._is_date_like(node.func.value):
                self.add_error(self.current_file, node.lineno, "Use .isoformat() instead of .strftime() if possible")
                
        self.generic_visit(node)

    def visit_JoinedStr(self, node):
        """Анализирует f-строки (Python 3.6+)

        Args:
            node: Узел AST f-строки

        Returns:
            None
        """
        for value in node.values:
            is_formatted = isinstance(value, ast.FormattedValue)
            if is_formatted:
                if self._is_date_like(value.value):
                    self.add_error(self.current_file, node.lineno, "Use .isoformat() to format datetime in f-string")
        self.generic_visit(node)
