from django.db import models
from django.contrib.auth.models import User


from task_manager.apps.statuses.models import Status


# Change default user __str__ method
User.add_to_class('__str__', lambda self: f'{self.first_name} {self.last_name}')


class Label(models.Model):
    name = models.CharField(max_length=100, unique=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='executor_foreign_key',
    )
    creation_date = models.DateTimeField(auto_now_add=True)
    labels = models.ManyToManyField(Label)

    def __str__(self):
        return self.name
