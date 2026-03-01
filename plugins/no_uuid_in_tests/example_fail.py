import uuid

def test_random_id():
    """Плохая практика: случайный UUID в тесте"""
    random_id = uuid.uuid4()
    assert random_id is not None

def test_another_random():
    """Еще один плохой пример"""
    user_id = uuid.uuid1().hex
    assert len(user_id) == 32
