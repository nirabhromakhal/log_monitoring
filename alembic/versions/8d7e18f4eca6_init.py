"""init

Revision ID: 8d7e18f4eca6
Revises: 
Create Date: 2023-11-17 11:07:57.686736

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8d7e18f4eca6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('logs',
    sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('level', sa.String(), nullable=False),
    sa.Column('message', sa.String(), nullable=False),
    sa.Column('resourceId', sa.String(), nullable=False),
    sa.Column('timestamp', sa.String(), nullable=False),
    sa.Column('traceId', sa.String(), nullable=False),
    sa.Column('spanId', sa.String(), nullable=False),
    sa.Column('commit', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.execute('ALTER TABLE logs ADD COLUMN message_vector tsvector GENERATED ALWAYS AS (to_tsvector(\'english\', message)) STORED;')
    op.create_index(op.f('ix_logs_commit'), 'logs', ['commit'], unique=False, postgresql_using='hash')
    op.create_index(op.f('ix_logs_level'), 'logs', ['level'], unique=False, postgresql_using='hash')
    op.create_index(op.f('ix_logs_message'), 'logs', ['message'], unique=False)
    op.create_index(op.f('ix_logs_message_vector'), 'logs', ['message_vector'], unique=False, postgresql_using='gin')
    op.create_index(op.f('ix_logs_resourceId'), 'logs', ['resourceId'], unique=False, postgresql_using='hash')
    op.create_index(op.f('ix_logs_spanId'), 'logs', ['spanId'], unique=False, postgresql_using='hash')
    op.create_index(op.f('ix_logs_timestamp'), 'logs', ['timestamp'], unique=False, postgresql_using='btree')
    op.create_index(op.f('ix_logs_traceId'), 'logs', ['traceId'], unique=False, postgresql_using='hash')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_logs_traceId'), table_name='logs')
    op.drop_index(op.f('ix_logs_timestamp'), table_name='logs')
    op.drop_index(op.f('ix_logs_spanId'), table_name='logs')
    op.drop_index(op.f('ix_logs_resourceId'), table_name='logs')
    op.drop_index(op.f('ix_logs_message_vector'), table_name='logs')
    op.drop_index(op.f('ix_logs_message'), table_name='logs')
    op.drop_index(op.f('ix_logs_level'), table_name='logs')
    op.drop_index(op.f('ix_logs_commit'), table_name='logs')
    op.drop_table('logs')
    # ### end Alembic commands ###
