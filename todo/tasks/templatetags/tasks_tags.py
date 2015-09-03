from django import template

from tasks.models import Task


register = template.Library()


def _show_current_tasks(profile, user, tasks_manager=Task.objects):
    tasks = tasks_manager.get_for_owner(profile)
    return {'tasks': tasks, 'user': user}


@register.inclusion_tag('tasks/show_current_tasks.html')
def show_current_tasks(profile, user):
    return _show_current_tasks(profile, user)


@register.filter
def is_visible_for(task, user):
    return user in [task.owner, task.author]
