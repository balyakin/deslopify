import ast
import os
from core.base_checker import BaseChecker


class SqlAlchemyDateTimeTimezoneChecker(BaseChecker):
    """Проверяет наличие timezone=True у DateTime в SQLAlchemy"""

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
            
        super(SqlAlchemyDateTimeTimezoneChecker, self).process_file(filename, tree)

    def visit_Call(self, node):
        """Анализирует вызовы DateTime()

        Args:
            node: Узел AST вызова

        Returns:
            None
        """
        is_name = isinstance(node.func, ast.Name) and node.func.id == 'DateTime'
        is_attr = isinstance(node.func, ast.Attribute) and node.func.attr == 'DateTime'
        
        if is_name or is_attr:
            # Ищем аргумент 'timezone'
            has_timezone_true = False
            for keyword in node.keywords:
                if keyword.arg == 'timezone':
                    # Проверяем что это True
                    is_true = False
                    is_constant = isinstance(keyword.value, getattr(ast, 'Constant', type(None)))
                    if is_constant and keyword.value.value is True:
                        is_true = True
                    
                    # Для Python < 3.8
                    is_name_true = isinstance(keyword.value, ast.Name) and keyword.value.id == 'True'
                    if is_true or is_name_true:
                        has_timezone_true = True
                        break
            
            if not has_timezone_true:
                self.add_error(self.current_file, node.lineno, "DateTime must have timezone=True")
                
        self.generic_visit(node)
