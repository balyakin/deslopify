import ast
import os
from core.base_checker import BaseChecker


class SqlAlchemyNamedConstraintsChecker(BaseChecker):
    """Проверяет наличие имен у всех констрейнтов SQLAlchemy"""

    _CONSTRAINT_CLASSES = (
        'PrimaryKeyConstraint',
        'UniqueConstraint',
        'CheckConstraint',
        'ForeignKeyConstraint',
        'Index'
    )

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
            
        super(SqlAlchemyNamedConstraintsChecker, self).process_file(filename, tree)

    def visit_Call(self, node):
        """Анализирует вызовы конструкторов констрейнтов

        Args:
            node: Узел AST вызова

        Returns:
            None
        """
        func_name = ""
        is_name = isinstance(node.func, ast.Name)
        if is_name:
            func_name = node.func.id
        
        is_attr = isinstance(node.func, ast.Attribute)
        if is_attr:
            func_name = node.func.attr
            
        if func_name in self._CONSTRAINT_CLASSES:
            # Ищем аргумент 'name' в именованных аргументах
            has_name = any(kw.arg == 'name' for kw in node.keywords)
            
            # В Index имя обычно идет первым позиционным аргументом
            if func_name == 'Index' and len(node.args) >= 1:
                has_name = True
                
            if not has_name:
                self.add_error(self.current_file, node.lineno, "SQLAlchemy constraint '{0}' must have a name".format(func_name))
                
        self.generic_visit(node)
