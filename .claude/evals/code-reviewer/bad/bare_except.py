# Eval sample: BAD — bare except and missing context in error handling.
# Expected reviewer verdict: REQUEST_CHANGES
# Expected finding: MAJOR — bare except, no context logged before re-raise
#
# Violations:
# - Bare except: (catches everything including KeyboardInterrupt)
# - No context logged before re-raising
# - Generic ValueError instead of domain-specific exception
# - Swallows original exception (no `from e`)

import logging

from src.types.user import UserCreate, User
from src.repo.user_repo import UserRepo

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, repo: UserRepo) -> None:
        self._repo = repo

    def create_user(self, data: UserCreate) -> User:
        try:
            return self._repo.save(data)
        except:
            raise ValueError("Something went wrong")
