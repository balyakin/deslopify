import ast
import os
from core.base_checker import BaseChecker


class LoggingConfigInCodeChecker(BaseChecker):
    """Проверяет наличие настройки логирования прямо в коде"""

    def process_file(self, filename, tree):
        """Пропускает файлы тестов и конфигурационные файлы

        Args:
            filename: Имя обрабатываемого файла
            tree: AST дерево файла

        Returns:
            None
        """
        file_basename = os.path.basename(filename)
        is_test_file = file_basename.startswith('test_')
        is_config_file = 'config' in file_basename.lower()
        
        if is_test_file or is_config_file:
            return
            
        super(LoggingConfigInCodeChecker, self).process_file(filename, tree)

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
            is_logging_module = isinstance(attr.value, ast.Name) and attr.value.id == 'logging'
            
            # Проверка logging.basicConfig(...)
            if is_logging_module and attr.attr == 'basicConfig':
                self.add_error(self.current_file, node.lineno, "Logging should be configured only in config file")
            
            # Проверка logging.config.dictConfig(...) или fileConfig
            is_logging_config = False
            is_sub_attribute = isinstance(attr.value, ast.Attribute)
            if is_sub_attribute:
                sub_attr = attr.value
                is_sub_logging = isinstance(sub_attr.value, ast.Name) and sub_attr.value.id == 'logging'
                is_sub_config = sub_attr.attr == 'config'
                if is_sub_logging and is_sub_config:
                    is_logging_config = True
            
            if is_logging_config and attr.attr in ('dictConfig', 'fileConfig'):
                self.add_error(self.current_file, node.lineno, "Logging should be configured only in config file")
                
        self.generic_visit(node)
