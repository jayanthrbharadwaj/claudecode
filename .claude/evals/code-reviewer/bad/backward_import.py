# Eval sample: BAD — types module importing from service layer.
# Expected reviewer verdict: REQUEST_CHANGES
# Expected finding: CRITICAL — backward layer import (Types importing from Service)
#
# Violations:
# - Types layer (layer 0) imports from Service layer (layer 3)
# - This is a backward dependency that breaks the layer model

import logging
from pydantic import BaseModel

from src.service.user_service import UserService  # VIOLATION: backward import

logger = logging.getLogger(__name__)


class UserSummary(BaseModel):
    """A user summary that incorrectly depends on the service layer."""
    id: str
    name: str

    @classmethod
    def from_service(cls, svc: UserService, user_id: str) -> "UserSummary":
        user = svc.get_user(user_id)
        return cls(id=str(user.id), name=user.name)
