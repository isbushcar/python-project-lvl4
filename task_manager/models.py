"""Get all models to make them able to reimport."""
from django.contrib.auth.models import User  # noqa: F401

from task_manager.apps.labels.models import Label  # noqa: F401
from task_manager.apps.statuses.models import Status  # noqa: F401
from task_manager.apps.tasks.models import Task  # noqa: F401
