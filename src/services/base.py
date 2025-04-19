from src.repository.base import BaseRepo


class BaseService:
    def __init__(self, repo):
        self.repo = repo
