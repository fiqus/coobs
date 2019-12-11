from django.db import models
import datetime


class Principle(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    visible = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Action(models.Model):
    principle = models.ForeignKey(Principle, on_delete=models.CASCADE, null=True)
    date = models.DateField(default=datetime.date.today)
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    invested_money = models.DecimalField(max_digits=19, decimal_places=2, null=True)

    def __str__(self):
        return '%s - %s ' % (self.date, self.principle)


class Period(models.Model):
    name = models.CharField(max_length=256, null=True, blank=True)
    date_from = models.DateField(default=datetime.date.today)
    date_to = models.DateField(default=datetime.date.today)
    actions_budget = models.DecimalField(max_digits=19, decimal_places=2)

    def __str__(self):
        return self.name

    @staticmethod
    def get_date_period(date):
        return Period.objects.filter(date_from__lte=date, date_to__gte=date)

    def get_current(self):
        today = datetime.date.today()
        # Note that if there are two periods that overlap, it returns the last one.
        return self.get_date_period(today).last()

class Cooperative(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False, unique=True)
    business_name = models.CharField(max_length=128, null=False, blank=False, unique=True)
    starting_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return '%s' % (self.business_name)

class Partner(models.Model):
    first_name = models.CharField(max_length=128, null=False, blank=False)
    last_name = models.CharField(max_length=128)
    email = models.EmailField(max_length=128, null=False, blank=False, unique=True)
    password = models.CharField(max_length=128, blank=False)
    cooperative = models.ForeignKey(Cooperative, on_delete=models.CASCADE, blank=False, null=True)

    def __str__(self):
        return '%s %s - %s' % (self.first_name, self.last_name, self.cooperative)