from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User, Account, Payment


class IAdminOparations(ABC):
    
    @abstractmethod
    async def create_user(self, db: AsyncSession, full_name, email, password: str) -> User:
        pass
    
    @abstractmethod
    async def patch_user(self, db: AsyncSession, user_id: int, full_name=None, hashed_password=None) -> User:
        pass
    
    @abstractmethod
    async def delete_user(self, db: AsyncSession, user_id: int) -> bool:
        pass
    
    @abstractmethod
    async def get_all_users_accounts(self, db: AsyncSession) -> list[User]:
        pass