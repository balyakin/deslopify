import ast
import os
from core.base_checker import BaseChecker


class LogExceptionInExceptChecker(BaseChecker):
    """Проверяет использование log.exception() в блоках except"""

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
            
        super(LogExceptionInExceptChecker, self).process_file(filename, tree)

    def visit_ExceptHandler(self, node):
        """Анализирует блоки except

        Args:
            node: Узел AST обработчика исключений

        Returns:
            None
        """
        # Ищем вызовы логгера внутри тела except
        for sub_node in ast.walk(node):
            if not isinstance(sub_node, ast.Call):
                continue
                
            if not isinstance(sub_node.func, ast.Attribute):
                continue
                
            attr = sub_node.func
            # Проверяем вызовы типа log.error, log.critical, log.warning
            if attr.attr in ('error', 'critical', 'warning'):
                # Если в имени переменной есть 'log', это скорее всего логгер
                is_logger = 'log' in str(attr.value).lower()
                if not is_logger and isinstance(attr.value, ast.Name):
                    is_logger = 'log' in attr.value.id.lower() or 'logger' in attr.value.id.lower()
                
                if is_logger:
                    self.add_error(
                        self.current_file, 
                        sub_node.lineno, 
                        "Use log.exception(...) instead of log.{0}(...) in except block".format(attr.attr)
                    )
                    
        self.generic_visit(node)
