"""Added: First init

Revision ID: 3a85d4959469
Revises: 
Create Date: 2025-04-06 20:11:47.043808

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3a85d4959469'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_mails_id_receiver_id', 'mails', ['id', 'receiver_id'], unique=False)
    op.create_index('ix_mails_id_sender_id', 'mails', ['id', 'sender_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_mails_id_sender_id', table_name='mails')
    op.drop_index('ix_mails_id_receiver_id', table_name='mails')
    # ### end Alembic commands ###
