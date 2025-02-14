import hashlib
from sanic.exceptions import Forbidden, BadRequest
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Account, Payment
from app.core.config import settings

class PaymentRepo:

    async def process_webhook(self, db: AsyncSession, transaction_id: str, user_id: int, account_id: int, amount: float, request_signature: str):
        
        secret_key = settings.SECRET_KEY 

        data_string = f"{account_id}{amount}{transaction_id}{user_id}{secret_key}"
        signature = hashlib.sha256(data_string.encode()).hexdigest()

        if signature != request_signature:
            raise Forbidden("Invalid signature")

        existing_payment = await db.execute(select(Payment).where(Payment.transaction_id == transaction_id))
        if existing_payment.scalars().first():
            raise BadRequest("Transaction already processed")

        account_query = await db.execute(select(Account).where(Account.id == account_id, Account.user_id == user_id))
        account = account_query.scalars().first()

        if not account:
            account = Account(id=account_id, user_id=user_id, balance=0)
            db.add(account)
            await db.commit()
            await db.refresh(account)

        payment = Payment(transaction_id=transaction_id, account_id=account_id, user_id=user_id, amount=amount, signature=signature)
        db.add(payment)

        account.balance += amount
        await db.commit()

        return payment, account