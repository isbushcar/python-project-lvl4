from django.db import models
from django.urls import reverse


class Label(models.Model):
    name = models.CharField(max_length=100, unique=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('labels')
