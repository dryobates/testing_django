import os

from django.test import TestCase

from morelia import run
from morelia.decorators import tags
from splinter import Browser

from tasks.factories import UserFactory


@tags(['acceptance'])
class AddTask(TestCase):

    def setUp(self):
        self._browser = Browser('django')

    def test_add_task(self):
        filename = os.path.join(os.path.dirname(__file__),
                                '../../docs/features/add_task.feature')
        run(filename, self, verbose=True)

    def step_user_exists(self, username):
        r'user "([^"]+)" exists'

        user = UserFactory.build(username=username)
        user.is_staff = True
        user.set_password(username)
        user.save()

    def step_I_visit_page_as_logged_user(self, page, username):
        r'I visit "([^"]+)" as logged user "([^"]+)"'

        self._browser.visit('/admin/')
        self._browser.fill('username', username)
        self._browser.fill('password', username)
        self._browser.find_by_value('Log in').first.click()
        self._browser.visit(page)

    def step_I_enter_value_in_field(self, value, field):
        r'I enter "([^"]+)" in field "([^"]+)"'

        self._browser.fill(field, value)

    def step_I_press(self, button):
        r'I press button "([^"]+)"'

        self._browser.find_by_name(button).first.click()

    def step_I_see_task_on_tasks_list(self, task):
        r'I see task "([^"]+)" on tasks list'

        task_on_list = self._browser.find_by_xpath('//ul[@id="todo"]/li[contains(., "%s")]' % task)
        self.assertTrue(task_on_list)
