from django.db import models
import datetime


class Cooperative(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Principle(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()

    def __str__(self):
        return self.name


class Event(models.Model):
    cooperative = models.ForeignKey(Cooperative, on_delete=models.CASCADE)
    principle = models.ForeignKey(Principle, on_delete=models.CASCADE, null=True)
    date = models.DateField(default=datetime.date.today)
    description = models.TextField()

    def __str__(self):
        return '%s - %s ' % (self.date, self.principle)
