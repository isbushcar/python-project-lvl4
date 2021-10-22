from django.db import models
from django.contrib.auth.models import User


from task_manager.apps.labels.models import Label
from task_manager.apps.statuses.models import Status
from task_manager.apps.tasks.models import Task


# Change default user __str__ method
User.add_to_class('__str__', lambda self: f'{self.first_name} {self.last_name}')
