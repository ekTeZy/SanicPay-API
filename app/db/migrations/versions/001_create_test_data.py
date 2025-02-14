"""Create test users and accounts

Revision ID: 001_create_test_data
Revises: be98811d50c6
Create Date: 2025-02-14 21:00:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from app.db.models import User, Account
from app.utils.password_utils import hash_password
from app.utils.token_utils import generate_api_token

# revision identifiers, used by Alembic
revision = '001_create_test_data'
down_revision = 'be98811d50c6'
branch_labels = None
depends_on = None

Session = sessionmaker()

def upgrade():
    bind = op.get_bind()
    session = Session(bind=bind)
    
    existing_admin = session.query(User).filter_by(email="admin@example.com").first()
    existing_user = session.query(User).filter_by(email="testuser@example.com").first()

    if not existing_admin:
        admin = User(
            email="admin@example.com",
            full_name="Admin User",
            hashed_password=hash_password("adminpassword"),
            api_token=generate_api_token(),
            is_admin=True,
        )
        session.add(admin)

    if not existing_user:
        test_user = User(
            email="testuser@example.com",
            full_name="Test User",
            hashed_password=hash_password("testpassword"),
            api_token=generate_api_token(),
            is_admin=False,
        )
        session.add(test_user)
        session.flush()  

        account = Account(user_id=test_user.id, balance=100.0)
        session.add(account)

    session.commit()

def downgrade():
    bind = op.get_bind()
    session = Session(bind=bind)
    session.query(Account).delete()
    session.query(User).filter(User.email.in_(["admin@example.com", "testuser@example.com"])).delete()
    session.commit()
