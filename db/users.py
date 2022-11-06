import sqlalchemy
import datetime
from db.base import metadata, Base


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

# class Users(Base):
#     __tablename__ = 'users'
#
#     id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True)
#     email = sqlalchemy.Column(sqlalchemy.Integer, unique=True, nullable=False)
#     name = sqlalchemy.Column(sqlalchemy.String)
#     hashed_password = sqlalchemy.Column(sqlalchemy.String)
#     is_active = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
#     is_admin = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
#     create_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.utcnow)
#     update_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.utcnow)
#
#
# users = Users.__tablename__
# print(type(users))



