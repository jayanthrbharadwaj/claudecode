"""Example UI E2E tests using Playwright page objects.

These tests demonstrate the pattern for writing UI E2E tests.
They require a running application server at BASE_URL.

Run:
    BASE_URL=http://localhost:8000 pytest tests/e2e/test_example_ui.py -m e2e
"""

from __future__ import annotations

import pytest
from playwright.sync_api import Page
from tests.e2e.page_objects.example_page import ExamplePage


@pytest.mark.e2e
class TestExamplePageNavigation:
    """Tests for basic page navigation and element presence."""

    def test_page_loads_successfully(self, page: Page) -> None:
        """Page should load and display the heading."""
        example = ExamplePage(page)
        example.navigate()
        example.expect_visible(example.page_heading)

    def test_heading_text(self, page: Page) -> None:
        """Heading should contain the expected text."""
        example = ExamplePage(page)
        example.navigate()
        example.expect_text(example.page_heading, "Items")

    def test_create_button_present(self, page: Page) -> None:
        """Create button should be visible on the page."""
        example = ExamplePage(page)
        example.navigate()
        example.expect_visible(example.create_button)


@pytest.mark.e2e
class TestExampleItemCreation:
    """Tests for item creation workflow."""

    def test_create_item_flow(self, page: Page) -> None:
        """Creating an item should navigate to the items list."""
        example = ExamplePage(page)
        example.navigate()
        example.create_item(name="Test Item", description="A test item")
        example.expect_url_contains("/items")

    def test_validation_error_on_empty_name(self, page: Page) -> None:
        """Submitting an empty name should show a validation error."""
        example = ExamplePage(page)
        example.navigate()
        example.open_create_form()
        example.submit_form()
        example.expect_visible(example.error_message)
