from dateutil.parser import isoparse

# Хорошая практика
dt = isoparse("2023-01-01T12:00:00Z")
other_dt = isoparse(some_date_str)
