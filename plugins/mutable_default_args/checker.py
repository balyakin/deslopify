import os
import ast
from core.base_checker import BaseChecker


class MutableDefaultArgsChecker(BaseChecker):
    """Проверяет использование изменяемых объектов в качестве значений по умолчанию"""

    def process_file(self, filename, tree):
        """Пропускает файлы тестов перед запуском анализа

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
            
        super(MutableDefaultArgsChecker, self).process_file(filename, tree)

    def _check_default_value(self, default_node, function_name):
        """Анализирует конкретный узел значения по умолчанию

        Args:
            default_node: Узел AST со значением по умолчанию
            function_name: Имя проверяемой функции

        Returns:
            None
        """
        is_list = isinstance(default_node, ast.List)
        is_dict = isinstance(default_node, ast.Dict)
        is_set = isinstance(default_node, ast.Set)
        
        is_bad_call = False
        is_call_node = isinstance(default_node, ast.Call)
        
        if is_call_node:
            func_node = default_node.func
            is_name_node = isinstance(func_node, ast.Name)
            if is_name_node:
                func_name = func_node.id
                if func_name in ('list', 'dict', 'set'):
                    is_bad_call = True

        if is_list or is_dict or is_set or is_bad_call:
            message = "Mutable default argument (list/dict/set) used in function '{0}'".format(function_name)
            self.add_error(self.current_file, default_node.lineno, message)

    def _check_function_args(self, node):
        """Проверяет все аргументы по умолчанию у функции

        Args:
            node: Узел AST функции

        Returns:
            None
        """
        # Проверка обычных позиционных аргументов с дефолтами
        for default_node in node.args.defaults:
            self._check_default_value(default_node, node.name)
            
        # Проверка keyword-only аргументов (появились в Python 3)
        has_kw_defaults = hasattr(node.args, 'kw_defaults')
        if has_kw_defaults:
            for default_node in node.args.kw_defaults:
                if default_node is not None:
                    self._check_default_value(default_node, node.name)

    def visit_FunctionDef(self, node):
        """Анализирует стандартные функции

        Args:
            node: Узел AST

        Returns:
            None
        """
        self._check_function_args(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        """Анализирует асинхронные функции

        Args:
            node: Узел AST

        Returns:
            None
        """
        self._check_function_args(node)
        self.generic_visit(node)
