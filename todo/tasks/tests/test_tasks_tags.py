from django.test import TestCase

from mock import Mock, sentinel
from morelia.decorators import tags

from tasks.templatetags.tasks_tags import _show_current_tasks, is_visible_for
from tasks.models import Task


@tags(['unit'])
class ShowCurrentTasksTest(TestCase):
    """ :py:func:`tasks.templatetags.tasks_tags._show_current_tasks` """

    def test_should_show_tasks_for_profile(self):
        # Arrange
        tasks_manager = Mock(Task.objects)
        tasks_manager.get_for_owner.return_value = sentinel.current_tasks

        # Act
        result = _show_current_tasks(
            sentinel.profile,
            sentinel.user,
            tasks_manager=tasks_manager)

        # Assert
        self.assertEqual(result['user'], sentinel.user)
        self.assertEqual(result['tasks'], sentinel.current_tasks)
        tasks_manager.get_for_owner.assert_called_once_with(sentinel.profile)


@tags(['unit'])
class IsVisibleForTest(TestCase):
    """ :py:func:`tasks.templatetags.tasks_tags.is_visible_for` """

    def test_should_return_true_for_author_tasks(self):
        # Arrange
        task = Mock(Task)
        task.author = sentinel.author
        task.owner = sentinel.owner

        # Act
        result = is_visible_for(task, sentinel.author)

        # Assert
        self.assertTrue(result)

    def test_should_return_true_for_owner_tasks(self):
        # Arrange
        task = Mock(Task)
        task.author = sentinel.author
        task.owner = sentinel.owner

        # Act
        result = is_visible_for(task, sentinel.owner)

        # Assert
        self.assertTrue(result)

    def test_should_return_false_for_foreign_tasks(self):
        # Arrange
        task = Mock(Task)
        task.author = sentinel.owner
        task.owner = sentinel.owner

        # Act
        result = is_visible_for(task, sentinel.author)

        # Assert
        self.assertFalse(result)
