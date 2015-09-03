from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models

from .managers import TaskManager


DEFAULT_PRIORITY = 1


class Task(models.Model):

    title = models.CharField(max_length=100)
    priority = models.PositiveSmallIntegerField(default=DEFAULT_PRIORITY)
    owner = models.ForeignKey(User, related_name='owner')
    author = models.ForeignKey(User, related_name='author')

    objects = TaskManager()

    def get_absolute_url(self):
        return reverse('profile_tasks', kwargs={'profile': self.owner.username})
