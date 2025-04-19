from typing import List

from asyncpg import Pool
from loguru import logger


class BaseRepo:
    def __init__(self, db_pool: Pool, table: str, columns: List[str]):
        self.db_pool = db_pool
        self.table = table
        self.columns = columns

    async def _verify_column(self, column: str) -> None:

        if column not in self.columns:
            raise Exception(f"⚠️ Attempt to update invalid column: {column}")

    # async def getUserById(self, id: int):
    #     pass
    async def delete(self, column: str, value: any) -> bool:
        async with self.db_pool.acquire() as conn:
            try:

                await self._verify_column(column)
                await conn.execute(
                    f"DELETE FROM {self.table} WHERE {column} = $1", value
                )

                return True
            except Exception as e:
                logger.error(f"❌ Failed to delete from {self.table}: {e}")
                return False
