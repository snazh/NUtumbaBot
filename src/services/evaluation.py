from src.dependencies.repo_di import get_eval_repo
from src.repository.evaluation import EvalRepository
from src.schemas.evaluation import EvalCreate



class EvalService:
    def __init__(self, eval_repo: EvalRepository):
        self.eval_repo = eval_repo

    @classmethod
    async def create(cls):
        """Asynchronous constructor to create an instance of UserService"""
        eval_repo = await get_eval_repo()
        return cls(eval_repo)

    async def eval_profile(self, eval_data: dict):
        new_eval = EvalCreate(
            anketa_id=eval_data["anketa_id"],
            lover_id=eval_data["lover_id"],
            evaluation=eval_data["evaluation"],
        )
        return await self.eval_repo.insert(new_eval)




