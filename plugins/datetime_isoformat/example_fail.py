# Плохая практика: str(dt)
date_str = str(created_at)
time_str = str(dt)

# strftime
formatted = updated_at.strftime("%Y-%m-%d")

# f-string
log_msg = f"Started at {start_time}"
