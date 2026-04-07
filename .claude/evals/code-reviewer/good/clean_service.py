# Eval sample: GOOD — clean service module following all conventions.
# Expected reviewer verdict: APPROVE
#
# Conventions demonstrated:
# - Module-level logger
# - Refined Pydantic types (not raw str/int)
# - Structured logging with context
# - Specific exception handling
# - Type annotations on all functions
# - Under 50 lines per function, under 300 lines per file

import logging
from typing import Optional

from src.types.user import UserId, UserCreate, User
from src.repo.user_repo import UserRepo

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, repo: UserRepo) -> None:
        self._repo = repo

    def create_user(self, data: UserCreate) -> User:
        """Create a new user from validated input."""
        logger.info("Creating user: email=%s", data.email)
        existing = self._repo.find_by_email(data.email)
        if existing is not None:
            logger.warning("Duplicate email: email=%s", data.email)
            raise DuplicateEmailError(data.email)
        user = self._repo.save(data)
        logger.info("User created: user_id=%s", user.id)
        return user

    def get_user(self, user_id: UserId) -> Optional[User]:
        """Retrieve a user by ID."""
        logger.debug("Fetching user: user_id=%s", user_id)
        return self._repo.find_by_id(user_id)


class DuplicateEmailError(Exception):
    def __init__(self, email: str) -> None:
        super().__init__(f"User with email {email} already exists")
        self.email = email
