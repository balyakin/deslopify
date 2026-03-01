import ast
import os
from core.base_checker import BaseChecker


class AsyncForExecuteChecker(BaseChecker):
    """Проверяет использование async for row in conn.execute(query) вместо fetchall()"""

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
            
        super(AsyncForExecuteChecker, self).process_file(filename, tree)

    def visit_Call(self, node):
        """Анализирует вызовы функций

        Args:
            node: Узел AST вызова

        Returns:
            None
        """
        if not isinstance(node.func, ast.Attribute):
            return

        attr = node.func
        # Ищем вызовы .fetchall() или .fetchmany()
        if attr.attr in ('fetchall', 'fetchmany'):
            # Проверяем, был ли перед этим await conn.execute(...)
            # Обычно это выглядит как (await conn.execute(query)).fetchall()
            is_await_execute = False
            if isinstance(attr.value, ast.Await):
                await_node = attr.value
                if isinstance(await_node.value, ast.Call):
                    call_node = await_node.value
                    if isinstance(call_node.func, ast.Attribute) and call_node.func.attr == 'execute':
                        is_await_execute = True
            
            # Или просто вызов на объекте, полученном из execute
            # (сложнее отследить без полноценного анализа типов)
            if is_await_execute:
                self.add_error(
                    self.current_file, 
                    node.lineno, 
                    "Use 'async for row in conn.execute(query)' instead of fetchall()"
                )

        self.generic_visit(node)
