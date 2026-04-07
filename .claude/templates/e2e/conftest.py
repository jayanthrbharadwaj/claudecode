"""Shared fixtures for E2E tests.

These fixtures provide the core test infrastructure:
- ``base_url``: Target server URL (from BASE_URL env var)
- ``browser``: Session-scoped Chromium browser instance
- ``browser_context``: Per-test browser context (isolated cookies/storage)
- ``page``: Per-test Playwright page
- ``api_client``: Per-test httpx client for API contract tests
- ``test_data``: Override point for feature-specific test data

Requires a running application server. Set BASE_URL to point at it:
    BASE_URL=http://localhost:8000 pytest tests/e2e/ -m e2e
"""

from __future__ import annotations

import os
from collections.abc import Generator
from typing import Any

import httpx
import pytest
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright


@pytest.fixture(scope="session")
def base_url() -> str:
    """Target server URL. Defaults to http://localhost:8000."""
    return os.environ.get("BASE_URL", "http://localhost:8000")


@pytest.fixture(scope="session")
def browser() -> Generator[Browser, None, None]:
    """Session-scoped Chromium browser instance."""
    pw = sync_playwright().start()
    chromium = pw.chromium.launch(headless=True)
    yield chromium
    chromium.close()
    pw.stop()


@pytest.fixture
def browser_context(browser: Browser, base_url: str) -> Generator[BrowserContext, None, None]:
    """Per-test browser context with base_url set.

    Each test gets an isolated context (separate cookies, localStorage, etc.).
    """
    context = browser.new_context(base_url=base_url)
    yield context
    context.close()


@pytest.fixture
def page(browser_context: BrowserContext) -> Generator[Page, None, None]:
    """Per-test Playwright page within the isolated context."""
    new_page = browser_context.new_page()
    yield new_page
    new_page.close()


@pytest.fixture
def api_client(base_url: str) -> Generator[httpx.Client, None, None]:
    """Per-test httpx client for API contract tests."""
    with httpx.Client(base_url=base_url, timeout=30.0) as client:
        yield client


@pytest.fixture
def test_data() -> dict[str, Any]:
    """Override in feature-specific conftest to provide test data.

    Example::

        @pytest.fixture
        def test_data():
            return {"admin_user": AdminUserDataFactory()}
    """
    return {}
