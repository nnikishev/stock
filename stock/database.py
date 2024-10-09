from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://nikolay:12345@localhost/stock"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL
)

asession = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)

Base = declarative_base()


