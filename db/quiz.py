import sqlalchemy
import datetime
from db.base import metadata


quizzes = sqlalchemy.Table(
    'quizzes',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column('company_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('companies.id'), nullable=False),
    sqlalchemy.Column('title', sqlalchemy.String),
    sqlalchemy.Column('description', sqlalchemy.String),
    sqlalchemy.Column('duration', sqlalchemy.Integer),
    sqlalchemy.Column('questions', sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column('create_date', sqlalchemy.DateTime, default=datetime.datetime.utcnow),
    sqlalchemy.Column('update_date', sqlalchemy.DateTime, default=datetime.datetime.utcnow),
)


questions = sqlalchemy.Table(
    'questions',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column('quiz_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('quizzes.id'), nullable=False),
    sqlalchemy.Column('question', sqlalchemy.String,  nullable=False),
    sqlalchemy.Column('option_1', sqlalchemy.String,  nullable=False),
    sqlalchemy.Column('option_2', sqlalchemy.String,  nullable=False),
    sqlalchemy.Column('option_3', sqlalchemy.String,  nullable=False),
    sqlalchemy.Column('option_4', sqlalchemy.String,  nullable=False),
    sqlalchemy.Column('answer', sqlalchemy.String,  nullable=False),
)


answers = sqlalchemy.Table(
    'answers',
    metadata,
    sqlalchemy.Column('user_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False),
    sqlalchemy.Column('quiz_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('quizzes.id'), nullable=False),
    sqlalchemy.Column('company_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('companies.id'), nullable=False),
    sqlalchemy.Column('create_date', sqlalchemy.DateTime, default=datetime.datetime.utcnow),
    sqlalchemy.Column('average_quiz_mark', sqlalchemy.Float,  nullable=False),
    sqlalchemy.Column('right_answers', sqlalchemy.Integer,  nullable=False),
    sqlalchemy.Column('total_answers', sqlalchemy.Integer,  nullable=False),
)


quiz_rate = sqlalchemy.Table(
    'quiz_rate',
    metadata,
    sqlalchemy.Column('user_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False, unique=True),
    sqlalchemy.Column('quiz_rate', sqlalchemy.Float, nullable=False),
    sqlalchemy.Column('total_answers', sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column('right_answers', sqlalchemy.Integer, nullable=False),
)
