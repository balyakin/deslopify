from abc import abstractmethod

def valid_function():
    return 42

class BaseInterface:
    @abstractmethod
    def abstract_method(self):
        pass
        
    @property
    @abstractmethod
    def abstract_prop(self):
        """Docstring"""
        ...
