from sqlalchemy import DateTime

# Правильное использование
created_at = Column(DateTime(timezone=True))
updated_at = Column(DateTime(timezone=True))
