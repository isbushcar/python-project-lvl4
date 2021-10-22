from django.db import models


class Label(models.Model):
    name = models.CharField(max_length=100, unique=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
