# Eval sample: BAD — tests with vacuous assertions.
# Expected reviewer verdict: REQUEST_CHANGES
# Expected finding: MAJOR — vacuous assertions that don't verify behavior
#
# Violations:
# - assert result is not None (doesn't check the actual value)
# - assert response (truthiness check, not specific)
# - No spec criterion references
# - Missing type annotations on test functions

import pytest
from unittest.mock import MagicMock


def test_create_user_works(mock_repo):
    """Test that create_user works."""
    mock_repo.find_by_email.return_value = None
    mock_repo.save.return_value = MagicMock()

    from src.service.user_service import UserService
    service = UserService(repo=mock_repo)
    result = service.create_user(MagicMock())

    assert result is not None  # VACUOUS: doesn't check what was returned


def test_get_user_returns_something(mock_repo):
    """Test get_user."""
    mock_repo.find_by_id.return_value = MagicMock()

    from src.service.user_service import UserService
    service = UserService(repo=mock_repo)
    result = service.get_user("some-id")

    assert result  # VACUOUS: truthiness check only


def test_service_initializes():
    """Test that the service can be created."""
    from src.service.user_service import UserService
    service = UserService(repo=MagicMock())
    assert service is not None  # VACUOUS: of course it's not None


@pytest.fixture
def mock_repo():
    return MagicMock()
