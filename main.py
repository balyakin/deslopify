import os
import sys
from plugin_manager import load_plugins
from runner import run_analysis, Colors


def print_errors(errors):
    """Выводит список ошибок в консоль

    Args:
        errors: Список словарей с информацией об ошибках

    Returns:
        None
    """
    print("\n--- Общий список ошибок ---")
    if not errors:
        print("{0}Все проверенные проекты/файлы в порядке.{1}".format(Colors.GREEN, Colors.RESET))
        return

    print("{0}Обнаружено ошибок: {1}{2}".format(Colors.RED, len(errors), Colors.RESET))
    for error_info in errors:
        file_path = error_info.get('file', 'Unknown')
        line_number = error_info.get('line', 0)
        message = error_info.get('message', '')
        
        error_string = "{0}Файл:{1} {2}, {0}Строка:{1} {3} - {4}".format(
            Colors.YELLOW, Colors.RESET, file_path, line_number, message
        )
        print(error_string)


def main():
    """Основная функция запуска программы

    Returns:
        None
    """
    target_directory = os.getcwd()
    
    checkers = load_plugins()
    if not checkers:
        print("{0}Плагины не найдены{1}".format(Colors.YELLOW, Colors.RESET))
        return
        
    errors = run_analysis(target_directory, checkers)
    print_errors(errors)
    
    if errors:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
