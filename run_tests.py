import os
import sys
import ast
import inspect
from plugin_manager import load_plugins
from runner import Colors


def run_plugin_tests():
    """Запускает тесты для всех загруженных плагинов

    Returns:
        Булево значение (True если все тесты прошли успешно)
    """
    checkers = load_plugins()
    all_passed = True

    print("--- Запуск тестов плагинов ---")
    
    if not checkers:
        print("{0}Плагины не найдены для тестирования{1}".format(Colors.YELLOW, Colors.RESET))
        return False

    for checker in checkers:
        plugin_name = checker.__class__.__name__
        module_path = inspect.getfile(checker.__class__)
        plugin_dir = os.path.dirname(module_path)
        
        pass_file = os.path.join(plugin_dir, 'example_pass.py')
        fail_file = os.path.join(plugin_dir, 'example_fail.py')

        checker_passed = True
        missing_files = False

        if not os.path.exists(pass_file):
            print("[{0}WARN{1}] {2} - Отсутствует example_pass.py".format(Colors.YELLOW, Colors.RESET, plugin_name))
            missing_files = True
        else:
            checker.errors = []
            with open(pass_file, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
            checker.process_file(pass_file, tree)
            checker.finalize()
            if len(checker.errors) > 0:
                print("[{0}FAIL{1}] {2} - Нашел ошибки в валидном коде (example_pass.py)".format(Colors.RED, Colors.RESET, plugin_name))
                checker_passed = False

        if not os.path.exists(fail_file):
            print("[{0}WARN{1}] {2} - Отсутствует example_fail.py".format(Colors.YELLOW, Colors.RESET, plugin_name))
            missing_files = True
        else:
            checker.errors = []
            with open(fail_file, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
            checker.process_file(fail_file, tree)
            checker.finalize()
            if len(checker.errors) == 0:
                print("[{0}FAIL{1}] {2} - Не нашел ошибок в плохом коде (example_fail.py)".format(Colors.RED, Colors.RESET, plugin_name))
                checker_passed = False

        if checker_passed and not missing_files:
            print("[{0}OK{1}]   {2}".format(Colors.GREEN, Colors.RESET, plugin_name))
        elif checker_passed and missing_files:
            all_passed = False

    return all_passed


if __name__ == '__main__':
    success = run_plugin_tests()
    sys.exit(0 if success else 1)
