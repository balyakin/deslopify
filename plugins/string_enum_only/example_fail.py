from enum import Enum

class BadStatus(Enum):
    """Плохой Enum (без наследования от str)"""
    ACTIVE = 1
    DELETED = 0

class IntBadStatus(IntEnum):
    """Тоже плохой для нашего проекта (предпочитаем строковые)"""
    ON = 1
    OFF = 0
