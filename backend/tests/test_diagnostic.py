import pytest
import pytest_asyncio
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_database_tables_created(db_session: AsyncSession):
    """Test that database tables are created."""
    # Get the engine from the session
    engine = db_session.get_bind()
    
    # Check tables using inspect
    async with engine.connect() as conn:
        def get_tables(sync_conn):
            inspector = inspect(sync_conn)
            return inspector.get_table_names()
        
        tables = await conn.run_sync(get_tables)
        print(f"\nTables in database: {tables}")
        
        assert len(tables) > 0, "No tables were created"
        assert "products" in tables, f"products table not found. Tables: {tables}"
