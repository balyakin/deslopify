from sqlalchemy import PrimaryKeyConstraint, Index, UniqueConstraint

# Именованные констрейнты
PrimaryKeyConstraint('id', name='pk_user')
Index('ix_user_email', 'email')
UniqueConstraint('email', name='uq_user_email')
