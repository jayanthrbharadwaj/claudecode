"""E2E test data factories — produce dicts for API request payloads."""

from tests.e2e.factories.base import DictFactory
from tests.e2e.factories.user_factory import AdminUserDataFactory, UserDataFactory

__all__ = ["AdminUserDataFactory", "DictFactory", "UserDataFactory"]
