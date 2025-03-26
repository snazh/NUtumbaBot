from typing import Optional
from asyncpg import Pool
from loguru import logger

from src.schemas.evaluation import EvalCreate



class EvalRepository:
    def __init__(self, db_pool: Pool):
        """Initialize UserService with a database connection pool."""
        self.db_pool = db_pool

    async def insert(self, eval: EvalCreate) -> bool:
        """Insert a new user"""
        async with self.db_pool.acquire() as conn:
            try:
                print(eval)
                await conn.execute(
                    "INSERT INTO evaluation (anketa_id, lover_id, evaluation)"
                    "VALUES ($1, $2, $3)",
                    eval.anketa_id, eval.lover_id, eval.evaluation
                )
                return True
            except Exception as e:
                print(str(e))
                logger.error(f"❌ Failed to insert evaluation", str(e))
                return False
