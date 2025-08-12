import pytest
from playwright.sync_api import Playwright, Page


@pytest.fixture
def chromium_page(playwright: Playwright) -> Page:
    with playwright.chromium.launch(headless=False) as browser:
        yield browser.new_page()
