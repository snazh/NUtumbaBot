from loguru import logger

from src.repository.schemas.evaluation import EvalCreate
from src.repository.base import BaseRepo


class EvalRepository(BaseRepo):

    async def insert(self, eval_data: EvalCreate) -> bool:
        """Insert evaluation"""
        async with self.db_pool.acquire() as conn:
            try:
                await conn.execute(
                    "INSERT INTO evaluation (anketa_id, lover_id, evaluation)"
                    "VALUES ($1, $2, $3)",
                    eval_data.anketa_id, eval_data.lover_id, eval_data.evaluation
                )
                return True
            except Exception as e:
                logger.error(f"❌ Failed to insert evaluation(gay)", str(e))
                return False

    async def delete_evaluation(self, user1_id: int, user2_id: int):
        async with self.db_pool.acquire() as conn:
            try:
                query = f"""
                                DELETE FROM {self.table}
                                WHERE (anketa_id = $1 AND lover_id = $2)
                                   OR (anketa_id = $2 AND lover_id = $1)
                            """

                await conn.execute(query, user1_id, user2_id)
                return True
            except Exception as e:
                logger.error(f"❌ Failed to delete evaluation: {str(e)}")
                return False
