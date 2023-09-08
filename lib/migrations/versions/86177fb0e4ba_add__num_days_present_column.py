"""Add _num_days_present column

Revision ID: 86177fb0e4ba
Revises: 399ff81943b4
Create Date: 2023-09-09 00:21:31.672280

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '86177fb0e4ba'
down_revision: Union[str, None] = '399ff81943b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('performance_records', sa.Column('_num_days_present', sa.Integer(), nullable=True))
    op.drop_column('performance_records', 'student_name')
    op.drop_column('performance_records', 'attendance')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('performance_records', sa.Column('attendance', sa.FLOAT(), nullable=True))
    op.add_column('performance_records', sa.Column('student_name', sa.VARCHAR(length=255), nullable=True))
    op.drop_column('performance_records', '_num_days_present')
    # ### end Alembic commands ###
