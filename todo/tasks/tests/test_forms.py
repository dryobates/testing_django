from django.test import TestCase

from mock import Mock
from morelia.decorators import tags
from smarttest.decorators import no_db_testcase

from tasks.factories import UserFactory
from tasks.forms import AddTaskForm, RestrictedAddTaskForm, TASKS_LIMIT
from tasks.models import Task


class AddTaskFormTest(TestCase):

    def setUp(self):
        self._title = 'some title'
        self._priority = 5
        self._data = {
            'title': self._title,
            'priority': self._priority,
        }


@no_db_testcase
@tags(['unit'])
class AddTaskFormIsValidTest(AddTaskFormTest):
    """ :py:meth:`tasks.forms.AddTaskForm.is_valid` """

    def test_should_validate_input(self):
        # Arrange
        owner = UserFactory.build()
        form = AddTaskForm(self._data, author=owner, owner=owner)

        # Act
        result = form.is_valid()

        # Assert
        self.assertTrue(result)
        self.assertEqual(form.cleaned_data['title'], self._title)
        self.assertEqual(form.cleaned_data['priority'], self._priority)


@tags(['unit', 'slow'])
class AddTaskFormSaveTest(AddTaskFormTest):
    """ :py:meth:`tasks.forms.AddTaskForm.save` """

    def test_should_create_task(self):
        # Arrange
        owner = UserFactory.create()
        form = AddTaskForm(self._data, author=owner, owner=owner)

        # Act
        form.is_valid()
        obj = form.save()

        # Assert
        self.assertIsNotNone(obj.pk)
        self.assertEqual(obj.title, self._title)
        self.assertEqual(obj.priority, self._priority)
        self.assertEqual(obj.author, owner)
        self.assertEqual(obj.owner, owner)


class RestrictedAddTaskFormTest(TestCase):

    def setUp(self):
        self._title = 'some title'
        self._priority = 5
        self._data = {
            'title': self._title,
            'priority': self._priority,
        }


@no_db_testcase
@tags(['unit'])
class RestrictedAddTaskFormValidTest(RestrictedAddTaskFormTest):
    """ :py:meth:`tasks.forms.RestrictedAddTaskForm.is_valid` """

    def test_should_ignore_priority_if_passed(self):
        # Arrange
        author = UserFactory.build()
        owner = UserFactory.build()
        tasks_manager = Mock(Task.objects)
        tasks_manager.get_for_owner_by_author.return_value.count.return_value = 0
        form = RestrictedAddTaskForm(
            self._data, author=author, owner=owner,
            tasks_manager=tasks_manager)

        # Act
        result = form.is_valid()

        # Assert
        self.assertTrue(result)
        self.assertEqual(form.cleaned_data['title'], self._title)
        self.assertTrue('priority' not in form.cleaned_data)

    def test_should_return_not_valid_if_too_many_tasks(self):
        # Arrange
        author = UserFactory.build()
        owner = UserFactory.build()
        tasks_manager = Mock(Task.objects)
        tasks_manager.get_for_owner_by_author.return_value.count.return_value = TASKS_LIMIT + 1
        form = RestrictedAddTaskForm(
            self._data, author=author, owner=owner,
            tasks_manager=tasks_manager)

        # Act
        result = form.is_valid()

        # Assert
        self.assertFalse(result)
        msg = 'You have added to many tasks for %s' % owner.username
        self.assertTrue(msg in form.errors['__all__'])


@tags(['unit', 'slow'])
class RestrictedAddTaskFormSaveTest(RestrictedAddTaskFormTest):
    """ :py:meth:`tasks.forms.RestrictedAddTaskForm.save` """

    def test_should_create_task_with_default_priority(self):
        # Arrange
        author = UserFactory.create()
        owner = UserFactory.create()
        tasks_manager = Mock(Task.objects)
        form = RestrictedAddTaskForm(
            self._data, author=author, owner=owner,
            tasks_manager=tasks_manager)
        author_tasks = tasks_manager.get_for_owner_by_author.return_value
        author_tasks.count.return_value = 2

        # Act
        form.is_valid()
        obj = form.save()

        # Assert
        self.assertIsNotNone(obj.pk)
        self.assertEqual(obj.title, self._title)
        self.assertEqual(obj.priority, 4)
        self.assertEqual(obj.author, author)
        self.assertEqual(obj.owner, owner)
