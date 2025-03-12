import asyncio
from src.database.postgres import init_postgres, get_postgres, close_postgres
from loguru import logger


async def test_connection():
    try:
        await init_postgres()  # Initialize the connection pool
        pool = await get_postgres()  # Get the pool

        async with pool.acquire() as conn:
            result = await conn.fetch("SELECT 1")
            logger.info(f"✅ Successfully connected! Result: {result}")

    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")

    finally:
        await close_postgres()  # Close the connection pool


# Run the test
asyncio.run(test_connection())
