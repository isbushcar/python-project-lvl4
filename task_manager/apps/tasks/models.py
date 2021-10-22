from django.contrib.auth.models import User
from django.db import models
from task_manager.models import Label, Status


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
