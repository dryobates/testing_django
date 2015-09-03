from django.db.models import Manager


class TaskManager(Manager):

    def get_for_owner_by_author(self, owner, author):
        return self.get_queryset().filter(owner=owner, author=author)

    def get_for_owner(self, owner):
        return self.get_queryset().filter(owner=owner)
