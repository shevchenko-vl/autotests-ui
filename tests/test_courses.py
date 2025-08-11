import pytest
from playwright.sync_api import expect


@pytest.mark.courses
@pytest.mark.regression
def test_empty_courses_list(chromium_page_with_state, urls, locators):
    page = chromium_page_with_state
    page.goto(urls.courses)

    courses_title = page.locator(locators.courses_toolbar_title)
    expect(courses_title).to_be_visible()
    expect(courses_title).to_have_text('Courses')

    courses_empty_view = page.locator(locators.courses_empty_view_title)
    expect(courses_empty_view).to_be_visible()
    expect(courses_empty_view).to_have_text('There is no results')
