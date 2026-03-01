import ast
import os
import re
from core.base_checker import BaseChecker


class RpcMethodDocstringChecker(BaseChecker):
    """Проверяет наличие русских докстрингов у RPC-методов"""

    # Регулярное выражение для поиска кириллицы
    _CYRILLIC_REGEX = re.compile(r'[а-яА-ЯёЁ]')

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
            
        super(RpcMethodDocstringChecker, self).process_file(filename, tree)

    def _check_docstring(self, node):
        """Проверяет докстринг функции

        Args:
            node: Узел AST функции

        Returns:
            None
        """
        if not node.name.startswith('rpc_'):
            return

        docstring = ast.get_docstring(node)
        if not docstring:
            message = "RPC method '{0}' must have a docstring".format(node.name)
            self.add_error(self.current_file, node.lineno, message)
            return

        # Проверка на кириллицу
        if not self._CYRILLIC_REGEX.search(docstring):
            message = "Docstring for RPC method '{0}' must be in Russian".format(node.name)
            self.add_error(self.current_file, node.lineno, message)

        # Проверка отсутствия точки в конце первого предложения (согласно правилам проекта)
        first_line = docstring.strip().split('\n')[0]
        if first_line.endswith('.'):
            message = "Docstring for RPC method '{0}' should not end with a dot".format(node.name)
            self.add_error(self.current_file, node.lineno, message)

    def visit_FunctionDef(self, node):
        """Анализирует стандартные функции

        Args:
            node: Узел AST

        Returns:
            None
        """
        self._check_docstring(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        """Анализирует асинхронные функции

        Args:
            node: Узел AST

        Returns:
            None
        """
        self._check_docstring(node)
        self.generic_visit(node)
