from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine
from sqlalchemy.orm import sessionmaker
import os
from sqlmodel import SQLModel
load_dotenv()

DB_CONFIG= os.getenv("DB_CONFIG")

class DatabaseSession:
    def __init__(self, url:str=DB_CONFIG):
        self.engine = create_async_engine(url, echo=True)
        self.SessionLocal = sessionmaker(
            bind= self.engine,
            class_ = AsyncSession,
            expire_on_commit=False,
            future=True

        )
    
    #generating models into the database
    async def create_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
    
    async def drop_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.drop_all)
    
    #close connection
    async def close(self):
        await self.engine.dispose()
    
    #prepares the context for the asynchronous operations
    async def __aenter__(self)->AsyncSession:
        self.session=self.SessionLocal()
        return self.session
    
    #it is used to clean up the resouces
    async def __aexit__(self,exc_type,exc_value,exc_tb):
        await self.session.close()
    

    async def commit_rollback(self):
        try:
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            raise e



db= DatabaseSession()
        