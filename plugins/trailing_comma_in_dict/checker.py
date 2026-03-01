import ast
import os
from core.base_checker import BaseChecker


class TrailingCommaInDictChecker(BaseChecker):
    """Проверяет наличие завершающей запятой в многострочных словарях"""

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
            
        super(TrailingCommaInDictChecker, self).process_file(filename, tree)

    def visit_Dict(self, node):
        """Анализирует словари

        Args:
            node: Узел AST словаря

        Returns:
            None
        """
        if not node.keys:
            return

        # Проверяем многострочный ли это словарь
        # (номер строки первого ключа отличается от номера строки последнего)
        first_key = node.keys[0]
        last_val = node.values[-1]
        
        if first_key.lineno == last_val.lineno:
            # Однострочный словарь, запятая не обязательна
            return

        # AST не хранит информацию о запятых напрямую. 
        # Нам нужно прочитать файл и посмотреть символ перед закрывающей скобкой.
        try:
            with open(self.current_file, 'r') as f:
                lines = f.readlines()
            
            # Находим строку, где закрывается словарь
            # node.end_lineno (Python 3.8+)
            end_lineno = getattr(node, 'end_lineno', last_val.lineno)
            
            # Ищем закрывающую скобку '}' начиная со строки после последнего значения
            found_comma = False
            for i in range(last_val.lineno - 1, end_lineno):
                line = lines[i].strip()
                if ',' in line and ('}' in line or i > last_val.lineno - 1):
                    # Очень упрощенная проверка: ищем запятую в строке с последним элементом
                    # или в последующих строках перед закрытием
                    if ',' in lines[last_val.lineno - 1]:
                        found_comma = True
                        break
            
            if not found_comma:
                # Еще одна попытка: ищем запятую прямо за последним значением в той же строке
                last_line = lines[last_val.lineno - 1]
                # Находим позицию последнего значения (если доступно)
                # или просто ищем запятую после текста
                if ',' not in last_line.split('#')[0]: # Игнорируем комментарии
                    self.add_error(
                        self.current_file, 
                        last_val.lineno, 
                        "Multiline dictionary should have a trailing comma"
                    )
        except Exception:
            # Если не удалось прочитать файл, пропускаем
            pass

        self.generic_visit(node)
