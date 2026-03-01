import uuid

# Хорошая практика: захардкоженные константы в тестах
USER_ID = "550e8400-e29b-41d4-a716-446655440000"

def test_user_creation():
    """Тест создания пользователя"""
    user = {"id": USER_ID, "name": "John"}
    assert user["id"] == USER_ID
