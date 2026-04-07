"""Base factory for E2E tests.

E2E factories produce plain dicts suitable for API request payloads.
They do NOT touch the database — data is created through the app's public API.
"""

import factory


class DictFactory(factory.Factory):
    """Factory that builds plain dictionaries instead of ORM models.

    Usage::

        class MyDataFactory(DictFactory):
            name = factory.Faker("name")
            email = factory.Faker("email")

        payload = MyDataFactory()  # -> {"name": "...", "email": "..."}
    """

    class Meta:
        model = dict
