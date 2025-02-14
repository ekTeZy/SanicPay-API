from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User
from app.repos.interfaces.CommonUser import ICommonUserOparations
from app.utils.password_utils import verify_password
from app.utils.token_utils import generate_api_token


class UserRepo(ICommonUserOparations):
    @staticmethod
    async def authenticate_user(db: AsyncSession, email: str, password: str) -> User:
        query_result = await db.execute(select(User).where(User.email == email))
        user = query_result.scalars().first()
        if user and verify_password(plain_password=password, hashed_password=user.hashed_password):
            if not user.api_token:
                user.api_token = generate_api_token()
                await db.commit()     
                await db.refresh(user)
            
            return user
        
        return None
    
    @staticmethod
    async def get_user(db: AsyncSession, user_id: int) -> User:
        query_result = await db.execute(select(User).where(User.id == user_id))
        user = query_result.scalar_one_or_none()

        return user

    @staticmethod
    async def get_user_by_token(db: AsyncSession, api_token: str) -> User:
        query_result = await db.execute(select(User).where(User.api_token == api_token))
        user = query_result.scalar_one_or_none()

        if not user:
            raise Exception("Invalid API token")

        return user