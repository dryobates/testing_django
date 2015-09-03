from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

import factory

from .models import Task, DEFAULT_PRIORITY


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    id = factory.Sequence(lambda n: n)
    username = factory.Sequence(lambda n: 'user{0}'.format(n))
    email = factory.LazyAttribute(lambda a: '{0}@example.com'.format(a.username).lower())
    password = make_password('test')


class TaskFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Task

    title = factory.Sequence(lambda n: 'title{0}'.format(n))
    priority = DEFAULT_PRIORITY
    owner = factory.SubFactory(UserFactory)
    author = factory.SubFactory(UserFactory)
