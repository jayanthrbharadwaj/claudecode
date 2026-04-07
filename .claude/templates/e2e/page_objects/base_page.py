"""Base page object for Playwright E2E tests.

All page objects should inherit from BasePage and override PATH.
Uses Playwright's recommended locator strategies: roles, labels, and test IDs.
"""

from __future__ import annotations

from playwright.sync_api import Locator, Page, expect


class BasePage:
    """Base class for page objects.

    Subclasses set ``PATH`` and add domain-specific selectors/actions.

    Usage::

        class LoginPage(BasePage):
            PATH = "/login"

            @property
            def email_input(self) -> Locator:
                return self.get_input("Email")

            def login(self, email: str, password: str) -> None:
                self.fill_field("Email", email)
                self.fill_field("Password", password)
                self.click_button("Sign in")
    """

    PATH: str = "/"

    def __init__(self, page: Page) -> None:
        self._page = page

    @property
    def page(self) -> Page:
        return self._page

    # ---- Navigation ----

    def navigate(self) -> None:
        """Go to the page's PATH."""
        self._page.goto(self.PATH)

    # ---- Locator helpers (Playwright best-practice strategies) ----

    def get_by_testid(self, testid: str) -> Locator:
        """Locate element by ``data-testid`` attribute."""
        return self._page.get_by_test_id(testid)

    def get_heading(self, name: str) -> Locator:
        """Locate a heading by accessible name."""
        return self._page.get_by_role("heading", name=name)

    def get_button(self, name: str) -> Locator:
        """Locate a button by accessible name."""
        return self._page.get_by_role("button", name=name)

    def get_link(self, name: str) -> Locator:
        """Locate a link by accessible name."""
        return self._page.get_by_role("link", name=name)

    def get_input(self, label: str) -> Locator:
        """Locate an input by its associated label text."""
        return self._page.get_by_label(label)

    # ---- Actions ----

    def fill_field(self, label: str, value: str) -> None:
        """Fill an input identified by label."""
        self.get_input(label).fill(value)

    def click_button(self, name: str) -> None:
        """Click a button identified by accessible name."""
        self.get_button(name).click()

    # ---- Assertions ----

    def expect_visible(self, locator: Locator) -> None:
        """Assert that a locator is visible."""
        expect(locator).to_be_visible()

    def expect_text(self, locator: Locator, text: str) -> None:
        """Assert that a locator contains the given text."""
        expect(locator).to_contain_text(text)

    def expect_url_contains(self, path: str) -> None:
        """Assert the current URL contains ``path``."""
        expect(self._page).to_have_url(f"*{path}*")
