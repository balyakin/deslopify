from sqlalchemy import DateTime

# Ошибки: отсутствие timezone или timezone=False
created_at = Column(DateTime())
updated_at = Column(DateTime(timezone=False))
last_login = Column(sa.DateTime())
