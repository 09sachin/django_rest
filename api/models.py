from django.db import models


class ToDo(models.Model):
    name = models.CharField(max_length=1000)
    details = models.CharField(max_length=10000)

    def __str__(self):
        return self.name
