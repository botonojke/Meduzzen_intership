"""Update company_users

Revision ID: fccef99e23d3
Revises: fe454808510e
Create Date: 2022-11-04 18:12:48.256737

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fccef99e23d3'
down_revision = 'fe454808510e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('company_users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('invite', sa.Boolean(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('decision', sa.Boolean(), nullable=True),
    sa.Column('request', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    op.drop_table('invites')
    op.create_unique_constraint(None, 'companies', ['id'])
    op.create_unique_constraint(None, 'users', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_constraint(None, 'companies', type_='unique')
    op.create_table('invites',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('company_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('invite', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('decision', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], name='invites_company_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='invites_user_id_fkey')
    )
    op.drop_table('company_users')
    # ### end Alembic commands ###
