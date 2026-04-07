"""Example page object demonstrating how to extend BasePage.

Replace this with page objects for your actual application pages.
"""

from __future__ import annotations

from playwright.sync_api import Locator
from tests.e2e.page_objects.base_page import BasePage


class ExamplePage(BasePage):
    """Page object for a hypothetical items listing page.

    Demonstrates the pattern:
    1. Set PATH for navigation
    2. Define property selectors for key elements
    3. Add action methods for user interactions
    4. Add composite actions for multi-step workflows
    """

    PATH = "/items"

    # ---- Selectors (properties) ----

    @property
    def page_heading(self) -> Locator:
        return self.get_heading("Items")

    @property
    def create_button(self) -> Locator:
        return self.get_button("Create item")

    @property
    def name_input(self) -> Locator:
        return self.get_input("Name")

    @property
    def description_input(self) -> Locator:
        return self.get_input("Description")

    @property
    def submit_button(self) -> Locator:
        return self.get_button("Save")

    @property
    def error_message(self) -> Locator:
        return self.get_by_testid("error-message")

    # ---- Actions ----

    def open_create_form(self) -> None:
        """Click the create button to open the item form."""
        self.create_button.click()

    def fill_item_form(self, name: str, description: str = "") -> None:
        """Fill out the item creation form."""
        self.fill_field("Name", name)
        if description:
            self.fill_field("Description", description)

    def submit_form(self) -> None:
        """Submit the current form."""
        self.submit_button.click()

    # ---- Composite actions ----

    def create_item(self, name: str, description: str = "") -> None:
        """Full flow: open form, fill, submit."""
        self.open_create_form()
        self.fill_item_form(name, description)
        self.submit_form()
