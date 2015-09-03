from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

from .forms import AddTaskForm


class AddTaskView(TemplateView):

    template_name = 'tasks/index.html'
    form_class = AddTaskForm
    users_manager = User.objects

    def get(self, request, *args, **kwargs):
        author = request.user
        owner = self._get_owner()
        form = self.form_class(author=author, owner=owner)
        context = {
            'form': form,
            'owner': owner,
            'author': author,
        }
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        author = request.user
        owner = self._get_owner()
        form = self.form_class(request.POST, author=author, owner=owner)
        if form.is_valid():
            obj = form.save()
            return HttpResponseRedirect(obj.get_absolute_url())
        context = {
            'form': form,
            'owner': owner,
            'author': author,
        }
        return self.render_to_response(context)

    def _get_owner(self):
        try:
            profile_login = self.kwargs['profile']
        except KeyError:
            owner = self.request.user
        else:
            owner = self.users_manager.get(username=profile_login)
        return owner
