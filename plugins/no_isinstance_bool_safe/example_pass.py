# Хорошая практика: точная проверка типа
if type(val) is int:
    process_int(val)

if type(val) is float:
    process_float(val)

# isinstance для других типов разрешен
if isinstance(obj, User):
    pass
