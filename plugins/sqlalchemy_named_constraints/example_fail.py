from sqlalchemy import PrimaryKeyConstraint, Index, UniqueConstraint

# Неименованные констрейнты
PrimaryKeyConstraint('id')
Index('email') # Без имени (имя должно быть первым или через name)
UniqueConstraint('email')
