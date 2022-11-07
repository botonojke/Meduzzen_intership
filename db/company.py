import sqlalchemy
import datetime
from db.base import metadata, Base

# class Companies(Base):
#     __tablename__ = 'companies'
#
#     id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
#     user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False)
#     title = sqlalchemy.Column(sqlalchemy.String)
#     description = sqlalchemy.Column(sqlalchemy.String)
#     is_active = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
#     create_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.utcnow)
#     update_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.utcnow)
#
#
# companies = Companies.__tablename__

companies = sqlalchemy.Table(
    'companies',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column('user_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False),
    sqlalchemy.Column('title', sqlalchemy.String),
    sqlalchemy.Column('description', sqlalchemy.String),
    sqlalchemy.Column('is_active', sqlalchemy.Boolean, default=True),
    sqlalchemy.Column('create_date', sqlalchemy.DateTime, default=datetime.datetime.utcnow),
    sqlalchemy.Column('update_date', sqlalchemy.DateTime, default=datetime.datetime.utcnow),
)

company_users = sqlalchemy.Table(
    'company_users',
    metadata,
    sqlalchemy.Column('user_id', sqlalchemy.ForeignKey('users.id'), nullable=False),
    sqlalchemy.Column('company_id', sqlalchemy.ForeignKey('companies.id'), nullable=False),
    sqlalchemy.Column('invite', sqlalchemy.Boolean, default=None, nullable=True),
    sqlalchemy.Column('is_admin', sqlalchemy.Boolean, default=False),
    sqlalchemy.Column('decision', sqlalchemy.Boolean, default=None, nullable=True),
    sqlalchemy.Column('request', sqlalchemy.Boolean, default=None, nullable=True),
)
