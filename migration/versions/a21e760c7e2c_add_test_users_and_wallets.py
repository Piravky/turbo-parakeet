"""add_test_users_and_wallets

Revision ID: a21e760c7e2c
Revises: 0ea075cb1f90
Create Date: 2025-10-31 07:10:57.574946

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'a21e760c7e2c'
down_revision: Union[str, Sequence[str], None] = '0ea075cb1f90'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
               INSERT INTO users (id, email, password)
               VALUES ('9c3baaec-e00e-49c8-9195-d0c0ef4078c4', 'user1@example.com', 'hashed_password_1'),
                      ('b6e162ee-960b-40a2-836b-c2817b344bbf', 'user2@example.com', 'hashed_password_2'),
                      ('b9ce70f3-7c6e-4ab0-9fc9-ddfdc669890c', 'user3@example.com', 'hashed_password_3')
               """)

    # Вставляем тестовые кошельки
    op.execute("""
               INSERT INTO wallets (id, balance, user_id)
               VALUES ('d70d0d78-f789-48b4-9ba0-d939cbf9d9f8', 1000.50, '9c3baaec-e00e-49c8-9195-d0c0ef4078c4'),
                      ('f726345e-abef-4e79-8788-d19a92825700', 250.75, '9c3baaec-e00e-49c8-9195-d0c0ef4078c4'),
                      ('d3576d28-3179-4821-bd5f-8899c722f876', 5000.00, 'b6e162ee-960b-40a2-836b-c2817b344bbf'),
                      ('418694b1-fec9-436e-b975-951830e13b59', 100.00, 'b9ce70f3-7c6e-4ab0-9fc9-ddfdc669890c')
               """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DELETE FROM wallets")
    op.execute("DELETE FROM users")
