from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User


class ICommonUserOparations(ABC):
    
    @abstractmethod
    async def authenticate_user(self, db: AsyncSession, email, password: str) -> User:
        pass
    
    @abstractmethod
    async def get_user(self, db: AsyncSession, user_id: int) -> User:
        pass