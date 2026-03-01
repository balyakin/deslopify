import ast
import os
import re
from core.base_checker import BaseChecker


class PortInCodeChecker(BaseChecker):
    """Проверяет наличие жестко заданных портов в коде"""

    # Регулярное выражение для поиска порта в URL (например, :8000/)
    _PORT_URL_REGEX = re.compile(r':(\d{2,5})(/|$)')
    
    # Список имен аргументов, которые часто принимают порт
    _PORT_ARG_NAMES = ('port', 'listen_port', 'server_port')
    
    # Список имен функций, которые могут принимать порт
    _PORT_FUNC_NAMES = ('run', 'listen', 'serve', 'start_server', 'create_server')

    def process_file(self, filename, tree):
        """Пропускает файлы тестов и конфиги

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
            
        super(PortInCodeChecker, self).process_file(filename, tree)

    def _check_value_for_port(self, value_node, context_name=None):
        """Проверяет значение на наличие порта

        Args:
            value_node: Узел AST со значением
            context_name: Имя аргумента или функции для уточнения контекста

        Returns:
            None
        """
        # Проверка числовых литералов (Python 3.8+)
        is_constant = isinstance(value_node, getattr(ast, 'Constant', type(None)))
        if is_constant:
            val = value_node.value
            if isinstance(val, int) and 80 <= val <= 65535:
                # Если это явно аргумент 'port' или внутри сетевой функции
                if context_name in self._PORT_ARG_NAMES or context_name in self._PORT_FUNC_NAMES:
                    self.add_error(self.current_file, value_node.lineno, "Port {0} should be taken from config".format(val))
            
            # Проверка строк на наличие порта в URL
            if isinstance(val, str):
                match = self._PORT_URL_REGEX.search(val)
                if match:
                    self.add_error(self.current_file, value_node.lineno, "URL contains hardcoded port: '{0}'".format(val))

        # Проверка числовых литералов (Python < 3.8)
        is_num = isinstance(value_node, getattr(ast, 'Num', type(None)))
        if is_num:
            val = value_node.n
            if isinstance(val, int) and 80 <= val <= 65535:
                if context_name in self._PORT_ARG_NAMES or context_name in self._PORT_FUNC_NAMES:
                    self.add_error(self.current_file, value_node.lineno, "Port {0} should be taken from config".format(val))

        # Проверка строковых литералов (Python < 3.8)
        is_str = isinstance(value_node, getattr(ast, 'Str', type(None)))
        if is_str:
            val = value_node.s
            match = self._PORT_URL_REGEX.search(val)
            if match:
                self.add_error(self.current_file, value_node.lineno, "URL contains hardcoded port: '{0}'".format(val))

    def visit_Call(self, node):
        """Анализирует вызовы функций

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
            
        # Проверяем позиционные аргументы, если функция подозрительная
        if func_name in self._PORT_FUNC_NAMES:
            for arg in node.args:
                self._check_value_for_port(arg, func_name)
        
        # Проверяем именованные аргументы
        for keyword in node.keywords:
            self._check_value_for_port(keyword.value, keyword.arg)
            
        self.generic_visit(node)

    def visit_Assign(self, node):
        """Анализирует присваивания (например, PORT = 8080)

        Args:
            node: Узел AST присваивания

        Returns:
            None
        """
        for target in node.targets:
            is_name = isinstance(target, ast.Name)
            if is_name:
                var_name = target.id.lower()
                if 'port' in var_name:
                    self._check_value_for_port(node.value, target.id)
        self.generic_visit(node)
