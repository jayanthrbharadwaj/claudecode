# Eval sample: GOOD — tests with meaningful assertions.
# Expected reviewer verdict: APPROVE
#
# Conventions demonstrated:
# - Specific value assertions (not vacuous)
# - Test naming convention: test_<function>_<scenario>_<outcome>
# - Fixtures from conftest (not duplicated)
# - Spec criterion reference in docstring
# - Type annotations on test functions

import pytest
from unittest.mock import MagicMock

from src.types.user import UserId, UserCreate, User
from src.service.user_service import UserService, DuplicateEmailError


@pytest.fixture
def mock_repo() -> MagicMock:
    return MagicMock()


@pytest.fixture
def service(mock_repo: MagicMock) -> UserService:
    return UserService(repo=mock_repo)


@pytest.mark.unit
def test_create_user_valid_input_returns_user(
    service: UserService, mock_repo: MagicMock
) -> None:
    """Given valid input, create_user returns the saved user.
    # Spec: specs/features/user-management.md AC-1
    """
    mock_repo.find_by_email.return_value = None
    expected = User(id=UserId("u-123"), email="alice@example.com", name="Alice")
    mock_repo.save.return_value = expected

    result = service.create_user(
        UserCreate(email="alice@example.com", name="Alice")
    )

    assert result.id == UserId("u-123")
    assert result.email == "alice@example.com"
    assert result.name == "Alice"
    mock_repo.save.assert_called_once()


@pytest.mark.unit
def test_create_user_duplicate_email_raises_conflict(
    service: UserService, mock_repo: MagicMock
) -> None:
    """Given a duplicate email, create_user raises DuplicateEmailError.
    # Spec: specs/features/user-management.md AC-2
    """
    mock_repo.find_by_email.return_value = User(
        id=UserId("u-existing"), email="alice@example.com", name="Alice"
    )

    with pytest.raises(DuplicateEmailError) as exc_info:
        service.create_user(
            UserCreate(email="alice@example.com", name="Alice Again")
        )

    assert "alice@example.com" in str(exc_info.value)


@pytest.mark.unit
def test_get_user_existing_returns_user(
    service: UserService, mock_repo: MagicMock
) -> None:
    """Given an existing user ID, get_user returns the user.
    # Spec: specs/features/user-management.md AC-3
    """
    expected = User(id=UserId("u-123"), email="alice@example.com", name="Alice")
    mock_repo.find_by_id.return_value = expected

    result = service.get_user(UserId("u-123"))

    assert result is not None
    assert result.id == UserId("u-123")
    assert result.email == "alice@example.com"


@pytest.mark.unit
def test_get_user_missing_returns_none(
    service: UserService, mock_repo: MagicMock
) -> None:
    """Given a nonexistent user ID, get_user returns None.
    # Spec: specs/features/user-management.md AC-4
    """
    mock_repo.find_by_id.return_value = None

    result = service.get_user(UserId("u-nonexistent"))

    assert result is None
