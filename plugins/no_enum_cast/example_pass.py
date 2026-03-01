# Хорошая практика: использование .value
status_val = MyEnum.ACTIVE.value
code = event_type.value

# Обычный каст строки к числу - допустимо
count = int("123")
offset = int(request.get('offset', 0))
