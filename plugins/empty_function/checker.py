import os
import ast
from core.base_checker import BaseChecker


class EmptyFunctionChecker(BaseChecker):
    """Проверяет наличие пустых функций состоящих только из pass или многоточия"""

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
            
        super(EmptyFunctionChecker, self).process_file(filename, tree)

    def _is_abstract_method(self, node):
        """Проверяет является ли метод абстрактным

        Args:
            node: Узел AST функции

        Returns:
            Булево значение
        """
        if not hasattr(node, 'decorator_list'):
            return False
            
        for decorator in node.decorator_list:
            is_name = isinstance(decorator, ast.Name)
            if is_name and decorator.id == 'abstractmethod':
                return True
                
            is_attribute = isinstance(decorator, ast.Attribute)
            if is_attribute and decorator.attr == 'abstractmethod':
                return True
                
        return False

    def _is_empty_statement(self, stmt):
        """Проверяет является ли инструкция пустой конструкцией

        Args:
            stmt: Инструкция AST

        Returns:
            Булево значение
        """
        if isinstance(stmt, ast.Pass):
            return True
            
        if isinstance(stmt, ast.Expr):
            value = stmt.value
            
            # Проверка на строку докстринга для Python 3.5
            is_str_35 = isinstance(value, getattr(ast, 'Str', type(None)))
            if is_str_35:
                return True
                
            # Проверка на строку докстринга для Python 3.8+
            ast_constant = getattr(ast, 'Constant', type(None))
            is_constant_38 = isinstance(value, ast_constant)
            if is_constant_38 and isinstance(getattr(value, 'value', None), str):
                return True
            
            # Проверка на многоточие для Python 3.5
            is_ellipsis_35 = type(value).__name__ == 'Ellipsis'
            if is_ellipsis_35:
                return True
                
            # Проверка на многоточие для Python 3.8+
            if is_constant_38 and getattr(value, 'value', None) is Ellipsis:
                return True
                
        return False

    def _check_function_node(self, node):
        """Анализирует тело функции на наличие реального кода

        Args:
            node: Узел AST функции

        Returns:
            None
        """
        is_abstract = self._is_abstract_method(node)
        if is_abstract:
            return
            
        has_real_code = False
        for stmt in node.body:
            is_empty = self._is_empty_statement(stmt)
            if not is_empty:
                has_real_code = True
                break
                
        if not has_real_code:
            error_message = "Function '{0}' is empty (contains only pass/docstring/...)".format(node.name)
            self.add_error(self.current_file, node.lineno, error_message)

    def visit_FunctionDef(self, node):
        """Анализирует стандартные функции

        Args:
            node: Узел AST

        Returns:
            None
        """
        self._check_function_node(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        """Анализирует асинхронные функции

        Args:
            node: Узел AST

        Returns:
            None
        """
        self._check_function_node(node)
        self.generic_visit(node)
