import pytest

from pages.courses.courses_list_page import CoursesListPage
from pages.courses.create_course_page import CreateCoursePage


@pytest.mark.courses
@pytest.mark.regression
class TestCourses:
    def test_empty_courses_list(self, courses_list_page: CoursesListPage):
        courses_list_page.visit('https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/courses')

        courses_list_page.navbar.check_visible('username')
        courses_list_page.sidebar.check_visible()
        courses_list_page.toolbar_view.check_visible()
        courses_list_page.check_visible_empty_view()

    def test_create_course(self, create_course_page: CreateCoursePage, courses_list_page: CoursesListPage):
        create_course_page.visit('https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/courses/create')

        create_course_page.create_course_toolbar.check_visible()

        create_course_page.image_upload_widget.check_visible(is_image_uploaded=False)

        create_course_page.create_course_form.check_visible(
            title='',
            estimated_time='',
            description='',
            max_score='0',
            min_score='0'
        )

        create_course_page.exercises_toolbar.check_visible()
        create_course_page.check_visible_exercises_empty_view()

        create_course_page.image_upload_widget.upload_preview_image('./testdata/files/image.png')
        create_course_page.image_upload_widget.check_visible(is_image_uploaded=True)

        new_course = {
            'title': 'Playwright',
            'estimated_time': '2 weeks',
            'description': 'Playwright',
            'max_score': '100',
            'min_score': '10',
        }
        create_course_page.create_course_form.fill(**new_course)
        create_course_page.create_course_form.check_visible(**new_course)

        create_course_page.create_course_toolbar.check_visible(is_create_course_disabled=False)
        create_course_page.create_course_toolbar.click_create_course_button()

        courses_list_page.toolbar_view.check_visible()
        courses_list_page.course_view.check_visible(
            index=0,
            title=new_course['title'],
            estimated_time=new_course['estimated_time'],
            max_score=new_course['max_score'],
            min_score=new_course['min_score']
        )

    def test_edit_course(self, create_course_page: CreateCoursePage, courses_list_page: CoursesListPage):
        create_course_page.visit('https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/courses/create')

        create_course_page.image_upload_widget.upload_preview_image('./testdata/files/image.png')
        new_course = {
            'title': 'Playwright2',
            'estimated_time': '21 weeks',
            'description': 'Playwright2',
            'max_score': '42',
            'min_score': '21',
        }
        create_course_page.create_course_form.fill(**new_course)
        create_course_page.create_course_toolbar.click_create_course_button()

        courses_list_page.course_view.check_visible(
            index=0,
            title=new_course['title'],
            estimated_time=new_course['estimated_time'],
            max_score=new_course['max_score'],
            min_score=new_course['min_score']
        )

        courses_list_page.course_view.menu.click_edit(index=0)
        create_course_page.create_course_form.check_visible(**new_course)

        edited_course = {
            'title': 'Playwright2_edited',
            'estimated_time': '42 weeks',
            'description': 'Playwright2 edited',
            'max_score': '43',
            'min_score': '22',
        }
        create_course_page.create_course_form.fill(**edited_course)
        create_course_page.create_course_form.check_visible(**edited_course)
        create_course_page.create_course_toolbar.click_create_course_button()

        courses_list_page.toolbar_view.check_visible()
        courses_list_page.course_view.check_visible(
            index=0,
            title=edited_course['title'],
            estimated_time=edited_course['estimated_time'],
            max_score=edited_course['max_score'],
            min_score=edited_course['min_score']
        )
