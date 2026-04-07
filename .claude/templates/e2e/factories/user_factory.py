"""Example user data factories for E2E tests.

Replace or extend these with your application's actual user fields.
"""

import factory
from tests.e2e.factories.base import DictFactory


class UserDataFactory(DictFactory):
    """Produces user registration/creation payloads."""

    name = factory.Faker("name")
    email = factory.Faker("email")
    role = "member"


class AdminUserDataFactory(UserDataFactory):
    """Produces admin user payloads."""

    role = "admin"
