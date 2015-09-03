from django.test import TestCase

from morelia.decorators import tags
from smarttest.decorators import no_db_testcase

from tasks.factories import TaskFactory, UserFactory


@no_db_testcase
@tags(['unit'])
class TaskGetAbsoluteUrlTest(TestCase):
    ''' :py:meth:`tasks.models.Task.get_absolute_url` '''

    def test_should_return_task_absolute_url(self):
        # Arrange
        owner = UserFactory.build(pk=1)
        task = TaskFactory.build(owner=owner, author=owner)

        # Act
        url = task.get_absolute_url()

        # Assert
        self.assertEqual(url, '/%s/' % owner.username)
