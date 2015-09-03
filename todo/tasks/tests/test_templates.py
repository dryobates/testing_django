from django.test import TestCase
from django.template.loader import render_to_string

from morelia.decorators import tags

from tasks.factories import UserFactory, TaskFactory


@tags(['unit'])
class ShowCurrentTasksTest(TestCase):
    """ tasks/show_current_tasks.html """

    def test_should_show_all_tasks_for_owner(self):
        # Arrange
        template_name = 'tasks/show_current_tasks.html'
        owner = UserFactory.build()
        wife = UserFactory.build()
        bread = "buy bread"
        milk = "buy milk"
        tasks = [
            TaskFactory.build(title=bread, owner=owner, author=owner),
            TaskFactory.build(title=milk, owner=owner, author=wife),
        ]
        context = {
            'tasks': tasks,
            'user': owner,
        }
        # Act
        result = render_to_string(template_name, context)

        # Assert
        self.assertTrue("buy bread" in result)
        self.assertTrue("buy milk" in result)

    def test_should_show_only_author_tasks_on_foreign_profile(self):
        # Arrange
        template_name = 'tasks/show_current_tasks.html'
        owner = UserFactory.build()
        wife = UserFactory.build()
        bread = "buy bread"
        milk = "buy milk"
        tasks = [
            TaskFactory.build(title=bread, owner=owner, author=owner),
            TaskFactory.build(title=milk, owner=owner, author=wife),
        ]
        context = {
            'tasks': tasks,
            'user': wife,
        }
        # Act
        result = render_to_string(template_name, context)

        # Assert
        self.assertFalse("buy bread" in result)
        self.assertTrue("buy milk" in result)
