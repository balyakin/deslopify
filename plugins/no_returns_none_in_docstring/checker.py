import ast
import os
from core.base_checker import BaseChecker


class NoReturnsNoneInDocstringChecker(BaseChecker):
    """Проверяет отсутствие Returns: None в докстрингах"""

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
            
        super(NoReturnsNoneInDocstringChecker, self).process_file(filename, tree)

    def _check_docstring(self, node):
        """Проверяет докстринг на наличие Returns: None

        Args:
            node: Узел AST функции

        Returns:
            None
        """
        docstring = ast.get_docstring(node)
        if not docstring:
            return
            
        # Ищем Returns: None или Returns:None (регистронезависимо)
        doc_lower = docstring.lower()
        if "returns: none" in doc_lower or "returns:none" in doc_lower:
            self.add_error(
                self.current_file, 
                node.lineno, 
                "Remove 'Returns: None' from docstring as it's redundant"
            )

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
