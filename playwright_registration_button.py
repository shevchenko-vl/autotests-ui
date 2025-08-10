from playwright.sync_api import sync_playwright, expect


REG_URL = 'https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/auth/registration'
TEST_ID = 'data-testid'
EMAIL_LOC = f'//*[@{TEST_ID}="registration-form-email-input"]//input'
USERNAME_LOC = f'//*[@{TEST_ID}="registration-form-username-input"]//input'
PASSWORD_LOC = f'//*[@{TEST_ID}="registration-form-password-input"]//input'
REG_LOC = f'//*[@{TEST_ID}="registration-page-registration-button"]'


with sync_playwright() as playwright:
    page = playwright.chromium.launch(headless=False).new_page()
    page.goto(REG_URL)

    registration_button = page.locator(REG_LOC)
    expect(registration_button).to_be_disabled()

    page.locator(EMAIL_LOC).fill('user.name@gmail.com')
    page.locator(USERNAME_LOC).fill('username')
    page.locator(PASSWORD_LOC).fill('password')

    expect(registration_button).to_be_enabled()
