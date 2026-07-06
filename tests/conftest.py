import pytest, pytest_asyncio
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import os

os.environ["DB_HOST"] = "localhost"
os.environ["DB_PORT"] = "5434"          
os.environ["DB_NAME"] = "test_db"       
os.environ["DB_USER"] = "amin"          
os.environ["DB_PASSWORD"] = "its_my_password"  

from app.main import app
from database.postgres import Base

TEST_DATABASE_URL = f"postgresql+asyncpg://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}"




@pytest_asyncio.fixture(scope="function")
async def db_session():
    engine = create_async_engine(TEST_DATABASE_URL, echo=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  
        await conn.run_sync(Base.metadata.create_all) 

    async_session = async_sessionmaker(engine,expire_on_commit=False)
    
    async with async_session() as session:
        yield session
    
    await engine.dispose()




@pytest_asyncio.fixture(scope="session")
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

@pytest_asyncio.fixture(scope="function")
async def test_department(client) -> dict:
    response = await client.post(
        "/departments/",
        json={"name": "Test Department"}
    )
    return response.json()

@pytest_asyncio.fixture(scope="function")
async def test_employee(client, test_department) -> dict:
    response = await client.post(
        f"/departments/{test_department['id']}/employees",
        json={
            "full_name": "Test Employee",
            "position": "Tester"
        }
    )
    return response.json()