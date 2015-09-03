from django.forms import ModelForm, ValidationError

from .models import Task

PRIORITY_BASE = 2
TASKS_LIMIT = 10


class AddTaskForm(ModelForm):

    class Meta:
        model = Task
        fields = ('title', 'priority')

    def __init__(self, *args, **kwargs):
        self._owner = kwargs.pop('owner')
        self._author = kwargs.pop('author')
        super(AddTaskForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        kwargs['commit'] = False
        obj = super(AddTaskForm, self).save(*args, **kwargs)
        obj = self._set_default_attributes(obj)
        obj.save()
        return obj

    def _set_default_attributes(self, obj):
        obj.author = self._author
        obj.owner = self._owner
        return obj


class RestrictedAddTaskForm(AddTaskForm):

    class Meta:
        model = Task
        fields = ('title',)

    def __init__(self, *args, **kwargs):
        self._tasks_manager = kwargs.pop('tasks_manager', Task.objects)
        super(RestrictedAddTaskForm, self).__init__(*args, **kwargs)

    def _set_default_attributes(self, obj):
        obj = super(RestrictedAddTaskForm, self)._set_default_attributes(obj)
        tasks_num = self._tasks_manager.get_for_owner_by_author(
            self._owner, self._author).count()
        obj.priority = PRIORITY_BASE ** tasks_num
        return obj

    def clean(self):
        cleaned_data = super(RestrictedAddTaskForm, self).clean()
        tasks_num = self._tasks_manager.get_for_owner_by_author(
            self._owner, self._author).count()
        if tasks_num > TASKS_LIMIT:
            raise ValidationError("You have added to many tasks for %s" % self._owner.username)
        return cleaned_data
