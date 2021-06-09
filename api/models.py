from django.db import models
import datetime


class ToDo(models.Model):
    name = models.CharField(max_length=1000)
    details = models.CharField(max_length=10000)
    created_at = models.DateTimeField(default=datetime.datetime.now)
    updated_at = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.name


class TimeSeries(models.Model):
    state = models.CharField(max_length=1000)
    dates = models.ManyToManyField('Dates',related_name='state_date')
    def __str__(self):
        return self.state


class Dates(models.Model):
    date = models.CharField(max_length=1000)
    delta = models.ForeignKey('Delta', on_delete=models.SET_NULL, null=True)
    delta7 = models.ForeignKey('Delta7', on_delete=models.SET_NULL, null=True)
    total = models.ForeignKey('Total', on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.date


class Delta(models.Model):
    delta = models.ForeignKey('CRDTV', on_delete=models.SET_NULL, null=True)

class Delta7(models.Model):
    delta7 = models.ForeignKey('CRDTV', on_delete=models.SET_NULL, null=True)


class Total(models.Model):
    total = models.ForeignKey('CRDTV', on_delete=models.SET_NULL, null=True)


class CRDTV(models.Model):
    confirmed = models.CharField(max_length=1000, null=True)
    recovered = models.CharField(max_length=1000, null=True)
    deceased = models.CharField(max_length=1000, null=True)
    tested = models.CharField(max_length=1000, null=True)
    vaccinated = models.CharField(max_length=1000, null=True)

