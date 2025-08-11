from dataclasses import dataclass

import pytest
from playwright.sync_api import Playwright, Page, Browser, BrowserContext


@dataclass
class URLs:
    registration: str = 'https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/auth/registration'
    courses: str = 'https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/courses'


@dataclass
class Locators:
    test_id: str = 'data-testid'

    email_input: str = f'//*[@{test_id}="registration-form-email-input"]//input'
    username_input: str = f'//*[@{test_id}="registration-form-username-input"]//input'
    password_input: str = f'//*[@{test_id}="registration-form-password-input"]//input'
    registration_button: str = f'//*[@{test_id}="registration-page-registration-button"]'

    courses_toolbar_title: str = f'//*[@{test_id}="courses-list-toolbar-title-text"]'
    courses_empty_view_title: str = f'//*[@{test_id}="courses-list-empty-view-title-text"]'


@dataclass
class User:
    email: str = 'user.name@gmail.com'
    username: str = 'username'
    password: str = 'password'


@dataclass
class Stateful:
    state_path: str = 'browser-state.json'

    def save_context(self, context: BrowserContext) -> None:
        context.storage_state(path=self.state_path)

    def load_context(self, browser: Browser) -> BrowserContext:
        return browser.new_context(storage_state=self.state_path)


@pytest.fixture(scope='session')
def urls() -> URLs:
    return URLs()


@pytest.fixture(scope='session')
def locators() -> Locators:
    return Locators()


@pytest.fixture(scope='session')
def user() -> User:
    return User()


@pytest.fixture(scope='session')
def stateful() -> Stateful:
    return Stateful()


@pytest.fixture(scope='session')
def initialize_browser_state(stateful: Stateful, urls: URLs, locators: Locators, user: User,
                             playwright: Playwright) -> None:
    with playwright.chromium.launch(headless=True) as browser:
        context = browser.new_context()
        page = context.new_page()

        page.goto(urls.registration)
        page.locator(locators.email_input).fill(user.email)
        page.locator(locators.username_input).fill(user.username)
        page.locator(locators.password_input).fill(user.password)
        page.locator(locators.registration_button).click()

        stateful.save_context(context)


@pytest.fixture
def chromium_page_with_state(initialize_browser_state: None, stateful: Stateful, playwright: Playwright) -> Page:
    with playwright.chromium.launch(headless=False) as browser:
        context = stateful.load_context(browser)
        yield context.new_page()
