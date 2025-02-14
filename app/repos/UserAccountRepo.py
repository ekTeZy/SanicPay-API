from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Account, Payment, User
from app.repos.interfaces.UserAccountOperations import AccountOperations

class UserAccountRepo(AccountOperations):
    
    @staticmethod
    async def get_accounts_data(db: AsyncSession, user_id: int) -> list[Account]:
        query_result = await db.execute(select(Account).outerjoin(User).where(User.id == user_id))
        
        all_accounts = query_result.scalars().all() 
        
        if not all_accounts:
            raise Exception("Accounts does not exists")
        
        return all_accounts
        
    @staticmethod
    async def get_payments_list(db: AsyncSession, user_id: int) -> list[Payment]:
        query_result = await db.execute(select(Payment).where(Payment.user_id == user_id))
        all_transactions = query_result.scalars().all()
        
        if not all_transactions:
            raise Exception("No transactions found")
        
        return all_transactions