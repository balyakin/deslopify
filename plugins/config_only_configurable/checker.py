import ast
import os
from core.base_checker import BaseChecker


class ConfigOnlyConfigurableChecker(BaseChecker):
    """Проверяет наличие неконфигурабельных данных (имен таблиц/колонок) в файлах конфигурации"""

    # Имена переменных, которые должны быть в const.py, а не в config.py
    _BAD_CONST_SUFFIXES = ('_TABLE', '_COLUMN', '_FIELD', '_ID_KEY')
    _BAD_CONST_KEYWORDS = ('TABLE_NAME', 'DB_SCHEMA')

    def process_file(self, filename, tree):
        """Проверяет ТОЛЬКО файлы конфигурации

        Args:
            filename: Имя обрабатываемого файла
            tree: AST дерево файла

        Returns:
            None
        """
        file_basename = os.path.basename(filename).lower()
        is_config_file = 'config' in file_basename or 'example' in file_basename
        
        # Если это не файл конфигурации, пропускаем
        if not is_config_file:
            return
            
        super(ConfigOnlyConfigurableChecker, self).process_file(filename, tree)

    def visit_Assign(self, node):
        """Анализирует присваивания констант

        Args:
            node: Узел AST присваивания

        Returns:
            None
        """
        for target in node.targets:
            is_name = isinstance(target, ast.Name)
            if not is_name:
                continue
                
            var_name = target.id.upper()
            
            # Проверяем суффиксы
            is_bad = any(var_name.endswith(suffix) for suffix in self._BAD_CONST_SUFFIXES)
            
            # Проверяем ключевые слова
            if not is_bad:
                is_bad = any(keyword in var_name for keyword in self._BAD_CONST_KEYWORDS)
                
            if is_bad:
                message = "Constant '{0}' should be in const.py, not in config file".format(target.id)
                self.add_error(self.current_file, node.lineno, message)
                
        self.generic_visit(node)
