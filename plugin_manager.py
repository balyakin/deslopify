import os
import sys
import importlib
import inspect
from core.base_checker import BaseChecker


def get_plugin_directory():
    """Определяет директорию с плагинами относительно текущего файла

    Returns:
        Абсолютный путь к директории plugins
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    plugin_dir = os.path.join(current_dir, 'plugins')
    return plugin_dir


def load_plugins():
    """Динамически загружает все чекеры из директории плагинов

    Returns:
        Список экземпляров загруженных чекеров
    """
    plugin_dir = get_plugin_directory()
    checkers = []
    
    plugin_dir_exists = os.path.exists(plugin_dir) and os.path.isdir(plugin_dir)
    if not plugin_dir_exists:
        return checkers

    sys.path.insert(0, os.path.dirname(plugin_dir))

    for item_name in os.listdir(plugin_dir):
        item_path = os.path.join(plugin_dir, item_name)
        
        is_directory = os.path.isdir(item_path)
        is_not_dunder = not item_name.startswith('__')
        
        if is_directory and is_not_dunder:
            module_name = 'plugins.{0}.checker'.format(item_name)
            
            try:
                module = importlib.import_module(module_name)
                
                for attribute_name, attribute_value in inspect.getmembers(module):
                    is_class = inspect.isclass(attribute_value)
                    
                    if is_class:
                        is_checker = issubclass(attribute_value, BaseChecker)
                        is_not_base = attribute_value is not BaseChecker
                        
                        if is_checker and is_not_base:
                            checker_instance = attribute_value()
                            checkers.append(checker_instance)
            except ImportError:
                pass

    sys.path.pop(0)
    return checkers
