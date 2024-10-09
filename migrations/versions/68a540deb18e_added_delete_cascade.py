"""added delete cascade

Revision ID: 68a540deb18e
Revises: 57b6eb8db831
Create Date: 2024-10-10 00:41:22.790603

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '68a540deb18e'
down_revision = '57b6eb8db831'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('borrowed_books', schema=None) as batch_op:
        batch_op.drop_constraint('borrowed_books_ibfk_2', type_='foreignkey')
        batch_op.drop_constraint('borrowed_books_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'books', ['book_id'], ['id'], ondelete='CASCADE')
        batch_op.create_foreign_key(None, 'users', ['member_id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('member_history', schema=None) as batch_op:
        batch_op.drop_constraint('member_history_ibfk_1', type_='foreignkey')
        batch_op.drop_constraint('member_history_ibfk_2', type_='foreignkey')
        batch_op.create_foreign_key(None, 'users', ['member_id'], ['id'], ondelete='CASCADE')
        batch_op.create_foreign_key(None, 'books', ['book_id'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('member_history', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('member_history_ibfk_2', 'users', ['member_id'], ['id'])
        batch_op.create_foreign_key('member_history_ibfk_1', 'books', ['book_id'], ['id'])

    with op.batch_alter_table('borrowed_books', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('borrowed_books_ibfk_1', 'books', ['book_id'], ['id'])
        batch_op.create_foreign_key('borrowed_books_ibfk_2', 'users', ['member_id'], ['id'])

    # ### end Alembic commands ###
