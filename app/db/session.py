import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

engine = create_async_engine(settings.DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def setup_db(app):
    try:
        app.ctx.session_factory = AsyncSessionLocal
        async with engine.begin() as conn:
            await conn.run_sync(lambda conn: logger.info("Successful conn!"))
    except Exception as e:
        logger.error(f"Get error while conn: {e}")
