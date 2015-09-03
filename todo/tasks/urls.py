from django.conf.urls import url

from .forms import RestrictedAddTaskForm
from .views import AddTaskView


urlpatterns = [
    url(r'^(?P<profile>\w+)/$', AddTaskView.as_view(form_class=RestrictedAddTaskForm), name='profile_tasks'),
    url(r'^$', AddTaskView.as_view(), name='my_tasks'),
]
