from django.test import TestCase

from morelia.decorators import tags

from tasks.factories import UserFactory, TaskFactory
from tasks.models import Task


@tags(['unit', 'slow'])
class TaskManagerGetForOwnerByAuthorTest(TestCase):
    """ :py:meth:`tasks.managers.TaskManager.get_for_owner_by_author` """

    def setUp(self):
        self._owner = UserFactory.create()
        self._num = 10

    def test_should_return_own_tasks(self):
        # Arrange
        TaskFactory.create_batch(
            self._num,
            owner=self._owner,
            author=self._owner)

        # Act
        result = Task.objects.get_for_owner_by_author(self._owner, self._owner)

        # Assert - should validate
        self.assertEqual(len(result), self._num)
        for task in result:
            self.assertEqual(task.owner, self._owner)
            self.assertEqual(task.author, self._owner)

    def test_should_return_tasks_for_owner_by_author(self):
        # Arrange
        author = UserFactory.create()
        TaskFactory.create_batch(
            self._num,
            owner=self._owner,
            author=author)

        # Act
        result = Task.objects.get_for_owner_by_author(self._owner, author)

        # Assert
        self.assertEqual(len(result), self._num)
        for task in result:
            self.assertEqual(task.owner, self._owner)
            self.assertEqual(task.author, author)
            self.assertNotEqual(author, self._owner)
