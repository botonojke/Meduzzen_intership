import sqlalchemy
import datetime
from db.base import metadata


users = sqlalchemy.Table(
    'users',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column('email', sqlalchemy.String, unique=True),
    sqlalchemy.Column('name', sqlalchemy.String),
    sqlalchemy.Column('hashed_password', sqlalchemy.String),
    sqlalchemy.Column('is_active', sqlalchemy.Boolean, default=True),
    sqlalchemy.Column('is_admin', sqlalchemy.Boolean, default=False),
    sqlalchemy.Column('create_date', sqlalchemy.DateTime, default=datetime.datetime.utcnow),
    sqlalchemy.Column('update_date', sqlalchemy.DateTime, default=datetime.datetime.utcnow),
    )



