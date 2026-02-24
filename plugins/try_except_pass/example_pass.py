try:
    result = 1 / 0
except ZeroDivisionError as e:
    print(e)

try:
    pass
except Exception:
    raise
