import os
import ast


class Colors:
    """Цвета для вывода в консоль"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'


def get_ignored_directories():
    """Возвращает список директорий для игнорирования

    Returns:
        Список имен директорий
    """
    return ['.venv', 'venv', '.git', '.idea', '__pycache__']


def process_python_file(file_path, checkers):
    """Читает файл парсит его и передает чекерам

    Args:
        file_path: Путь к файлу
        checkers: Список чекеров для запуска

    Returns:
        None
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as source_file:
            source_code = source_file.read()
            
        tree = ast.parse(source_code)
        
        for checker in checkers:
            checker.process_file(file_path, tree)
            
    except (SyntaxError, IOError) as e:
        print("[{0}ERROR{1}] Не удалось обработать {2}: {3}".format(Colors.YELLOW, Colors.RESET, file_path, e))


def run_analysis(target_dir, checkers):
    """Запускает полный цикл проверки проекта

    Args:
        target_dir: Путь к проверяемой директории
        checkers: Список загруженных чекеров

    Returns:
        Список всех найденных ошибок
    """
    ignored_dirs = get_ignored_directories()
    
    print("--- Запуск статического анализа ---")
    
    # Фаза 1: Сбор данных по всем файлам (локальный анализ)
    for root, directories, files in os.walk(target_dir):
        valid_directories = []
        for directory_name in directories:
            if directory_name not in ignored_dirs:
                valid_directories.append(directory_name)
        directories[:] = valid_directories
        
        for file_name in files:
            is_python_file = file_name.endswith('.py')
            is_example_file = file_name.startswith('example_')
            
            if is_python_file and not is_example_file:
                file_path = os.path.join(root, file_name)
                process_python_file(file_path, checkers)
                
    # Фаза 2: Финализация (глобальный анализ) и вывод статуса по каждому чекеру
    all_errors = []
    for checker in checkers:
        checker_name = checker.__class__.__name__
        
        # Получаем возможные новые ошибки из финализации
        checker_errors = checker.finalize()
        all_errors.extend(checker_errors)
        # Добавляем также те ошибки, которые уже лежали в checker.errors (если они еще не там)
        # На самом деле checker.finalize() в нашем base_checker возвращает self.errors.
        
        # Проверяем общее количество ошибок в чекере (локальные + глобальные)
        if len(checker.errors) > 0:
            print("[{0}FAIL{1}] {2}".format(Colors.RED, Colors.RESET, checker_name))
        else:
            print("[{0}OK{1}]   {2}".format(Colors.GREEN, Colors.RESET, checker_name))
            
    # base_checker.finalize() возвращает ВСЕ накопленные ошибки
    return all_errors
