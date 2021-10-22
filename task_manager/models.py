"""Get all models to make them able to reimport."""
from django.contrib.auth.models import User

from task_manager.apps.labels.models import Label
from task_manager.apps.statuses.models import Status
from task_manager.apps.tasks.models import Task
