from datetime import datetime

# Плохо: strptime
dt = datetime.strptime("2023-01-01", "%Y-%m-%d")

# Плохо: fromisoformat
other_dt = datetime.fromisoformat("2023-01-01")
date_obj = date.fromisoformat("2023-01-01")
