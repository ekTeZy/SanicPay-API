from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Account, Payment


class AccountOperations(ABC):
    
    @abstractmethod
    async def get_accounts_data(self, db: AsyncSession, user_id: str) -> list[Account]:
        pass
    
    @abstractmethod
    async def get_payments_list(self, db: AsyncSession, user_id: int) -> list[Payment]:
        pass