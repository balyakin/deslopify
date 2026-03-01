# Хорошая практика: использование .isoformat()
now_str = now.isoformat()
created_at_str = user.created_at.isoformat()
print("Date: " + dt.isoformat())

# Обычное преобразование строк - разрешено
str_id = str(user_id)
message = f"Hello {name}"
