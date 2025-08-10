from playwright.sync_api import sync_playwright, expect


REG_URL = 'https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/auth/registration'
COURSES_URL = 'https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/courses'
BROWSER_STATE_PATH = 'browser-state.json'
TEST_ID = 'data-testid'

EMAIL_LOC = f'//*[@{TEST_ID}="registration-form-email-input"]//input'
USERNAME_LOC = f'//*[@{TEST_ID}="registration-form-username-input"]//input'
PASSWORD_LOC = f'//*[@{TEST_ID}="registration-form-password-input"]//input'
REG_LOC = f'//*[@{TEST_ID}="registration-page-registration-button"]'
COURSES_TOOLBAR_TITLE_LOC = f'//*[@{TEST_ID}="courses-list-toolbar-title-text"]'
COURSES_EMPTY_VIEW_TITLE_LOC = f'//*[@{TEST_ID}="courses-list-empty-view-title-text"]'

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(REG_URL)

    page.locator(EMAIL_LOC).fill('user.name@gmail.com')
    page.locator(USERNAME_LOC).fill('username')
    page.locator(PASSWORD_LOC).fill('password')
    page.locator(REG_LOC).click()

    expect(page).not_to_have_url(REG_URL)

    context.storage_state(path=BROWSER_STATE_PATH)

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(storage_state=BROWSER_STATE_PATH)
    page = context.new_page()
    page.goto(COURSES_URL)

    courses_title = page.locator(COURSES_TOOLBAR_TITLE_LOC)
    expect(courses_title).to_be_visible()
    expect(courses_title).to_have_text('Courses')

    courses_empty_view = page.locator(COURSES_EMPTY_VIEW_TITLE_LOC)
    expect(courses_empty_view).to_be_visible()
    expect(courses_empty_view).to_have_text('There is no results')
