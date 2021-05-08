from django.db import models
import datetime

class ToDo(models.Model):
    name = models.CharField(max_length=1000)
    details = models.CharField(max_length=10000)
    created_at = models.DateTimeField(default=datetime.datetime.now)
    updated_at = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.name
