# Плохо: isinstance(a, int) возвращает True для True/False
if isinstance(val, int):
    pass

if isinstance(val, float):
    pass

if isinstance(val, (int, float)):
    pass
