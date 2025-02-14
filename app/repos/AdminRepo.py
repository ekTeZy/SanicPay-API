from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from app.db.models import User, Account, Payment
from app.repos.interfaces.AdminOperations import IAdminOparations
from app.utils.password_utils import hash_password
from app.utils.token_utils import generate_api_token
from sanic.exceptions import NotFound

class AdminRepo(IAdminOparations):
    @staticmethod
    async def create_user(db: AsyncSession, full_name, email, password: str) -> User:
        query_result = await db.execute(select(User).where(User.email == email))
        existing_user = query_result.scalar_one_or_none()
        if existing_user:
            raise Exception("User with this data is already exists")
            
        hashed_password = hash_password(password)
        api_token = generate_api_token()

        new_user = User(
            email=email, 
            full_name=full_name, 
            hashed_password=hashed_password, 
            api_token=api_token
        )
        db.add(new_user)
        
        await db.commit()
        await db.refresh(new_user)

        return new_user    
            
    @staticmethod
    async def patch_user(db: AsyncSession, user_id: int, full_name=None, new_password=None) -> User:
        query_result = await db.execute(select(User).where(User.id == user_id))
        existing_user = query_result.scalar_one_or_none()

        if not existing_user:
            raise NotFound(f"User with id == {user_id} not found")

        existing_user.hashed_password = hash_password(new_password)
        existing_user.full_name = full_name
        
        await db.commit()
        await db.refresh(existing_user)
        
        return existing_user
    
    @staticmethod
    async def delete_user(db: AsyncSession, user_id: int) -> bool:
        query_result = await db.execute(select(User).where(User.id == user_id))
        existing_user = query_result.scalar_one_or_none()

        if not existing_user:
            raise NotFound(f"User with id == {user_id} not found")

        await db.delete(existing_user)
        await db.flush() 
        await db.commit()

        return True
    
    @staticmethod
    async def get_all_users_accounts(db: AsyncSession) -> list[User]:
        query_users_result = await db.execute(
            select(User)
            .options(joinedload(User.accounts))
        )
        
        users_data = query_users_result.unique().scalars().all()
        
        return users_data


