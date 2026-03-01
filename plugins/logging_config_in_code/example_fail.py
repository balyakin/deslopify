import logging
import logging.config

def setup():
    """Настройка логирования (плохой тон для модуля)"""
    logging.basicConfig(level=logging.INFO)
    
    config = {'version': 1}
    logging.config.dictConfig(config)
