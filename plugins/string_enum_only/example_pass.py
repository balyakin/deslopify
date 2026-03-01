from enum import Enum

class UserStatus(str, Enum):
    """Правильный строковый Enum"""
    ACTIVE = "active"
    DELETED = "deleted"

class EventType(str, Enum):
    """Еще один пример"""
    CREATE = "create"
