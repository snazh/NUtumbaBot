from src.repository.schemas.relationship import RelationshipCreate
from src.dependencies.repo_di import get_relationship_repo
from src.services.base import BaseService


class RelationshipService(BaseService):

    @classmethod
    async def create(cls):
        repo = await get_relationship_repo()
        return cls(repo)

    async def create_relationship(self, relationship_data: dict):
        new_relationship = RelationshipCreate(
            user1=relationship_data["user1"],
            user2=relationship_data["user2"],
            status=relationship_data["status"],
        )
        return await self.repo.insert(new_relationship)
