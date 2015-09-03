from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory

from mock import Mock, sentinel
from morelia.decorators import tags
from smarttest.decorators import no_db_testcase

from tasks.forms import AddTaskForm
from tasks.views import AddTaskView


class AddTaskViewTest(TestCase):

    def setUp(self):
        self._factory = RequestFactory()
        self._form_class = Mock(AddTaskForm)
        self._users_manager = Mock(User.objects)
        self._view = AddTaskView.as_view(
            form_class=self._form_class,
            users_manager=self._users_manager)


@no_db_testcase
@tags(['unit'])
class AddTaskViewGetTest(AddTaskViewTest):
    ''' :py:meth:`tasks.views.AddTaskView.get` '''

    def test_should_display_task_creation_form(self):
        # Arrange
        url = reverse('my_tasks')
        request = self._factory.get(url)
        request.user = Mock(User)

        # Act
        response = self._view(request)

        # Assert
        self.assertTrue('form' in response.context_data)

    def test_should_display_task_creation_form_for_others(self):
        # Arrange
        profile = 'test1'
        url = reverse('profile_tasks', kwargs={'profile': profile})
        self._users_manager.get.return_value = sentinel.profile
        request = self._factory.get(url)
        request.user = Mock(User)

        # Act
        response = self._view(request, profile=profile)

        # Assert
        self.assertTrue('form' in response.context_data)
        self.assertEqual(response.context_data['owner'], sentinel.profile)


@no_db_testcase
@tags(['unit'])
class AddTaskViewPostTest(AddTaskViewTest):
    ''' :py:meth:`tasks.views.AddTaskView.post` '''

    def test_should_save_form_and_redirect_on_success(self):
        # Arrange
        url = reverse('my_tasks')
        form = self._form_class.return_value
        form.is_valid.return_value = True
        redirect_url = '/some/url'
        obj = form.save.return_value
        obj.get_absolute_url.return_value = redirect_url
        data = {
            'title': sentinel.title,
        }
        request = self._factory.post(url, data)
        request.user = Mock(User)

        # Act
        response = self._view(request)

        # Assert
        self.assertTrue(form.save.called)
        self.assertTrue(obj.get_absolute_url.called)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], redirect_url)

    def test_should_show_errors_on_invalid_data(self):
        # Arrange
        url = reverse('my_tasks')
        form = self._form_class.return_value
        form.is_valid.return_value = False
        data = {}
        request = self._factory.post(url, data)
        request.user = Mock(User)

        # Act
        response = self._view(request)

        # Assert
        self.assertFalse(form.save.called)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context_data)
