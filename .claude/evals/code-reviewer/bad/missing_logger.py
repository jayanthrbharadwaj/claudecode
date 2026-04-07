# Eval sample: BAD — service module missing module-level logger.
# Expected reviewer verdict: REQUEST_CHANGES
# Expected finding: MAJOR — missing logger = logging.getLogger(__name__)
#
# Violations:
# - No module-level logger (uses print instead)
# - Raw print() for logging

from src.types.user import UserId, UserCreate, User
from src.repo.user_repo import UserRepo


class UserService:
    def __init__(self, repo: UserRepo) -> None:
        self._repo = repo

    def create_user(self, data: UserCreate) -> User:
        print(f"Creating user: {data.email}")
        existing = self._repo.find_by_email(data.email)
        if existing is not None:
            print(f"Duplicate email: {data.email}")
            raise ValueError(f"Duplicate: {data.email}")
        user = self._repo.save(data)
        print(f"User created: {user.id}")
        return user
